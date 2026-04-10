import { SUMMARY_MAX_CHARS } from '../config';

const CUTPOINTS = ['。', '！', '？', '，', '.', '!', '?', ',', '\n'];

export function generateSummary(content: string): string {
  if (!content) return '';

  const trimmed = content.replace(/\s+/g, ' ').trim();

  if (trimmed.length <= SUMMARY_MAX_CHARS) {
    return trimmed;
  }

  let cutoff = SUMMARY_MAX_CHARS;
  for (const cp of CUTPOINTS) {
    const idx = trimmed.lastIndexOf(cp, cutoff);
    if (idx > 10) {
      cutoff = idx + 1;
      break;
    }
  }

  const result = trimmed.substring(0, cutoff);
  return result.length < trimmed.length ? result + '...' : result;
}
