import type { ExtensionMessage, PageState, TabStateResponse } from '../types/extension';

const pageStates = new Map<number, PageState>();

chrome.runtime.onMessage.addListener(
  (message: ExtensionMessage, sender, sendResponse: (response: TabStateResponse) => void) => {
    if (message.type === 'drape:page-state-updated' && sender.tab?.id !== undefined) {
      pageStates.set(sender.tab.id, message.pageState);
      return;
    }

    if (message.type === 'drape:get-tab-state') {
      const tabId = message.tabId ?? sender.tab?.id;
      sendResponse({ pageState: tabId === undefined ? undefined : pageStates.get(tabId) });
    }
  },
);

chrome.tabs.onRemoved.addListener((tabId) => {
  pageStates.delete(tabId);
});
