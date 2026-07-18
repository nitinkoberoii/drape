import { createRemoteJWKSet, jwtVerify } from 'jose';
import type { FastifyRequest } from 'fastify';

import { environment } from '../config/env.js';
import { ApiError } from '../errors/api-error.js';

export interface AuthenticatedUser {
  id: string;
  email?: string;
}

let jwks: ReturnType<typeof createRemoteJWKSet> | undefined;

function getJwks(): ReturnType<typeof createRemoteJWKSet> {
  if (!environment.SUPABASE_URL)
    throw new ApiError(
      503,
      'AUTH_NOT_CONFIGURED',
      'Authentication is not configured on this server.',
    );
  jwks ??= createRemoteJWKSet(new URL('/auth/v1/.well-known/jwks.json', environment.SUPABASE_URL));
  return jwks;
}

/** Verifies a Supabase access token and returns the minimal user identity needed by API routes. */
export async function authenticate(request: FastifyRequest): Promise<AuthenticatedUser> {
  const authorization = request.headers.authorization;
  if (!authorization?.startsWith('Bearer '))
    throw new ApiError(401, 'UNAUTHENTICATED', 'A bearer access token is required.');

  try {
    const { payload } = await jwtVerify(authorization.slice('Bearer '.length), getJwks(), {
      issuer: `${environment.SUPABASE_URL}/auth/v1`,
      audience: environment.SUPABASE_JWT_AUDIENCE,
    });
    if (typeof payload.sub !== 'string' || payload.sub.length === 0)
      throw new ApiError(401, 'UNAUTHENTICATED', 'The access token has no user identity.');
    return {
      id: payload.sub,
      email: typeof payload.email === 'string' ? payload.email : undefined,
    };
  } catch (error) {
    if (error instanceof ApiError) throw error;
    request.log.warn({ err: error }, 'Rejected invalid access token');
    throw new ApiError(401, 'UNAUTHENTICATED', 'The access token is invalid or expired.');
  }
}
