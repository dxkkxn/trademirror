import React , { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';

const Wallets = () => {

  const fetchIntervalVal = 3
    const [lastTransactionsPrivate, setLastTransactionsPrivate] = useState({})

    // Function to fetch last n transactions
    const fetchTransactionsPrivate = () => {
    fetch('/api/latest_transactions')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            const dict = JSON.parse(data);
            setLastTransactionsPrivate(dict);
        })
        .catch(error => {
            console.error('Error fetching transactions:', error);
        });
    }


    // catch
    useEffect(() => {
        const fetchInterval = setInterval(() => {
            fetchTransactionsPrivate();
        }, 1000 * fetchIntervalVal);
        fetchTransactionsPrivate();
        return () => {
          clearInterval(fetchInterval);
        };
      // polling all relevant data
    }, []);

  const treatData = () => {
    // treats data contained in lastTransactionsPublic
  };

return (
            <CustomCard borderRadius="xl">
                <Text textStyle="h2" color="black.80">Recent Global Transactions</Text>
                  {Object.keys(lastTransactionsPrivate).length === 0 ? (
                    <Button w="full" mt="6" colorScheme="gray">
                        View All
                    </Button>
                ) : (
                  <Stack>
                  {Object.keys(lastTransactionsPrivate).map((key) => (
                            <Flex p="1" key={key} gap="4" w="full">
 
                              <Flex justify="space-between" w="full" >
                                  <Stack >
                                      <Text textStyle="h6">
                                          <b>{lastTransactionsPrivate[key].wallet}</b>
                                      </Text>
                                      <Text textStyle="h6">
                                          Balance : {lastTransactionsPrivate[key].current_balance} $
                                      </Text>
                                      <Text fontSize="sm" color= {lastTransactionsPrivate[key].balance_update.includes('+') ? "green" : "red"}>
                                          Evolution : {lastTransactionsPrivate[key].balance_update}
                                      </Text>
                                      <Text textStyle="h6">
                                          Bitcoin Price : {lastTransactionsPrivate[key].btc_price}
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
