"""
配置
"""

# 笔记存储目录
NOTES_DIR = "/Users/coderzn/.openclaw/workspace/notes"

# 笔记数据库（SQLite 用于检索索引）
DB_PATH = "/Users/coderzn/.openclaw/workspace/notes/notes.db"

# 标签白名单
ALLOWED_TAGS = [
    "工作", "技术", "想法", "待办", "学习",
    "项目", "前端", "生活", "问题", "灵感",
]

# 默认标签（无法分类时使用）
DEFAULT_TAG = "杂项"

# 摘要长度
SUMMARY_MAX_CHARS = 50
