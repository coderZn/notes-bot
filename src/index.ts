import { NoteStore } from './storage/noteStore';
import { extractTags } from './utils/tagger';
import { generateSummary } from './utils/summarizer';

export interface HandlerResult {
  ok: boolean;
  type?: string;
  note_id?: number;
  summary?: string;
  tags?: string[];
  count?: number;
  results?: any[];
  tag?: string;
  error?: string;
}

export class MessageHandler {
  private store: NoteStore;

  private CMD_SEARCH = ['搜索', '找一下', '查一下'];
  private CMD_RECENT = ['我的笔记', '最近笔记', '查看笔记'];
  private CMD_TAG = ['标签', '按标签'];
  private CMD_HELP = ['帮助', 'help', '怎么用'];

  constructor() {
    this.store = new NoteStore();
  }

  handle(userInput: string): HandlerResult {
    const input = userInput.trim();
    if (!input) {
      return { ok: false, error: '笔记内容不能为空哦~' };
    }

    if (this.isCommand(input, this.CMD_HELP)) {
      return this.help();
    }
    if (this.isCommand(input, this.CMD_SEARCH)) {
      const keyword = this.extractKeyword(input, this.CMD_SEARCH);
      return this.search(keyword);
    }
    if (this.isCommand(input, this.CMD_RECENT)) {
      return this.recentNotes();
    }
    if (this.isCommand(input, this.CMD_TAG)) {
      const tag = this.extractKeyword(input, this.CMD_TAG);
      return this.notesByTag(tag);
    }

    return this.saveNote(input);
  }

  private isCommand(text: string, cmds: string[]): boolean {
    return cmds.some(cmd => text.includes(cmd));
  }

  private extractKeyword(text: string, cmds: string[]): string {
    for (const cmd of cmds) {
      if (text.includes(cmd)) {
        return text.replace(cmd, '').trim();
      }
    }
    return '';
  }

  private saveNote(content: string): HandlerResult {
    const tags = extractTags(content);
    const summary = generateSummary(content);
    const noteId = this.store.addNote(content, tags, summary);
    return {
      ok: true,
      type: 'save',
      note_id: noteId,
      summary,
      tags,
    };
  }

  search(keyword: string): HandlerResult {
    if (!keyword) {
      return { ok: false, error: '请告诉我你想搜什么？格式：`搜索 XXX`' };
    }
    const results = this.store.search(keyword);
    return { ok: true, type: 'search', count: results.length, results };
  }

  recentNotes(): HandlerResult {
    const results = this.store.getRecent(10);
    return { ok: true, type: 'recent', count: results.length, results };
  }

  notesByTag(tag: string): HandlerResult {
    if (!tag) {
      return { ok: false, error: '请告诉我你想看哪个标签？格式：`标签 XXX`' };
    }
    const results = this.store.getByTag(tag);
    return { ok: true, type: 'tag', tag, count: results.length, results };
  }

  private help(): HandlerResult {
    return {
      ok: true,
      type: 'help',
    };
  }
}

// CLI 入口
if (require.main === module) {
  const handler = new MessageHandler();
  const args = process.argv.slice(2);

  if (args.length < 1) {
    console.log(JSON.stringify({ ok: false, error: '参数不足，格式：node dist/index.js <命令> [内容]' }));
    process.exit(1);
  }

  const cmd = args[0];
  const content = args.slice(1).join(' ');

  let result: HandlerResult;
  switch (cmd) {
    case 'save':
      result = handler.handle(content);
      break;
    case 'search':
      result = handler.search(content);
      break;
    case 'recent':
      result = handler.recentNotes();
      break;
    case 'tag':
      result = handler.notesByTag(content);
      break;
    default:
      result = { ok: false, error: `未知命令: ${cmd}` };
  }

  console.log(JSON.stringify(result, null, 2));
}
