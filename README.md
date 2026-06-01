# chinese-claude-skill — 全局中文化输出规范

让 Claude Code 在所有人类可读文本中默认使用简体中文。

## 🎯 一句话

**加载即生效——覆盖对话、文档、注释、Git、计划、终端、思考过程。内置自检闭环 + 违规自首机制。**

## 🆚 与现有方案的区别

| | superpowers-zh 中文技能 | chinese-claude-skill |
|------|:--:|:--:|
| 触发 | 手动 `/chinese-xxx` | **自动加载** |
| 覆盖 | 单领域 | **全部领域** |
| 思考中文 | ❌ | ✅ 锚点强制 |
| 自检 | ❌ | ✅ 三步闭环 |
| 审计工具 | ❌ | ✅ Python 脚本 |

## 📦 安装

```bash
# 1. 克隆技能
cd ~/.claude/skills
git clone https://github.com/cjwcjd/chinese-claude-skill.git

# 2. 安装 SessionStart hook（推荐——系统层注入）
mkdir -p ~/.claude/hooks
cp ~/.claude/skills/chinese-claude-skill/scripts/chinese-thinking-inject.js ~/.claude/hooks/
```

然后在 `.claude/settings.json` 的 `hooks.SessionStart` 中加入：

```json
{
  "matcher": "",
  "hooks": [{
    "type": "command",
    "command": "node \"~/.claude/hooks/chinese-thinking-inject.js\"",
    "timeout": 5
  }]
}
```

## 📂 目录

```
chinese-claude-skill/
├── SKILL.md                         # 入口：执行规则 + 适用范围 + 反辩解
├── references/
│   └── chinese-compliance.md        # 理论分析 + 违规模式库 + 失败模式对策
├── assets/
│   └── self-check-card.md           # 输出前速查卡片
├── scripts/
│   ├── audit-chinese.py             # 事后审计脚本
│   └── chinese-thinking-inject.js   # SessionStart hook（系统层注入）
├── README.md
├── LICENSE
└── .gitignore
```

## 🔧 执行流程

```
步骤一 锚点 —— thinking 块首句锁定 "好的，→ 用中文思考。"
步骤二 三句自检 —— 每 3 句扫描一次，发现英文立即切换
步骤三 违规自首 —— 若违规已发出，正文第一行公开声明
```

## 🧩 覆盖

| ✅ 中文 | ❌ 英文 |
|------|------|
| 🧠 思考过程 | 变量名/函数名/类名 |
| 🗣️ 对话回复 | 包名/模块路径 |
| 📄 文档 | API 端点/参数名 |
| 💬 代码注释 | 技术术语（REST、OAuth） |
| 📝 Git | 第三方库名（React、npm） |
| 📋 计划 | 代码内字符串 |
| ⚙️ 配置注释 | |
| 🖥️ 终端输出 | |

## 🛠 审计脚本

```bash
python scripts/audit-chinese.py transcript.md       # 扫描
python scripts/audit-chinese.py transcript.md --json # JSON
```

返回值：`0` = 零违规，`1` = 发现违规，`2` = 文件不存在或参数错误。

## 📄 许可证

MIT
