import type { PlasmoCSConfig } from 'plasmo';

import { getSupportedSite } from '../sites/supportedSites';
import type { PageState } from '../types/extension';

export const config: PlasmoCSConfig = {
  matches: [
    '*://*.youtube.com/*', '*://youtu.be/*', '*://*.netflix.com/*', '*://*.primevideo.com/*', '*://*.instagram.com/*', '*://*.tiktok.com/*',
  ],
  run_at: 'document_idle',
};

function readPageState(): PageState | undefined {
  const supportedSite = getSupportedSite(window.location.href);
  if (!supportedSite) return undefined;

  const videos = Array.from(document.querySelectorAll('video'));
  return {
    site: supportedSite.id,
    url: window.location.href,
    videoCount: videos.length,
    hasPausedVideo: videos.some((video) => video.paused && !video.ended),
  };
}

function reportPageState(): void {
  const pageState = readPageState();
  if (pageState) void chrome.runtime.sendMessage({ type: 'drape:page-state-updated', pageState });
}

document.addEventListener('pause', reportPageState, true);
document.addEventListener('play', reportPageState, true);
new MutationObserver(reportPageState).observe(document.documentElement, { childList: true, subtree: true });
chrome.runtime.onMessage.addListener((message: { type?: string }, _sender, sendResponse) => {
  if (message.type === 'drape:get-page-state') sendResponse(readPageState());
});
reportPageState();
