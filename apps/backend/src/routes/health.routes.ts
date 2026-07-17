import type { FastifyPluginAsync } from 'fastify';
import type { ApiResponse, HealthStatus } from '@drape/shared-types';

export const healthRoutes: FastifyPluginAsync = async (app) => {
  app.get('/health', async (): Promise<ApiResponse<HealthStatus>> => ({
    data: { status: 'ok' },
  }));
};
