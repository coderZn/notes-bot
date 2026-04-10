# 对话式笔记机器人

> 通过 QQ 接收消息，自动打标签、提炼摘要、存入知识库。后续可检索。

## 项目结构

```
notes-bot/
├── handlers/
│   └── message_handler.py   # 接收消息 → 分类 → 存储
├── storage/
│   └── note_store.py         # 笔记存储（Markdown + SQLite）
├── utils/
│   ├── tagger.py             # 自动打标签
│   └── summarizer.py         # 摘要生成
└── config.py                 # 配置文件
```

## 工作流程

```
QQ 消息
  ↓
意图分类（intent classifier）
  ↓
判断：笔记 / 检索 / 其他
  ↓
笔记 → 打标签 + 摘要 + 存入 storage
检索 → 搜索知识库 → 返回结果
```

## 命令

- `记一下 XXX` → 按笔记处理
- `搜索 XXX` → 检索知识库
- `我的笔记` → 查看最近笔记列表
- `标签：XXX` → 查看某标签下的笔记

## 开发进度

- [x] 项目结构搭建
- [ ] 消息接收与路由
- [ ] 自动打标签
- [ ] 摘要生成
- [ ] 存储层
- [ ] 检索功能
