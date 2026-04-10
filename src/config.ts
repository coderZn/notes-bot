import * as path from 'path';
import * as os from 'os';

export const NOTES_DIR = path.join(os.homedir(), '.openclaw', 'workspace', 'notes');
export const DB_PATH = path.join(NOTES_DIR, 'notes.db');

export const ALLOWED_TAGS = [
  '工作', '技术', '想法', '待办', '学习',
  '项目', '前端', '生活', '问题', '灵感',
];

export const DEFAULT_TAG = '杂项';
export const SUMMARY_MAX_CHARS = 50;
