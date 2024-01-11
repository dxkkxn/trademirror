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
                console.log('HistorySection : Network response was not ok.');
                return null;
            }
            return response.json();
        })
        .then(data => {
          let dict = JSON.parse(data);
          // limit to 5
          if (dict.length > 5)
          {
            dict = dict.slice(0,5);
          }
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
                  {history == null || history.length === 0 || !Array.isArray(history) ? (
                    <Button w="full" mt="6" colorScheme="gray">
                        View All
                    </Button>
                ) : (
                  <Stack>

                  {history.map((transaction, index) => (
                    <Flex p="1" key={index} gap="4" w="full">
                    <Flex justify="space-between" w="full">
                    <Stack>
                    <Text textStyle="h6" color={transaction.op === 'BUY' ? "green" : "red"}>
                      {transaction.op === 'BUY' ? ('Bought') : ('Sold')} {transaction.amount} BTC
                    </Text>
                    <Text fontSize="sm">
                    Bitcoin Price: {transaction.btc_price} $
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
