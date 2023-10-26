import { Button, HStack, Icon, Stack, Tag, Text } from "@chakra-ui/react";
import React from "react";
import {
  AiOutlineInfoCircle,
  AiOutlineArrowDown,
  AiOutlineArrowUp,
} from "react-icons/ai";
const PortfolioSection = () => {
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
    <Text fontSize="sm" fontWeight="medium">Your Portfolio Balance</Text>
</HStack>
<Text textStyle="h2" fontWeight="medium"> $ 1,020,000</Text>
</Stack>



        
          <Stack pl="20">
          <HStack color="black.80">
             <Text fontSize="sm" fontWeight="medium">Your Wallet ballance </Text>
          </HStack>
                 <Text textStyle="h2" fontWeight="medium"> $ 1,000,000</Text>
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

