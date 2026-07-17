import { create } from 'zustand';

interface ExtensionState {
  isReady: boolean;
  setReady: (isReady: boolean) => void;
}

export const useExtensionStore = create<ExtensionState>((set) => ({
  isReady: false,
  setReady: (isReady) => set({ isReady }),
}));
