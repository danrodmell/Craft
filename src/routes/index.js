const express = require('express');
const router = express.Router();

// Example routes
router.get('/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

router.get('/version', (req, res) => {
  res.json({ version: process.env.npm_package_version || '1.0.0' });
});

module.exports = router; 