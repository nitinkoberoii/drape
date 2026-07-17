import type { ExtensionSettings } from '../types/extension';

const settingsKey = 'drape:settings';

export const defaultSettings: ExtensionSettings = {
  theme: 'system',
  enabled: true,
};

export async function getSettings(): Promise<ExtensionSettings> {
  const stored = await chrome.storage.sync.get(settingsKey);
  const settings = stored[settingsKey] as Partial<ExtensionSettings> | undefined;

  return { ...defaultSettings, ...settings };
}

export async function saveSettings(settings: ExtensionSettings): Promise<void> {
  await chrome.storage.sync.set({ [settingsKey]: settings });
}
