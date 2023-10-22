const {createClient} = require("redis")
require("dotenv").config() // access env variables

const redisClient = createClient({ // config client
  url: process.env.REDIS_URL,
  socket: {
    tls: true,
    servername: process.env.REDIS_HOST,
  },
})
(async ()=> {
  // connect to server
  await redisClient.connect()
})()

(async(user, mdp)=> {

