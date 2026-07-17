export type ThemePreference = 'light' | 'dark' | 'system';

export type SupportedSiteId = 'youtube' | 'netflix' | 'prime-video' | 'instagram' | 'tiktok';

export interface PageState {
  site: SupportedSiteId;
  url: string;
  videoCount: number;
  hasPausedVideo: boolean;
}

export interface ExtensionSettings {
  theme: ThemePreference;
  enabled: boolean;
}

export type ExtensionMessage =
  | { type: 'drape:page-state-updated'; pageState: PageState }
  | { type: 'drape:get-tab-state'; tabId?: number };

export interface TabStateResponse {
  pageState?: PageState;
}
