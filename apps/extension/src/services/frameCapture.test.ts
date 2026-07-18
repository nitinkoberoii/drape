import { describe, expect, it, vi } from 'vitest';

import { findCapturablePausedVideo } from './frameCapture';

function video(overrides: Partial<HTMLVideoElement> = {}): HTMLVideoElement {
  return {
    paused: true,
    ended: false,
    readyState: 2,
    getBoundingClientRect: () => ({ width: 640, height: 360 }),
    ...overrides,
  } as HTMLVideoElement;
}

describe('findCapturablePausedVideo', () => {
  it('selects the largest visible paused video with frame data', () => {
    vi.stubGlobal('window', { getComputedStyle: () => ({ display: 'block', visibility: 'visible' }) });
    const smaller = video({ getBoundingClientRect: () => ({ width: 320, height: 180 } as unknown as DOMRect) });
    const larger = video({ getBoundingClientRect: () => ({ width: 1280, height: 720 } as unknown as DOMRect) });
    expect(findCapturablePausedVideo([smaller, larger])).toBe(larger);
  });

  it('ignores playing, ended, hidden, and not-yet-decoded videos', () => {
    vi.stubGlobal('window', { getComputedStyle: () => ({ display: 'none', visibility: 'visible' }) });
    expect(findCapturablePausedVideo([video(), video({ paused: false }), video({ ended: true }), video({ readyState: 1 })])).toBeUndefined();
  });
});
