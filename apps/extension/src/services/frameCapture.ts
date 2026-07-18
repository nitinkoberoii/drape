import type { FrameCaptureResult } from '../types/extension';

const jpegQuality = 0.9;
const currentDataReadyState = 2;

function isVisible(video: HTMLVideoElement): boolean {
  const bounds = video.getBoundingClientRect();
  const style = window.getComputedStyle(video);
  return bounds.width > 0 && bounds.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
}

/** Returns the largest visible, paused video that has a decoded frame available. */
export function findCapturablePausedVideo(videos: readonly HTMLVideoElement[]): HTMLVideoElement | undefined {
  return videos
    .filter((video) => video.paused && !video.ended && video.readyState >= currentDataReadyState && isVisible(video))
    .sort((first, second) => {
      const firstBounds = first.getBoundingClientRect();
      const secondBounds = second.getBoundingClientRect();
      return secondBounds.width * secondBounds.height - firstBounds.width * firstBounds.height;
    })[0];
}

/** Captures the selected video frame as a JPEG data URL for local popup preview. */
export function capturePausedVideoFrame(videos: readonly HTMLVideoElement[]): FrameCaptureResult {
  const video = findCapturablePausedVideo(videos);
  if (!video) return { success: false, code: 'no-paused-video', message: 'Pause a visible video with a loaded frame before capturing.' };
  if (video.videoWidth === 0 || video.videoHeight === 0) {
    return { success: false, code: 'frame-not-ready', message: 'The video frame is not ready yet. Wait a moment and try again.' };
  }

  try {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    if (!context) return { success: false, code: 'capture-unavailable', message: 'Frame capture is unavailable in this browser.' };

    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return { success: true, dataUrl: canvas.toDataURL('image/jpeg', jpegQuality), capturedAt: Date.now() };
  } catch {
    return {
      success: false,
      code: 'capture-unavailable',
      message: 'This video does not permit frame capture. Protected or cross-origin video cannot be captured.',
    };
  }
}
