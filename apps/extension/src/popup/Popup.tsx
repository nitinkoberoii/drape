import { useEffect } from 'react';

import { getSettings, saveSettings } from '../services/settings';
import { getSupportedSite } from '../sites/supportedSites';
import { useExtensionStore } from '../store/useExtensionStore';
import type { ThemePreference } from '../types/extension';

async function getActiveTab(): Promise<chrome.tabs.Tab | undefined> {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

export function Popup() {
  const { isLoading, pageState, settings, setIsLoading, setPageState, setSettings } = useExtensionStore();

  useEffect(() => {
    async function loadPopup(): Promise<void> {
      try {
        const [storedSettings, activeTab] = await Promise.all([getSettings(), getActiveTab()]);
        setSettings(storedSettings);
        if (!activeTab?.url || activeTab.id === undefined || !getSupportedSite(activeTab.url)) {
          setPageState(undefined);
          return;
        }
        const response = await chrome.runtime.sendMessage({ type: 'drape:get-tab-state', tabId: activeTab.id });
        setPageState(response.pageState);
      } finally {
        setIsLoading(false);
      }
    }
    void loadPopup();
  }, [setIsLoading, setPageState, setSettings]);

  async function updateTheme(theme: ThemePreference): Promise<void> {
    const updatedSettings = { ...settings, theme };
    setSettings(updatedSettings);
    await saveSettings(updatedSettings);
  }

  async function updateEnabled(enabled: boolean): Promise<void> {
    const updatedSettings = { ...settings, enabled };
    setSettings(updatedSettings);
    await saveSettings(updatedSettings);
  }

  const supportedSite = pageState ? getSupportedSite(pageState.url) : undefined;
  const videoCount = pageState?.videoCount ?? 0;
  const hasPausedVideo = pageState?.hasPausedVideo ?? false;
  const status = isLoading
    ? 'Checking this page…'
    : !settings.enabled
      ? 'Drape is turned off'
      : !supportedSite
        ? 'Open a supported video site to get started'
        : videoCount === 0
          ? `No video found on ${supportedSite.label}`
          : hasPausedVideo
            ? 'A paused video is ready for capture'
            : 'Pause a video to prepare a capture';

  return (
    <main className={`popup theme-${settings.theme}`}>
      <header>
        <div>
          <h1>Drape</h1>
          <p>Find fashion from video.</p>
        </div>
        <label className="switch-label">
          <span>Enabled</span>
          <input checked={settings.enabled} onChange={(event) => void updateEnabled(event.target.checked)} type="checkbox" />
        </label>
      </header>

      <section aria-live="polite" className="status-card">
        <strong>{supportedSite?.label ?? 'Video site detection'}</strong>
        <p>{status}</p>
      </section>

      <label className="setting-label" htmlFor="theme-preference">Appearance</label>
      <select id="theme-preference" onChange={(event) => void updateTheme(event.target.value as ThemePreference)} value={settings.theme}>
        <option value="system">System</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
      <p className="supported-sites">Supported: YouTube, Netflix, Prime Video, Instagram, and TikTok.</p>
    </main>
  );
}
