import { ALLOWED_TAGS, DEFAULT_TAG } from '../config';

const KEYWORD_TAG_MAP: Record<string, string[]> = {
  '工作': ['工作', '任务', '需求', '项目', '客户', '领导', '开会', '报告', '周报', '日报', '进度'],
  '技术': ['代码', 'bug', 'API', '接口', '框架', '服务器', '部署', 'docker', 'nginx'],
  '前端': ['页面', '组件', '样式', 'CSS', '布局', '动画', 'DOM', '浏览器', 'H5', '小程序', 'Vue', 'React', 'JavaScript'],
  '学习': ['学', '看', '读', '视频', '课程', '笔记', '理解', '研究'],
  '待办': ['待办', 'TODO', '记得', '提醒', '要做', '要弄', '还没'],
  '想法': ['觉得', '认为', '想法', '觉得可以', '突然想到', '灵感'],
  '项目': ['项目', '模块', '重构', '优化', '方案', '设计', '架构'],
  '生活': ['吃饭', '睡觉', '运动', '健康', '约', '朋友', '周末', '假期', '旅游'],
  '问题': ['问题', '不懂', '不会', '不知道为什么', '卡在', '解决不了', '报错'],
  '灵感': ['灵感', '创新', '有意思', '这个想法', '突然发现'],
};

export function extractTags(content: string): string[] {
  const matched = new Set<string>();
  const contentLower = content.toLowerCase();

  for (const [tag, keywords] of Object.entries(KEYWORD_TAG_MAP)) {
    for (const kw of keywords) {
      if (content.includes(kw) || contentLower.includes(kw.toLowerCase())) {
        matched.add(tag);
        break;
      }
    }
  }

  if (matched.size === 0) {
    return [DEFAULT_TAG];
  }

  return Array.from(matched).slice(0, 3);
}
