import cors from '@fastify/cors';
import Fastify from 'fastify';
import { healthRoutes } from './routes/health.routes.js';

export function createApp() {
  const app = Fastify({ logger: true });

  void app.register(cors, { origin: false });
  void app.register(healthRoutes, { prefix: '/api/v1' });

  return app;
}
