import type { ApiResponse } from '@drape/shared-types';
import type { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';

import { ApiError } from '../errors/api-error.js';
import { authenticate } from '../plugins/authentication.js';

const frameSubmissionSchema = z
  .object({
    imageDataUrl: z
      .string()
      .regex(/^data:image\/(jpeg|png);base64,/)
      .max(8_000_000),
    sourceUrl: z.string().url().max(2_048),
    capturedAt: z.number().int().positive(),
  })
  .strict();

interface FrameReceipt {
  requestId: string;
  status: 'received';
}

/** Accepts a validated frame contract; AI processing and persistence begin in Phase 4. */
export const frameRoutes: FastifyPluginAsync = async (app) => {
  app.post('/frames', async (request, reply): Promise<ApiResponse<FrameReceipt>> => {
    await authenticate(request);
    const parsed = frameSubmissionSchema.safeParse(request.body);
    if (!parsed.success)
      throw new ApiError(400, 'VALIDATION_ERROR', 'The frame submission is invalid.');

    request.log.info(
      { requestId: request.id, sourceHost: new URL(parsed.data.sourceUrl).host },
      'Frame received',
    );
    return reply.code(202).send({ data: { requestId: request.id, status: 'received' } });
  });
};
