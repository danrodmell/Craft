import express from 'express';
import dotenv from 'dotenv';
import axios from 'axios';

// Load environment variables
dotenv.config();

const app = express();
const port = process.env.PORT || 3000;
const pythonServiceUrl = process.env.PYTHON_SERVICE_URL || 'http://localhost:5000';

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ status: 'error', message: 'Something went wrong!' });
});

// Basic route
app.get('/', (req, res) => {
  res.json({ status: 'ok', message: 'Welcome to Craft API' });
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'node-api',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    memoryUsage: process.memoryUsage()
  });
});

// MCP Context endpoint
app.post('/api/mcp/context', async (req, res, next) => {
  try {
    const response = await axios.post(`${pythonServiceUrl}/mcp/context`, req.body);
    res.json(response.data);
  } catch (error) {
    console.error('Error communicating with MCP service:', error.message);
    next(error);
  }
});

// Handle 404
app.use((req, res) => {
  res.status(404).json({ status: 'error', message: 'Route not found' });
});

// Start server
const server = app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
  console.log(`Python MCP service URL: ${pythonServiceUrl}`);
});

// Handle graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM signal received: closing HTTP server');
  server.close(() => {
    console.log('HTTP server closed');
    process.exit(0);
  });
}); 