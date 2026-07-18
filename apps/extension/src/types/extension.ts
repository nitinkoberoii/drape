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

export type FrameCaptureErrorCode = 'no-paused-video' | 'frame-not-ready' | 'capture-unavailable';

export type FrameCaptureResult =
  | { success: true; dataUrl: string; capturedAt: number }
  | { success: false; code: FrameCaptureErrorCode; message: string };

export type ExtensionMessage =
  | { type: 'drape:page-state-updated'; pageState: PageState }
  | { type: 'drape:get-tab-state'; tabId: number }
  | { type: 'drape:get-page-state' }
  | { type: 'drape:capture-frame'; tabId: number };

export interface TabStateResponse {
  pageState?: PageState;
}

export interface FrameCaptureResponse {
  capture: FrameCaptureResult;
}
