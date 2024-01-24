import React, {useState, useEffect} from 'react';
import TopNav from '../../components/TopNav';
import { Box, Flex, Grid, GridItem } from '@chakra-ui/react';
import Portfoliosection from './components/PortfolioSection';
import HistorySection from './components/HistorySection';
import Wallets from './components/Wallets';
import Following from './components/Following.jsx';

const Dashboard = () => {

  const [followedList, setFollowedList] = useState([]);

  const handleChildUpdate = (newValue) => {
    setFollowedList(newValue);
  }

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
        
           
    
        <GridItem colSpan={2}>
          <HistorySection />
        </GridItem>
        <GridItem colSpan={2}>
          <Wallets onUpdate = {handleChildUpdate}/>
        </GridItem>
        <GridItem colSpan={2}>
          <Following followedList={followedList} />
        </GridItem>
        
        </Grid>
        
     
    </div>
  );
};

export default Dashboard;
