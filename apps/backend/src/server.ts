import { createApp } from './app.js';
import { environment } from './config/env.js';

const app = createApp();

try {
  await app.listen({ port: environment.PORT, host: environment.HOST });
} catch (error) {
  app.log.error(error, 'Unable to start server');
  process.exit(1);
}
