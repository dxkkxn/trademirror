import React from 'react';
import TopNav from '../../components/TopNav';
import { Box, Flex, Grid, GridItem } from '@chakra-ui/react';
import Portfoliosection from './components/PortfolioSection';
import HistorySection from './components/HistorySection';
import Wallets from './components/Wallets';

const Dashboard = () => {
  return (
    <div>
        <Flex>
            <Box flexGrow={1}>
              <TopNav/>
              
            </Box>        
        </Flex>
        <Portfoliosection/>
        <Grid gridTemplateColumns={{
            base: "repeat(1, 1fr)",
            md: "repeat(2, 1fr)",
        }} gap="6" m="6">
        
           
    
        <GridItem colSpan={1}>
           <HistorySection />
        </GridItem>
        <GridItem colSpan={1}>
            <Wallets />
        </GridItem>
        
        </Grid>
        
     
    </div>
  );
};

export default Dashboard;
