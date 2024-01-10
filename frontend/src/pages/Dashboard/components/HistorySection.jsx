import React, { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';


const HistorySection = () => {

    const fetchIntervalVal = 3
    const [lastTransactionsPrivate, setLastTransactionsPrivate] = useState({})

    // Function ro fetch last n transactions
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
            console.log(data);
            setLastTransactionsPrivate(data);
        })
        .catch(error => {
            console.error('Error fetching transactions:', error);
            // Handle errors here if necessary
        });
    }

    
    fetchTransactionsPrivate();
    // catch
    useEffect(() => {
        const fetchInterval = setInterval(() => {
            fetchTransactionsPrivate(10);
        }, 1000 * fetchIntervalVal);
        return () => clearInterval(fetchInterval); // polling all relevant data
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
    console.log("transactions : ")
    console.log(lastTransactionsPrivate)

    useEffect((lastTransactionsPrivate) => {
        console.log('updating...');
        if (lastTransactionsPrivate == undefined) {
          return ( 
            <CustomCard borderRadius="xl">
                <Text textStyle="h2" color="black.80" >Recent Transactions</Text>
                <Button w="full" mt="6" colorScheme="gray">
                    View All
                </Button>

            </CustomCard>
          )
        }
        else {
          return (
              <CustomCard borderRadius="xl">
                  <Text textStyle="h2" color="black.80" >Recent Transactions</Text>
                  <Stack>
                      {lastTransactionsPrivate.map((transaction) => (
                          <Flex p="1" key={transaction.current_balance} gap="4" w="full" >

                              <Flex justify="space-between" w="full" >
                                  <Stack >
                                      <Text textStyle="h6">
                                          {transaction.value}
                                      </Text>
                                      <Text fontSize="sm" color="black.40">
                                          {transaction.op}
                                      </Text>

                                  </Stack>
                                  <Text textStyle="h6">
                                      {transaction.btc_price}
                                  </Text>

                              </Flex>
                          </Flex>
                      ))}
                  </Stack>
                  <Button w="full" mt="6" colorScheme="gray">
                      View All
                  </Button>

              </CustomCard>
          )
        }
    });
};

export default HistorySection;
