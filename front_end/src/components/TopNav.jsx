import { Box, Button, Container, Flex, HStack, Heading, Icon, Menu, MenuButton, MenuItem, MenuList, Text } from '@chakra-ui/react';
import React , { useState, useEffect } from 'react';
import {FaSignOutAlt} from "react-icons/fa";

const TopNav = () => {

  const [apiStatus, setApiStatus] = useState('Loading...');
  const [dbStatus, setDbStatus] = useState('Loading...');

  const apiHost = import.meta.env.VITE_API_URL;
  console.log(apiHost)

  useEffect(() => {
    // Function to fetch API status
    const fetchApiStatus = () => {
      fetch(`${apiHost}/`)
        .then(response => response.json())
        .then(data => setApiStatus(data))
        .catch(() => setApiStatus('Error'));
    };

    // Function to fetch Database status
    const fetchDbStatus = () => {
      fetch(`${apiHost}/redis_status`)
        .then(response => response.json())
        .then(data => setDbStatus(data))
        .catch(() => setDbStatus('Error'));
    };

    // Fetch statuses initially
    fetchApiStatus();
    fetchDbStatus();

    // Set up polling
    const interval = setInterval(() => {
      fetchApiStatus();
      fetchDbStatus();
    }, 10000); // polling every 5 seconds

    console.log(apiStatus, dbStatus)

    // Cleanup function to clear the interval when the component is unmounted
    return () => clearInterval(interval);
  }, []);

  return (
   <Box>
      <HStack  boxShadow="xl" h="16" justify="space-between" px="20">
     
        <Heading fontSize="24px">Trade Mirror</Heading>

        <Text fontSize="18px">{apiStatus}</Text>
        <Text fontSize="18px">{dbStatus}</Text>

        <Menu>
          <MenuButton ><Icon as={FaSignOutAlt} fontSize="24px"/></MenuButton>
          
        </Menu>



     
      </HStack>
    </Box>
  );
};

export default TopNav;