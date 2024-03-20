const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware to parse JSON bodies
app.use(bodyParser.json());

// Dummy database to store user data
let users = [];

// Route to handle user signup
app.post('/signup', (req, res) => {
  const { username, email, password } = req.body;

  // Check if required fields are provided
  if (!username || !email || !password) {
    return res.status(400).json({ error: 'Please provide username, email, and password' });
  }

  // Check if user with provided email already exists
  const existingUser = users.find(user => user.email === email);
  if (existingUser) {
    return res.status(400).json({ error: 'User with this email already exists' });
  }

  // Create new user object
  const newUser = {
    username,
    email,
    password // Note: You should hash the password before storing it in a real-world application
  };

  // Store the new user in the database
  users.push(newUser);

  // Respond with success message
  res.status(201).json({ message: 'User signed up successfully', user: newUser });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
