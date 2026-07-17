import { create } from 'zustand';

import { defaultSettings } from '../services/settings';
import type { ExtensionSettings, PageState } from '../types/extension';

interface ExtensionState {
  isLoading: boolean;
  pageState?: PageState;
  settings: ExtensionSettings;
  setIsLoading: (isLoading: boolean) => void;
  setPageState: (pageState?: PageState) => void;
  setSettings: (settings: ExtensionSettings) => void;
}

export const useExtensionStore = create<ExtensionState>((set) => ({
  isLoading: true,
  pageState: undefined,
  settings: defaultSettings,
  setIsLoading: (isLoading) => set({ isLoading }),
  setPageState: (pageState) => set({ pageState }),
  setSettings: (settings) => set({ settings }),
}));
