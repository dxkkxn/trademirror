import React, { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';


const HistorySection = () => {

    const fetchIntervalVal = 3
    const [lastTransactionsPrivate, setLastTransactionsPrivate] = useState({})

    // Function to fetch last n transactions
    const fetchTransactionsPrivate = () => {
    console.log("fetching...");
    fetch('/api/latest_transactions')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            console.log("latest fetched:");
            console.log(data); // {"wallet": {"wallet": "wallet", "current_balance": 150, "balance_update": "+200.0%"}}
            console.log(typeof data); // string
            const dict = JSON.parse(data);
            console.log(dict); 
            console.log(dict["wallet"].balance_update);
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

    /*
      const transactions = [
        {
            id: "1",
            text: "INR Deposit",
            amount: "+$80,000",
            timestamp: "2023-10-22"
        },
        {
            id: "2",
            text: "BTC SELL",
            amount: "-$20,000",
            timestamp: "2023-9-02"
        },
        {

            id:"3",
            text: "INR Deposit",
            amount: "+$100,000",
            timestamp: "2023-08-12"
        },

      ];*/
    return (
            <CustomCard borderRadius="xl">
                <Text textStyle="h2" color="black.80">Recent Transactions</Text>
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

export default HistorySection;
