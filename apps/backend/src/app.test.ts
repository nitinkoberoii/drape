import assert from 'node:assert/strict';
import test from 'node:test';

import { createApp } from './app.js';

test('health endpoint returns the standard response envelope', async () => {
  const app = createApp();
  const response = await app.inject({ method: 'GET', url: '/api/v1/health' });
  assert.equal(response.statusCode, 200);
  assert.deepEqual(response.json(), { data: { status: 'ok' } });
  assert.ok(response.headers['x-request-id']);
  await app.close();
});

test('frame submission requires a bearer token', async () => {
  const app = createApp();
  const response = await app.inject({ method: 'POST', url: '/api/v1/frames', payload: {} });
  assert.equal(response.statusCode, 401);
  assert.deepEqual(response.json(), {
    error: { code: 'UNAUTHENTICATED', message: 'A bearer access token is required.' },
  });
  await app.close();
});
