"""
摘要生成
基于规则 + LLM 两种方式
"""

SUMMARY_MAX_CHARS = 50


def generate_summary(content: str, use_llm: bool = False) -> str:
    """
    生成一句话摘要

    规则方式：取前 N 个字符，尽量在标点或断句处截断
    LLM 方式：调用 LLM 生成更准确的摘要
    """
    if not content:
        return ""

    if use_llm:
        return _generate_summary_llm(content)

    return _generate_summary_rule(content)


def _generate_summary_rule(content: str) -> str:
    """基于规则生成摘要"""
    # 移除多余空白
    content = " ".join(content.split())

    # 如果已经很短，直接返回
    if len(content) <= SUMMARY_MAX_CHARS:
        return content

    # 在句子边界截断
    cutpoints = ['。', '！', '？', '，', '.', '!', '?', ',', '\n']
    cutoff = SUMMARY_MAX_CHARS

    for cp in cutpoints:
        idx = content.rfind(cp, 0, cutoff)
        if idx > 10:  # 确保不是太靠前
            cutoff = idx + 1
            break

    result = content[:cutoff]
    if len(content) > cutoff:
        result += "..."
    return result


def _generate_summary_llm(content: str) -> str:
    """调用 LLM 生成摘要"""
    # TODO: 后续接入 LLM
    return _generate_summary_rule(content)


def make_summary_prompt(content: str) -> str:
    """给 LLM 用的摘要 prompt"""
    return f"""
请用一句话概括以下笔记的核心内容，不超过 50 字。

笔记内容：
{content}

返回格式：一句话摘要
"""
