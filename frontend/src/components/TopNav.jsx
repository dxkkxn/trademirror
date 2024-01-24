import { Box, Button, Container, Flex, HStack, Heading, Icon, Menu, MenuButton, MenuItem, MenuList, Text } from '@chakra-ui/react';
import React , { useState, useEffect } from 'react';
import {FaSignOutAlt} from "react-icons/fa";

const dbStatusIntervalVal = 10

const TopNav = () => {

  return (
   <Box>
      <HStack  boxShadow="xl" h="16" justify="space-between" px="20">
     
        <Heading fontSize="24px">Trade Mirror</Heading>

        <Menu>
          <MenuButton ><Icon as={FaSignOutAlt} fontSize="24px"/></MenuButton>
          
        </Menu>



     
      </HStack>
    </Box>
  );
};


export default TopNav;
