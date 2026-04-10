"""
笔记存储层
支持 Markdown 文件存储 + SQLite 索引
"""

import os
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from config import NOTES_DIR, DB_PATH, ALLOWED_TAGS, DEFAULT_TAG, SUMMARY_MAX_CHARS


class NoteStore:
    def __init__(self):
        self.notes_dir = Path(NOTES_DIR)
        self.notes_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """初始化 SQLite"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                summary TEXT,
                tags TEXT,
                source TEXT DEFAULT 'qq',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        # 全文搜索索引
        c.execute("CREATE INDEX IF NOT EXISTS idx_content ON notes(content)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_tags ON notes(tags)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_created ON notes(created_at)")
        conn.commit()
        conn.close()

    def add_note(self, content: str, tags: list = None, summary: str = None):
        """添加笔记"""
        tags = tags or [DEFAULT_TAG]
        tags_str = ",".join(tags)

        # 摘要截断
        if summary and len(summary) > SUMMARY_MAX_CHARS:
            summary = summary[:SUMMARY_MAX_CHARS] + "..."

        now = datetime.now().isoformat()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO notes (content, summary, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (content, summary, tags_str, now, now))
        note_id = c.lastrowid
        conn.commit()
        conn.close()

        # 同时存一份 Markdown 方便直接查看
        self._save_as_markdown(note_id, content, tags, summary, now)

        return note_id

    def _save_as_markdown(self, note_id: int, content: str, tags: list, summary: str, created_at: str):
        """存一份 Markdown 文件"""
        date = created_at[:10]
        filename = self.notes_dir / f"{date}_{note_id}.md"
        tags_str = " ".join([f"`{t}`" for t in tags])
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# 笔记 #{note_id}\n\n")
            f.write(f"**标签**：{tags_str}\n\n")
            f.write(f"**摘要**：{summary or '无'}\n\n")
            f.write(f"**时间**：{created_at}\n\n")
            f.write("---\n\n")
            f.write(content)

    def search(self, keyword: str, limit: int = 10) -> list:
        """搜索笔记"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT id, content, summary, tags, created_at
            FROM notes
            WHERE content LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (f"%{keyword}%", limit))
        results = c.fetchall()
        conn.close()
        return results

    def get_recent(self, limit: int = 10) -> list:
        """获取最近笔记"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT id, content, summary, tags, created_at
            FROM notes
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        results = c.fetchall()
        conn.close()
        return results

    def get_by_tag(self, tag: str, limit: int = 10) -> list:
        """按标签查询"""
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            SELECT id, content, summary, tags, created_at
            FROM notes
            WHERE tags LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (f"%{tag}%", limit))
        results = c.fetchall()
        conn.close()
        return results


if __name__ == "__main__":
    store = NoteStore()
    # 测试添加
    note_id = store.add_note(
        content="这是一个测试笔记，关于 Vue3 的响应式原理",
        tags=["技术", "前端", "Vue"],
        summary="Vue3 响应式原理"
    )
    print(f"添加成功，ID: {note_id}")

    # 测试搜索
    results = store.search("Vue3")
    print(f"搜索结果: {len(results)} 条")
