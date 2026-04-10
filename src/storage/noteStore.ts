import Database from 'better-sqlite3';
import * as fs from 'fs';
import * as path from 'path';
import { NOTES_DIR, DB_PATH, ALLOWED_TAGS, DEFAULT_TAG, SUMMARY_MAX_CHARS } from '../config';

export interface Note {
  id: number;
  content: string;
  summary: string | null;
  tags: string;
  source: string;
  created_at: string;
  updated_at: string;
}

export interface NoteResult {
  id: number;
  content: string;
  summary: string | null;
  tags: string;
  created: string;
}

export class NoteStore {
  private db: Database.Database;

  constructor() {
    if (!fs.existsSync(NOTES_DIR)) {
      fs.mkdirSync(NOTES_DIR, { recursive: true });
    }
    this.db = new Database(DB_PATH);
    this.initDb();
  }

  private initDb(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        summary TEXT,
        tags TEXT,
        source TEXT DEFAULT 'qq',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
      )
    `);
    this.db.exec(`CREATE INDEX IF NOT EXISTS idx_content ON notes(content)`);
    this.db.exec(`CREATE INDEX IF NOT EXISTS idx_tags ON notes(tags)`);
    this.db.exec(`CREATE INDEX IF NOT EXISTS idx_created ON notes(created_at)`);
  }

  addNote(content: string, tags: string[], summary: string | null = null): number {
    const tagsStr = tags.join(',');
    let finalSummary = summary;
    if (finalSummary && finalSummary.length > SUMMARY_MAX_CHARS) {
      finalSummary = finalSummary.substring(0, SUMMARY_MAX_CHARS) + '...';
    }

    const now = new Date().toISOString();
    const stmt = this.db.prepare(`
      INSERT INTO notes (content, summary, tags, source, created_at, updated_at)
      VALUES (?, ?, ?, 'qq', ?, ?)
    `);
    const result = stmt.run(content, finalSummary, tagsStr, now, now);
    const noteId = result.lastInsertRowid as number;

    this.saveAsMarkdown(noteId, content, tags, finalSummary, now);
    return noteId;
  }

  private saveAsMarkdown(noteId: number, content: string, tags: string[], summary: string | null, createdAt: string): void {
    const date = createdAt.substring(0, 10);
    const filename = path.join(NOTES_DIR, `${date}_${noteId}.md`);
    const tagsStr = tags.map(t => `\`${t}\``).join(' ');

    const md = `# 笔记 #${noteId}\n\n` +
      `**标签**：${tagsStr}\n\n` +
      `**摘要**：${summary || '无'}\n\n` +
      `**时间**：${createdAt}\n\n` +
      `---\n\n` +
      `${content}`;

    fs.writeFileSync(filename, md, 'utf-8');
  }

  search(keyword: string, limit: number = 10): NoteResult[] {
    const stmt = this.db.prepare(`
      SELECT id, content, summary, tags, created_at
      FROM notes
      WHERE content LIKE ?
      ORDER BY created_at DESC
      LIMIT ?
    `);
    const rows = stmt.all(`%${keyword}%`, limit) as Note[];
    return rows.map(r => ({
      id: r.id,
      content: r.content.length > 50 ? r.content.substring(0, 50) + '...' : r.content,
      summary: r.summary,
      tags: r.tags,
      created: r.created_at.substring(0, 10),
    }));
  }

  getRecent(limit: number = 10): NoteResult[] {
    const stmt = this.db.prepare(`
      SELECT id, content, summary, tags, created_at
      FROM notes
      ORDER BY created_at DESC
      LIMIT ?
    `);
    const rows = stmt.all(limit) as Note[];
    return rows.map(r => ({
      id: r.id,
      content: r.content.length > 40 ? r.content.substring(0, 40) + '...' : r.content,
      summary: r.summary,
      tags: r.tags,
      created: r.created_at.substring(5, 10),
    }));
  }

  getByTag(tag: string, limit: number = 10): NoteResult[] {
    const stmt = this.db.prepare(`
      SELECT id, content, summary, tags, created_at
      FROM notes
      WHERE tags LIKE ?
      ORDER BY created_at DESC
      LIMIT ?
    `);
    const rows = stmt.all(`%${tag}%`, limit) as Note[];
    return rows.map(r => ({
      id: r.id,
      content: r.content.length > 40 ? r.content.substring(0, 40) + '...' : r.content,
      summary: r.summary,
      tags: r.tags,
      created: r.created_at.substring(5, 10),
    }));
  }
}
