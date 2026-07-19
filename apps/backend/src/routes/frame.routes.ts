import type { ApiResponse } from '@drape/shared-types';
import type { FastifyPluginAsync } from 'fastify';
import { z } from 'zod';

import { ApiError } from '../errors/api-error.js';
import { authenticate } from '../plugins/authentication.js';
import { analyzeFrame, type DetectedClothingItem } from '../services/ai-client.js';

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

interface FrameAnalysis {
  requestId: string;
  status: 'analyzed';
  items: DetectedClothingItem[];
}

/** Validates a captured frame and returns its detected, segmented clothing items. */
export const frameRoutes: FastifyPluginAsync = async (app) => {
  app.post('/frames', async (request, reply): Promise<ApiResponse<FrameAnalysis>> => {
    await authenticate(request);
    const parsed = frameSubmissionSchema.safeParse(request.body);
    if (!parsed.success)
      throw new ApiError(400, 'VALIDATION_ERROR', 'The frame submission is invalid.');

    const items = await analyzeFrame(parsed.data);
    request.log.info({ requestId: request.id, itemCount: items.length }, 'Frame analyzed');
    return reply.code(200).send({ data: { requestId: request.id, status: 'analyzed', items } });
  });
};
