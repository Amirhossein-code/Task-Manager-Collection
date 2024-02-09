// api.js

import axios from 'axios';

// Define your base URL
const baseURL = 'http://127.0.0.1:8000';

const getToken = async (username, password) => {
  try {
    // Make a POST request to the Djoser /auth/jwt/create endpoint
    const response = await axios.post(`${baseURL}/auth/jwt/create`, {
      username,
      password,
    });

    // Assuming Djoser returns the token in the 'access' key of the response data
    const token = response.data.access;
    return token;
  } catch (error) {
    // Handle authentication failure (e.g., return an error message)
    throw error.response ? error.response.data : error.message;
  }
};

export { getToken };
