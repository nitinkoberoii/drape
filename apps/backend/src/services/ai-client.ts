import { z } from 'zod';

import { environment } from '../config/env.js';
import { ApiError } from '../errors/api-error.js';

const analysisResponseSchema = z.object({
  items: z.array(
    z.object({
      label: z.string(),
      confidence: z.number().min(0).max(1),
      bounding_box: z.object({
        left: z.number().int().nonnegative(),
        top: z.number().int().nonnegative(),
        width: z.number().int().positive(),
        height: z.number().int().positive(),
      }),
      mask: z.object({
        encoding: z.literal('rle'),
        size: z.tuple([z.number().int().positive(), z.number().int().positive()]),
        counts: z.array(z.number().int().positive()),
      }),
    }),
  ),
});

export type DetectedClothingItem = z.infer<typeof analysisResponseSchema>['items'][number];

/** Calls the stateless AI service and rejects malformed or unavailable upstream responses. */
export async function analyzeFrame(input: {
  imageDataUrl: string;
  sourceUrl: string;
}): Promise<DetectedClothingItem[]> {
  let response: Response;
  try {
    response = await fetch(`${environment.AI_SERVICE_URL}/analyze`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ image_data_url: input.imageDataUrl, source_url: input.sourceUrl }),
      signal: AbortSignal.timeout(30_000),
    });
  } catch {
    throw new ApiError(503, 'AI_SERVICE_UNAVAILABLE', 'Image analysis is temporarily unavailable.');
  }

  if (!response.ok)
    throw new ApiError(503, 'AI_SERVICE_UNAVAILABLE', 'Image analysis is temporarily unavailable.');

  let body: unknown;
  try {
    body = await response.json();
  } catch {
    throw new ApiError(502, 'AI_SERVICE_INVALID_RESPONSE', 'Image analysis returned an invalid response.');
  }
  const parsed = analysisResponseSchema.safeParse(body);
  if (!parsed.success)
    throw new ApiError(502, 'AI_SERVICE_INVALID_RESPONSE', 'Image analysis returned an invalid response.');
  return parsed.data.items;
}
