"""
消息处理器
接收消息 → 判断意图 → 路由到对应处理函数
"""

import sys
import re
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.note_store import NoteStore
from utils.tagger import extract_tags
from utils.summarizer import generate_summary


class MessageHandler:
    def __init__(self):
        self.store = NoteStore()

        # 命令前缀
        self.CMD_SEARCH = ["搜索", "找一下", "查一下"]
        self.CMD_RECENT = ["我的笔记", "最近笔记", "查看笔记"]
        self.CMD_TAG = ["标签", "按标签"]
        self.CMD_HELP = ["帮助", "help", "怎么用"]

    def handle(self, user_input: str, sender_id: str = None) -> str:
        """
        主入口：处理用户输入，返回回复内容
        """
        user_input = user_input.strip()

        if not user_input:
            return "笔记内容不能为空哦~"

        # 命令路由
        if self._is_command(user_input, self.CMD_HELP):
            return self._help()

        if self._is_command(user_input, self.CMD_SEARCH):
            keyword = self._extract_keyword(user_input, self.CMD_SEARCH)
            return self._search(keyword)

        if self._is_command(user_input, self.CMD_RECENT):
            return self._recent_notes()

        if self._is_command(user_input, self.CMD_TAG):
            tag = self._extract_keyword(user_input, self.CMD_TAG)
            return self._notes_by_tag(tag)

        # 默认：当作笔记处理
        return self._save_note(user_input)

    def _is_command(self, text: str, cmd_list: list) -> bool:
        return any(cmd in text for cmd in cmd_list)

    def _extract_keyword(self, text: str, cmd_list: list) -> str:
        """提取命令后的关键词"""
        for cmd in cmd_list:
            if cmd in text:
                keyword = text.replace(cmd, "").strip()
                return keyword if keyword else None
        return None

    def _save_note(self, content: str) -> str:
        """保存笔记"""
        tags = extract_tags(content)
        summary = generate_summary(content)
        note_id = self.store.add_note(content, tags, summary)

        tags_str = " ".join([f"`{t}`" for t in tags])
        return (
            f"✅ 已记下！\n\n"
            f"📝 {summary}\n\n"
            f"🏷️ {tags_str}\n\n"
            f"[ID: {note_id}]"
        )

    def _search(self, keyword: str) -> str:
        """搜索笔记"""
        if not keyword:
            return "请告诉我你想搜什么？\n\n格式：`搜索 XXX`"

        results = self.store.search(keyword)
        if not results:
            return f"没找到关于「{keyword}」的笔记~\n\n试试换个关键词？"

        lines = [f"找到 {len(results)} 条相关笔记：\n"]
        for note_id, content, summary, tags, created in results[:5]:
            date = created[:10]
            tags_str = " ".join([f"`{t}`" for t in tags.split(",")])
            preview = content[:30] + "..." if len(content) > 30 else content
            lines.append(f"\n## [{date}] {summary or preview}")
            lines.append(f"🏷️ {tags_str} [ID:{note_id}]")

        return "\n".join(lines)

    def _recent_notes(self) -> str:
        """最近笔记"""
        results = self.store.get_recent(limit=10)
        if not results:
            return "还没有笔记，记点什么吧~\n\n格式：`记一下 XXX`"

        lines = ["📓 最近笔记：\n"]
        for note_id, content, summary, tags, created in results:
            date = created[5:10]  # MM-DD
            preview = content[:25] + "..." if len(content) > 25 else content
            lines.append(f"\n[{date}] {summary or preview}")
            lines.append(f"   🏷️ `{'|'.join(tags.split(','))}` [ID:{note_id}]")

        return "\n".join(lines)

    def _notes_by_tag(self, tag: str) -> str:
        """按标签查看"""
        if not tag:
            return "请告诉我你想看哪个标签？\n\n格式：`标签 Vue`"

        results = self.store.get_by_tag(tag, limit=10)
        if not results:
            return f"没有标签为「{tag}」的笔记~\n\n已有标签：工作、技术、想法、前端、学习、待办、生活、问题、灵感"

        lines = [f"🏷️ 「{tag}」相关的笔记：\n"]
        for note_id, content, summary, tags, created in results:
            date = created[5:10]
            lines.append(f"\n[{date}] {summary or content[:25]}")
            lines.append(f"   [ID:{note_id}]")

        return "\n".join(lines)

    def _help(self) -> str:
        return """
📓 柚子笔记机器人 - 使用帮助

**记笔记**
直接发送内容：`今天学了点 Vue3`
我会自动打标签 + 生成摘要

**搜索笔记**
格式：`搜索 Vue`

**查看最近**
格式：`我的笔记`

**按标签查看**
格式：`标签 前端`

**其他**
问「帮助」看这个说明
"""


if __name__ == "__main__":
    handler = MessageHandler()

    # 简单测试
    tests = [
        "今天学了点 Vue3 的响应式原理，感觉比 Vue2 复杂很多",
        "搜索 Vue",
        "我的笔记",
        "标签 技术",
    ]

    for t in tests:
        print(f"\n>>> {t}")
        print(handler.handle(t))
