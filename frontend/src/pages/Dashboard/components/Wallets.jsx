import React , { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';

const Wallets = () => {

  const fetchIntervalVal = 1;
  const [lastTransactions, setLastTransactions] = useState({});
  const [limit, setLimit] = useState(5);

  // const [followedList, setFollowedList] = useState([]);

  const updateFollowedList = (latest_transactions) => {
    fetch('/api/get_following_wallets')
    .then( response => {
      if(!response.ok) {
        console.log('followed wallets network error');
        console.log(response.status);
        return [];
      }
      return response.json();
    })
    .then(data => {
      treatData(latest_transactions, data);
    })
  };

  const treatData = (latest_transactions, followedList) => {
    
    // treats data contained in lastTransactionsPublic
    if(latest_transactions.length > limit) {
      latest_transactions = latest_transactions.slice(0,5);
    }
    // checks if wallet is followed by default user
    // updateFollowedList();
    for (const wallet of latest_transactions) {
      wallet.followed = followedList.includes(wallet.wallet);
    }
    setLastTransactions(latest_transactions);
  };

    // Function to fetch last n transactions
    const fetchTransactions = () => {
    fetch('/api/latest_transactions')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
          const array = JSON.parse(data);
          updateFollowedList(array);
        })
        .catch(error => {
            console.error('Error fetching transactions:', error);
        });
    }


    // catch
    useEffect(() => {
        const fetchInterval = setInterval(() => {
            fetchTransactions();
        }, 1000 * fetchIntervalVal);
        fetchTransactions();
        return () => {
          clearInterval(fetchInterval);
        };
      // polling all relevant data
    }, []);


  const unfollow = (wallet_hash) => {
    fetch('/api/unfollow_wallet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"wallet_id": wallet_hash}),
      })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
          else {
            return response.json();
          }
        })
        .then(() => updateFollowedList(lastTransactions))
        .catch(error => {
            console.error('Error unfollowing wallet:', error);
        });
    }

  const follow = (wallet_hash) => {
    fetch('/api/follow_wallet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"wallet_id": wallet_hash}),
      })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
          else {
            return response.json();
          }
        })
        .then(() => updateFollowedList(lastTransactions))
        .catch(error => {
            console.error('Error following wallets:', error);
        });
    }



return (
            <CustomCard borderRadius="xl">
                <Text textStyle="h2" color="black.80">Recent Global Transactions</Text>
                  {Object.keys(lastTransactions).length === 0 ? (
                    <Button onClick={()=>setLimit(15 - limit)} w="full" mt="6" colorScheme="gray">
                      { limit == 5 ? ('View More') : ( 'View Less') }
                    </Button>
                ) : (
                  <Stack>
                  {Object.keys(lastTransactions).map((key) => (
                            <Flex p="1" key={key} gap="4" w="full">
 
                              <Flex justify="space-between" w="full" >
                                  <Stack >
                                      <Text textStyle="h6">
                                          <b>{lastTransactions[key].wallet}</b>
                                      </Text>
                                      {lastTransactions[key].followed === false ? (
                                        <Button onClick={()=>follow(lastTransactions[key].wallet)} w="full" mt="6" colorScheme="green">
                                          Follow
                                        </Button> ) :
                                        ( 
                                        <Button onClick={()=>unfollow(lastTransactions[key].wallet)} w="full" mt="6" colorScheme="red">
                                          Unfollow
                                        </Button> )}


                                      <Text textStyle="h6">
                                          Balance : {(parseInt(lastTransactions[key].current_balance, 10)*10**-6).toLocaleString()} BTC (
                                            <span style={{ color: lastTransactions[key].balance_update.includes('+') ? 'green' : 'red' }}>
                                            {parseFloat(lastTransactions[key].balance_update.replace('%', '')).toFixed(2) + '%'}
                                          </span> )
                                      </Text>
                                      <Text textStyle="h6">
                                          Bitcoin Price : {lastTransactions[key].btc_price}
                                      </Text>

                                  </Stack>
                              </Flex>
                               
                            </Flex>
                        ))}
                        <Button w="full" mt="6" colorScheme="gray">
                            View All
                        </Button>
                    </Stack>
                )}
            </CustomCard>
        );
    };

export default Wallets;
