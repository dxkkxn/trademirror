import React from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';

const Wallets = () => {
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
        '24-hChange': "+0.34%"
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
            {Wallets.map((wallet) => (
                <Flex p="1" key={wallet.id} gap="4" w="full" >
                    
                    <Flex justify="space-between" w="full" >
                        <Stack >
                            <Text textStyle="h6" style={{ color: wallet.id <2 || wallet.id == 3 ? 'green' : 'black' }}>
                                {wallet.text}
                            </Text>
                            <Text fontSize="sm" style={{ color: wallet['24-hChange'].includes('+') ? 'green' : 'red' }} >
                                {wallet['24-hChange']}
                            </Text>

                        </Stack>
                        <Text textStyle="h6"  style={{ color: wallet.id <2 || wallet.id == 3  ? 'green' : 'black' }}>
                                {wallet.price}
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