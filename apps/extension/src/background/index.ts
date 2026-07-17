import type { ExtensionMessage, PageState, TabStateResponse } from '../types/extension';

const pageStates = new Map<number, PageState>();

chrome.runtime.onMessage.addListener(
  (message: ExtensionMessage, sender, sendResponse: (response: TabStateResponse) => void) => {
    if (message.type === 'drape:page-state-updated' && sender.tab?.id !== undefined) {
      pageStates.set(sender.tab.id, message.pageState);
      return;
    }

    if (message.type === 'drape:get-tab-state') {
      const cachedPageState = pageStates.get(message.tabId);
      if (cachedPageState) {
        sendResponse({ pageState: cachedPageState });
        return;
      }

      void chrome.tabs
        .sendMessage(message.tabId, { type: 'drape:get-page-state' })
        .then((pageState: PageState | undefined) => {
          if (pageState) pageStates.set(message.tabId, pageState);
          sendResponse({ pageState });
        })
        .catch(() => sendResponse({}));
      return true;
    }
  },
);

chrome.tabs.onRemoved.addListener((tabId) => {
  pageStates.delete(tabId);
});
