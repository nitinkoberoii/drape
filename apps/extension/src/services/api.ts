interface ExtensionEnvironment {
  PLASMO_PUBLIC_API_BASE_URL?: string;
}

const apiBaseUrl = (globalThis as typeof globalThis & { process?: { env?: ExtensionEnvironment } })
  .process?.env?.PLASMO_PUBLIC_API_BASE_URL;

export function getApiBaseUrl(): string | undefined {
  return apiBaseUrl;
}
