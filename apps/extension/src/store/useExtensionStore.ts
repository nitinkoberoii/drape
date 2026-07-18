import { create } from 'zustand';

import { defaultSettings } from '../services/settings';
import type { ExtensionSettings, FrameCaptureResult, PageState } from '../types/extension';

interface ExtensionState {
  isLoading: boolean;
  pageState?: PageState;
  capture?: FrameCaptureResult;
  settings: ExtensionSettings;
  setIsLoading: (isLoading: boolean) => void;
  setPageState: (pageState?: PageState) => void;
  setCapture: (capture?: FrameCaptureResult) => void;
  setSettings: (settings: ExtensionSettings) => void;
}

export const useExtensionStore = create<ExtensionState>((set) => ({
  isLoading: true,
  pageState: undefined,
  capture: undefined,
  settings: defaultSettings,
  setIsLoading: (isLoading) => set({ isLoading }),
  setPageState: (pageState) => set({ pageState }),
  setCapture: (capture) => set({ capture }),
  setSettings: (settings) => set({ settings }),
}));
