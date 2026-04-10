# 📓 柚子笔记机器人

通过 QQ 接收消息，自动打标签、提炼摘要、存入知识库，支持后续检索。

## 功能

- `记一下 XXX` / 直接发送内容 → 自动打标签 + 摘要 + 存储
- `搜索 XXX` → 全文检索
- `我的笔记` → 最近 10 条
- `标签 XXX` → 按标签查看

## 技术栈

- **TypeScript** + **SQLite**（better-sqlite3）
- OpenClaw Skill 接入 QQ
- 支持 OpenAI / MiniMax 等 LLM 生成摘要和标签

## 快速开始

```bash
npm install

# 编译
npm run build

# CLI 测试
node dist/index.js save "今天学了点 Vue3"
node dist/index.js search "Vue"
node dist/index.js recent
node dist/index.js tag "前端"
```

## 项目结构

```
src/
├── config.ts           # 配置（路径、标签白名单）
├── index.ts            # 主入口 + MessageHandler
├── storage/
│   └── noteStore.ts    # SQLite + Markdown 存储
└── utils/
    ├── tagger.ts       # 关键词打标签
    └── summarizer.ts   # 摘要生成
```

## 标签分类

`工作` `技术` `前端` `学习` `待办` `想法` `项目` `生活` `问题` `灵感` `杂项`

## OpenClaw Skill

参见 `../skills/qqbot-notes/`

## License

MIT
