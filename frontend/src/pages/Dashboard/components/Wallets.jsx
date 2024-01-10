import React , { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';

const fetchIntervalVal = 3

const Wallets = () => {
  const dbFetchInterval = 3
  const [lastTransactionsPublic, setLastTransactionsPublic] = useState({})

  // Function ro fetch last n transactions
  const fetchTransactionsPublic = () => {
    fetch('/api/latest_transactions')
    .then(response => response.json())
    .then(data => setLastTransactionsPublic(data))
    .then(console.log(lastTransactionsPublic))
    .catch(() => console.log('Error fetching wallets'));
  }


  const treatData = () => {
    // treats data contained in lastTransactionsPublic
  }

  const fetchInterval = setInterval(() => {
    fetchTransactionsPublic(10);
    // treatData();
  }, 1000 * fetchIntervalVal); // polling all relevant data

  const Wallets = [
    {
        id: "1",
        text: "1NDHh2fD29yC7pXNTcNB62RHTNJy11F5V7",
        price: "$45,123",
        '24-hChange': "-1.10%"
    },
    {
        id: "2",
        text: "1NDHh3fJ29hC6pFNGcNR62EHRNJy22E4S2",
        price: "$5,123",
        '24-hChange': "-3000$"
    },
    {
        id: "3",
        text: "1NNHh2Fd29yC7pXNTcNB62RHTNjvU11TG5",
        price: "$2,096",
        '24-hChange': "+3.04%"
    },
     
  ];

  return (
    <CustomCard borderRadius="xl">
        <Text textStyle="h2" color="black.80" >Wallets</Text>
        <Stack>
            {lastTransactionsPublic.map((wallet) => (
                <Flex p="1" key={wallet['wallet']} gap="4" w="full" >
                    
                    <Flex justify="space-between" w="full" >
                        <Stack >
                            <Text textStyle="h6" style={{ color: wallet['balance_update'].includes('+') ? 'green' : 'red' }}>
                                {wallet['wallet']}
                            </Text>
                            <Text fontSize="sm" style={{ color: wallet['balance_update'].includes('+') ? 'green' : 'red' }} >
                                {wallet['balance_update']}
                            </Text>

                        </Stack>
                        <Text textStyle="h6"  style={{ color: wallet['balance_update'].includes('+') ? 'green' : 'red' }}>
                                {wallet['current_balance']}
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

export default Wallets;
