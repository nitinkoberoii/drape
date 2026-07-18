import cors from '@fastify/cors';
import Fastify, { type FastifyError } from 'fastify';
import { environment } from './config/env.js';
import { ApiError } from './errors/api-error.js';
import { frameRoutes } from './routes/frame.routes.js';
import { healthRoutes } from './routes/health.routes.js';

export function createApp() {
  const app = Fastify({
    logger: { level: environment.LOG_LEVEL, redact: ['req.headers.authorization'] },
    requestIdHeader: 'x-request-id',
  });

  void app.register(cors, { origin: environment.CORS_ALLOWED_ORIGINS });
  void app.register(healthRoutes, { prefix: '/api/v1' });
  void app.register(frameRoutes, { prefix: '/api/v1' });
  app.addHook('onSend', async (request, reply) => {
    reply.header('x-request-id', request.id);
  });
  app.setErrorHandler((error: FastifyError | ApiError, request, reply) => {
    const apiError =
      error instanceof ApiError
        ? error
        : new ApiError(500, 'INTERNAL_ERROR', 'An unexpected error occurred.');
    if (!(error instanceof ApiError)) request.log.error({ err: error }, 'Unhandled request error');
    return reply
      .code(apiError.statusCode)
      .send({ error: { code: apiError.code, message: apiError.message } });
  });

  return app;
}
