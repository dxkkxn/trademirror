import React , { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';

const Wallets = () => {

  const fetchIntervalVal = 3
    const [lastTransactions, setLastTransactions] = useState({})

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
            const dict = JSON.parse(data);
            setLastTransactions(dict);
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

  const treatData = () => {
    // treats data contained in lastTransactionsPublic
  };

  const follow = (wallet_hash) => {
    console.log("Called follow");
    console.log(wallet_hash);
    fetch('/api/follow_wallet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({wallet_hash: wallet_hash}),
      })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
          else {
            alert ("Followed successfully wallet");
            return response.json();
          }
        })
        .catch(error => {
            console.error('Error following wallets:', error);
        });
    }



return (
            <CustomCard borderRadius="xl">
                <Text textStyle="h2" color="black.80">Recent Global Transactions</Text>
                  {Object.keys(lastTransactions).length === 0 ? (
                    <Button w="full" mt="6" colorScheme="gray">
                        View All
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
                                      <Button onClick={()=>follow(lastTransactions[key].wallet)} w="full" mt="6" colorScheme="green">
                                        Follow
                                      </Button>

                                      <Text textStyle="h6">
                                          Balance : {lastTransactions[key].current_balance} $ (
                                            <span style={{ color: lastTransactions[key].balance_update.includes('+') ? 'green' : 'red' }}>
                                            {lastTransactions[key].balance_update}
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
