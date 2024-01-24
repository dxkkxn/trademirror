import React , { useState, useEffect } from 'react';
import { CustomCard } from '../../../chakra/CustomCard';
import { Box, Button, Flex, Grid, HStack, Stack, Text } from '@chakra-ui/react';

const Following = ({ followedList }) => {

  const unfollow = (wallet_hash) => {
    fetch('/api/unfollow_wallet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({"wallet_id": wallet_hash}),
      })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
          else {
            return response.json();
          }
        })
        // .then(() => updateFollowedList())
        .catch(error => {
            console.error('Error following wallets:', error);
        });
    }

return (
            <CustomCard borderRadius="xl">
                <Text textStyle="h2" color="black.80">Followed Wallets </Text>
                  {followedList.length === 0 ? (
                    <Text textStyle = "h6">
                      Your are not currently following any wallet
                    </Text>
                ) : (
                  <Stack>
                  {followedList.map((item, index) => (
                            <Flex p="1" key={index} gap="4" w="full">
 
                              <Flex justify="space-between" w="full" >
                                  <Stack >
                                      <Text textStyle="h6">
                                          <b>{item}</b>
                                      </Text>
                                        <Button onClick={()=>unfollow(item)} w="full" mt="6" colorScheme="red">
                                          Unfollow
                                        </Button> 

                                  </Stack>
                              </Flex>
                               
                            </Flex>
                        ))}
                    </Stack>
                )}
            </CustomCard>
        );
    };

export default Following;
