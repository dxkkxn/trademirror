import { Box, Button, Container, Flex, HStack, Heading, Icon, Menu, MenuButton, MenuItem, MenuList } from '@chakra-ui/react';
import React from 'react';
import {FaSignOutAlt} from "react-icons/fa";

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