const redis = require('redis');
const client = redis.createClient();

// Define a key prefix for user-related data in Redis
const USER_PREFIX = 'user:';

// Function to save a user in Redis
function saveUser(user) {
  // Generate a unique key for the user based on their username or ID
  const key = USER_PREFIX + user.username; // You may use a different identifier like user ID

  // Store user data in Redis as a JSON string
  client.set(key, JSON.stringify(user));
}

// Function to retrieve a user from Redis by username
function getUserByUsername(username, callback) {
  const key = USER_PREFIX + username;

  // Retrieve user data from Redis
  client.get(key, (err, data) => {
    if (err) {
      return callback(err, null);
    }

    if (data) {
      // Parse the JSON data to get the user object
      const user = JSON.parse(data);
      return callback(null, user);
    }

    return callback(null, null);
  });
}

module.exports = {
  saveUser,
  getUserByUsername,
};

