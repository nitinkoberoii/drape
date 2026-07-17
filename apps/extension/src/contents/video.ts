import type { PlasmoCSConfig } from 'plasmo';

export const config: PlasmoCSConfig = {
  matches: ['<all_urls>'],
  run_at: 'document_idle',
};

// Phase 1 will add supported-site detection and video communication here.
export {};
