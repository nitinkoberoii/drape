import 'dotenv/config';
import { z } from 'zod';

const environmentSchema = z.object({
  PORT: z.coerce.number().int().positive().default(3001),
  HOST: z.string().default('0.0.0.0'),
  AI_SERVICE_URL: z.string().url().default('http://localhost:8000'),
});

export const environment = environmentSchema.parse(process.env);
