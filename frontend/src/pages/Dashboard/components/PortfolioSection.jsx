import { Button, HStack, Icon, Stack, Tag, Text } from "@chakra-ui/react";
import React, {useState, useEffect} from 'react';
import {
  AiOutlineInfoCircle,
  AiOutlineArrowDown,
  AiOutlineArrowUp,
} from "react-icons/ai";



const PortfolioSection = () => {

  const fetchIntervalVal = 3
  const [balance, setBalance] = useState({})

  // Function to fetch last n transactions
  const fetchBalance = () => {
    fetch('/api/user_balance')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok.');
        }
        return response.json();
      })
      .then(data => {
        const dict = JSON.parse(data);
        console.log(data);
        setBalance(dict);
      })
      .catch(error => {
        console.error('Error fetching balance:', error);
      });
  };

  useEffect(() => {
    const fetchInterval = setInterval(() => {
      fetchBalance();
    }, 1000 * fetchIntervalVal);
    fetchBalance();
    return () => {
      clearInterval(fetchInterval);
    };
    // polling all relevant data
  }, []);


  return (
    <HStack
    justify="space-between"
    bg="white"
    borderRadius="xl"
    p="5" m="6"
    align={{
      base: "flex-start",
        xl: "center",
    }}
    flexDir={{
      base: "column",
        xl: "row",
    }}
    spacing={{
      base: 4,
        xl: 0,
    }}
    >
    <HStack pl="6" 
    spacing={{
      base: 0,
        xl: 16,
    }}
    align={{
      base: "flex-start",
        xl: "center",
    }}
    flexDir={{
      base: "column",
        xl: "row",
    }}
    >
    <Stack>
    <HStack color="black.80">
    <Text fontSize="sm" fontWeight="medium">Your Wallet Balance</Text>
    </HStack>
    {balance == null ? (
      <Text textStyle="h2" fontWeight="medium"> Internal Server Error </Text>
    ) : (
      <HStack>
        <Text textStyle="h2" fontWeight="medium"> $ {balance.btc} BTC </Text>
        <Text textStyle="h2" fontWeight="medium"> $ {balance.fiat} $ </Text>
      </HStack>
    )}
    </Stack>
    </HStack>


    <HStack pr="6">
    <Button leftIcon={<Icon as={AiOutlineArrowDown} />}>Deposit</Button>
    <Button leftIcon={<Icon as={AiOutlineArrowUp} />}>Withdraw</Button>
    </HStack>
    </HStack>
  );
};

export default PortfolioSection;

