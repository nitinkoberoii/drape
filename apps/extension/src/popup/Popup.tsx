import { useEffect, useState } from 'react';

import { checkBackendConnection, type BackendConnection } from '../services/api';
import { getSettings, saveSettings } from '../services/settings';
import { getSupportedSite } from '../sites/supportedSites';
import { useExtensionStore } from '../store/useExtensionStore';
import type { FrameCaptureResponse, ThemePreference } from '../types/extension';

async function getActiveTab(): Promise<chrome.tabs.Tab | undefined> {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

export function Popup() {
  const {
    capture,
    isLoading,
    pageState,
    settings,
    setCapture,
    setIsLoading,
    setPageState,
    setSettings,
  } = useExtensionStore();
  const [backendConnection, setBackendConnection] = useState<BackendConnection>('not-configured');

  useEffect(() => {
    async function loadPopup(): Promise<void> {
      try {
        const [storedSettings, activeTab, connection] = await Promise.all([
          getSettings(),
          getActiveTab(),
          checkBackendConnection(),
        ]);
        setSettings(storedSettings);
        setBackendConnection(connection);
        if (!activeTab?.url || activeTab.id === undefined || !getSupportedSite(activeTab.url)) {
          setPageState(undefined);
          return;
        }
        const response = await chrome.runtime.sendMessage({
          type: 'drape:get-tab-state',
          tabId: activeTab.id,
        });
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

  async function captureFrame(): Promise<void> {
    const activeTab = await getActiveTab();
    if (activeTab?.id === undefined) return;

    setCapture(undefined);
    try {
      const response = (await chrome.runtime.sendMessage({
        type: 'drape:capture-frame',
        tabId: activeTab.id,
      })) as FrameCaptureResponse;
      setCapture(response.capture);
    } catch {
      setCapture({
        success: false,
        code: 'capture-unavailable',
        message: 'Drape could not start frame capture. Please try again.',
      });
    }
  }

  const supportedSite = pageState ? getSupportedSite(pageState.url) : undefined;
  const videoCount = pageState?.videoCount ?? 0;
  const hasPausedVideo = pageState?.hasPausedVideo ?? false;
  const canCapture = settings.enabled && Boolean(supportedSite) && hasPausedVideo;
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
          <input
            checked={settings.enabled}
            onChange={(event) => void updateEnabled(event.target.checked)}
            type="checkbox"
          />
        </label>
      </header>

      <section aria-live="polite" className="status-card">
        <strong>{supportedSite?.label ?? 'Video site detection'}</strong>
        <p>{status}</p>
      </section>
      <p className="backend-status" role="status">
        Backend:{' '}
        {backendConnection === 'connected'
          ? 'connected'
          : backendConnection === 'unavailable'
            ? 'unavailable'
            : 'not configured'}
      </p>

      <button
        className="capture-button"
        disabled={!canCapture}
        onClick={() => void captureFrame()}
        type="button"
      >
        Capture frame
      </button>

      {capture?.success ? (
        <section className="capture-preview">
          <strong>Captured frame</strong>
          <img alt="Captured video frame" src={capture.dataUrl} />
        </section>
      ) : null}
      {capture && !capture.success ? (
        <p className="capture-error" role="alert">
          {capture.message}
        </p>
      ) : null}

      <label className="setting-label" htmlFor="theme-preference">
        Appearance
      </label>
      <select
        id="theme-preference"
        onChange={(event) => void updateTheme(event.target.value as ThemePreference)}
        value={settings.theme}
      >
        <option value="system">System</option>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
      <p className="supported-sites">
        Supported: YouTube, Netflix, Prime Video, Instagram, and TikTok.
      </p>
    </main>
  );
}
