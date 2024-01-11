import React, { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';


const HistorySection = () => {

    const fetchIntervalVal = 3
    const [history, setHistory] = useState({})

    // Function to fetch last n transactions
    const fetchHistory = () => {
    fetch('/api/user_history')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            const dict = JSON.parse(data);
            setHistory(dict);
        })
        .catch(error => {
            console.error('Error fetching history:', error);
        });
    };

    useEffect(() => {
        const fetchInterval = setInterval(() => {
            fetchHistory();
        }, 1000 * fetchIntervalVal);
        fetchHistory();
        return () => {
          clearInterval(fetchInterval);
        };
      // polling all relevant data
    }, []);

    return (
            <CustomCard borderRadius="xl">
                <Text textStyle="h2" color="black.80">Recent Transactions</Text>
                  {history == null || Object.keys(history).length === 0 ? (
                    <Button w="full" mt="6" colorScheme="gray">
                        View All
                    </Button>
                ) : (
                  <Stack>
                  {Object.keys(history).map((key) => (
                            <Flex p="1" key={key} gap="4" w="full">
 
                              <Flex justify="space-between" w="full" >
                                  <Stack >
                                      <Text textStyle="h6">
                                          <b>{history[key].time}</b>
                                      </Text>
                                      <Text fontSize="sm" color= {history[key].amount.includes('+') ? "green" : "red"}>
                                          Amount : {history[key].amount}
                                      </Text>
                                      <Text textStyle="h6">
                                          Bitcoin Price : {history[key].btc_price} $
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
