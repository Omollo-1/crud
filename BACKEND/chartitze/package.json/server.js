// chartitze/server.js or app.js
const express = require('express');
const cors = require('cors');
const app = express();

// Middleware
app.use(cors());  // Enable Cross-Origin Requests
app.use(express.json());  // Parse JSON bodies

// Test route
app.get('/api/health', (req, res) => {
  res.json({ status: 'Backend is running!' });
});

// Your actual API routes
app.get('/api/data', (req, res) => {
  // Your chart data logic here
  res.json({ data: [1, 2, 3, 4, 5] });
});

// Start server
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`chartitze backend running on http://localhost:${PORT}`);
});