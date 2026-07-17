import type { SupportedSiteId } from '../types/extension';

interface SupportedSite {
  id: SupportedSiteId;
  label: string;
  hosts: readonly string[];
}

export const supportedSites: readonly SupportedSite[] = [
  { id: 'youtube', label: 'YouTube', hosts: ['youtube.com', 'youtu.be'] },
  { id: 'netflix', label: 'Netflix', hosts: ['netflix.com'] },
  { id: 'prime-video', label: 'Prime Video', hosts: ['primevideo.com'] },
  { id: 'instagram', label: 'Instagram', hosts: ['instagram.com'] },
  { id: 'tiktok', label: 'TikTok', hosts: ['tiktok.com'] },
];

function matchesHost(hostname: string, supportedHost: string): boolean {
  return hostname === supportedHost || hostname.endsWith(`.${supportedHost}`);
}

export function getSupportedSite(url: string): SupportedSite | undefined {
  try {
    const hostname = new URL(url).hostname.toLowerCase();
    return supportedSites.find((site) => site.hosts.some((host) => matchesHost(hostname, host)));
  } catch {
    return undefined;
  }
}

export function isSupportedUrl(url: string): boolean {
  return getSupportedSite(url) !== undefined;
}
