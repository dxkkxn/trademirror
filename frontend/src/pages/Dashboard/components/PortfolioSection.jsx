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

  const withdraw = () => {
    // display dialog box
    let amount = prompt("Enter an amount : ");
    if (amount === null || isNaN(amount) || amount > balance.fiat) {
        alert("Invalid input. Please enter a valid integer lesser than your balance.");
        return null; // or you can return a default value or handle it as needed
    }

    // Parse the input as an integer
    const withdrawValue = parseInt(amount, 10);

    // posting to api
    fetch('/api/withdraw_fiat', {
      method: 'POST',
      headers: {
       'Content-Type': 'application/json',
      },
        body: JSON.stringify({"amount": withdrawValue}),
      })
      .then(response => {
         if (!response.ok) {
           throw new Error('Network response was not ok.');
         }
         else {
           return response.json();
         }
      })
      .catch(error => {
        console.error("Error withdrawing fiat");
      });
  }


  const deposit = () => {
    // display dialog box
    let amount = prompt("Enter an amount : ");
    if (amount === null || isNaN(amount)) {
        alert("Invalid input. Please enter a valid integer.");
        return null; // or you can return a default value or handle it as needed
    }

    // Parse the input as an integer
    const depositValue = parseInt(amount, 10);

    // posting to api
    fetch('/api/add_fiat', {
      method: 'POST',
      headers: {
       'Content-Type': 'application/json',
      },
        body: JSON.stringify({"amount": depositValue}),
      })
      .then(response => {
         if (!response.ok) {
           throw new Error('Network response was not ok.');
         }
         else {
           return response.json();
         }
      })
      .catch(error => {
        console.error("Error depositing fiat");
      });
  }


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
        <Text textStyle="h2" fontWeight="medium"> {balance.btc} BTC </Text>
        <Text textStyle="h2" fontWeight="medium"> {balance.fiat} $ </Text>
      </HStack>
    )}
    </Stack>
    </HStack>


    <HStack pr="6">
    <Button leftIcon={<Icon as={AiOutlineArrowDown} />} onClick={()=>deposit()}>Deposit</Button>
    <Button leftIcon={<Icon as={AiOutlineArrowUp} />}onClick = {() => withdraw()} >Withdraw</Button>
    </HStack>
    </HStack>
  );
};

export default PortfolioSection;

