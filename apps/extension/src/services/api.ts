interface ExtensionEnvironment {
  PLASMO_PUBLIC_API_BASE_URL?: string;
}

const apiBaseUrl = (globalThis as typeof globalThis & { process?: { env?: ExtensionEnvironment } })
  .process?.env?.PLASMO_PUBLIC_API_BASE_URL;

export function getApiBaseUrl(): string | undefined {
  return apiBaseUrl;
}

export type BackendConnection = 'connected' | 'unavailable' | 'not-configured';

/** Checks the public API health endpoint without sending captured image data. */
export async function checkBackendConnection(): Promise<BackendConnection> {
  if (!apiBaseUrl) return 'not-configured';
  try {
    const response = await fetch(`${apiBaseUrl.replace(/\/$/, '')}/health`);
    if (!response.ok) return 'unavailable';
    const body: unknown = await response.json();
    return isHealthyResponse(body) ? 'connected' : 'unavailable';
  } catch {
    return 'unavailable';
  }
}

function isHealthyResponse(body: unknown): body is { data: { status: 'ok' } } {
  return (
    typeof body === 'object' &&
    body !== null &&
    'data' in body &&
    (body as { data?: { status?: unknown } }).data?.status === 'ok'
  );
}
