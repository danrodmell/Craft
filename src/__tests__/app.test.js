const request = require('supertest');
const app = require('../app');

describe('App Endpoints', () => {
  describe('GET /', () => {
    it('should return welcome message', async () => {
      const res = await request(app).get('/');
      expect(res.statusCode).toBe(200);
      expect(res.body).toHaveProperty('message', 'Welcome to Craft API');
    });
  });

  describe('GET /api/health', () => {
    it('should return health status', async () => {
      const res = await request(app).get('/api/health');
      expect(res.statusCode).toBe(200);
      expect(res.body).toHaveProperty('status', 'OK');
      expect(res.body).toHaveProperty('timestamp');
    });
  });

  describe('GET /api/version', () => {
    it('should return version information', async () => {
      const res = await request(app).get('/api/version');
      expect(res.statusCode).toBe(200);
      expect(res.body).toHaveProperty('version');
    });
  });

  describe('Error Handling', () => {
    it('should return 404 for non-existent routes', async () => {
      const res = await request(app).get('/non-existent-route');
      expect(res.statusCode).toBe(404);
    });
  });
}); 