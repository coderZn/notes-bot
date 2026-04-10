"""
自动打标签
基于关键词匹配 + LLM 推断
"""

from config import ALLOWED_TAGS, DEFAULT_TAG

# 关键词 → 标签映射
KEYWORD_TAG_MAP = {
    "工作": ["工作", "任务", "需求", "项目", "客户", "领导", "开会", "报告", "周报", "日报", "进度"],
    "技术": ["代码", "bug", "前端", "后端", "API", "接口", "框架", "Vue", "React", "JavaScript", "Python", "服务器", "部署", "docker", "nginx"],
    "前端": ["页面", "组件", "样式", "CSS", "布局", "动画", "DOM", "浏览器", "H5", "小程序"],
    "学习": ["学", "看", "读", "视频", "课程", "文档", "笔记", "理解", "研究"],
    "待办": ["待办", "TODO", "记得", "提醒", "要做", "要弄", "还没"],
    "想法": ["觉得", "认为", "想法", "觉得可以", "突然想到", "灵感"],
    "项目": ["项目", "模块", "重构", "优化", "方案", "设计", "架构"],
    "生活": ["吃饭", "睡觉", "运动", "健康", "约", "朋友", "周末", "假期", "旅游"],
    "问题": ["问题", "不懂", "不会", "不知道为什么", "卡在", "解决不了", "报错"],
    "灵感": ["灵感", "创新", "有意思", "这个想法", "突然发现"],
}


def extract_tags(content: str) -> list:
    """
    根据内容自动提取标签
    优先级：完全匹配关键词 > 包含关键词 > 默认标签
    """
    matched = set()
    content_lower = content.lower()

    for tag, keywords in KEYWORD_TAG_MAP.items():
        for kw in keywords:
            if kw in content or kw.lower() in content_lower:
                matched.add(tag)

    if not matched:
        return [DEFAULT_TAG]

    # 限制最多3个标签
    return list(matched)[:3]


def suggest_tags(content: str) -> str:
    """给 LLM 用的标签建议 prompt"""
    tags_str = ", ".join(ALLOWED_TAGS)
    return f"""
根据以下笔记内容，从 [{tags_str}] 中选择最合适的标签，返回 1-3 个标签，用逗号分隔。

笔记内容：
{content}

返回格式：标签1, 标签2, 标签3
"""
