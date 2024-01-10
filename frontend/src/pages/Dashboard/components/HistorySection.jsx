import React , { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';


const HistorySection = () => {

  const fetchIntervalVal = 3
  const [lastTransactionsPrivate, setLastTransactionsPrivate] = useState({})

   // Function ro fetch last n transactions
  const fetchTransactionsPrivate = () => {
     /*
     fetch('/api/latest_transactions')
     .then(response => response.json())
      .then(data => setLastTransactionsPrivate(data))
      console.log(data);*/
      // catch
  }

  const fetchInterval = setInterval(() => {
   fetchTransactionsPrivate(10);
  }, 1000 * fetchIntervalVal); // polling all relevant data


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
    
  ];

  return (
    <CustomCard borderRadius="xl">
        <Text textStyle="h2" color="black.80" >Recent Transactions</Text>
        <Stack>
            {transactions.map((transaction) => (
                <Flex p="1" key={transaction.id} gap="4" w="full" >
                    
                    <Flex justify="space-between" w="full" >
                        <Stack >
                            <Text textStyle="h6">
                                {transaction.text}
                            </Text>
                            <Text fontSize="sm" color="black.40">
                                {transaction.timestamp}
                            </Text>

                        </Stack>
                        <Text textStyle="h6">
                                {transaction.amount}
                            </Text>

                    </Flex>
                </Flex>
            ))}
        </Stack>
        <Button w="full" mt="6" colorScheme="gray">
            View All
        </Button>

    </CustomCard>
  );
};

export default HistorySection;
