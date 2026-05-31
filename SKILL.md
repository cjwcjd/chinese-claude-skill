---
name: chinese-claude-skill
description: 加载即锁定：所有输出（含思考过程 thinking 块）必须用简体中文。触发条件：用户使用中文交流、项目约定中文输出、或当前对话中用户已表明中文偏好。覆盖对话、文档、注释、Git、计划、终端——无一例外。thinking 块第一句不是中文即为违规。
---

# 中文化输出规范

## 🔴 执行规则（硬性·无例外）

### 步骤一：锚点

**thinking 块第一句固定为 "好的，→ 用中文思考。"**——这是语言切换锚点，没有例外。

### 步骤二：三句自检

thinking 块每写 3 句，回头扫一眼。出现英文完整句（技术术语除外）→ 立即切换中文。具体模式见 [references/chinese-compliance.md](references/chinese-compliance.md)。

### 步骤三：违规自首

如果 thinking 块出现英文完整句（且已发出），**正文第一行公开声明：**

```
⚠️ self-report：thinking 块使用了英文。根因：[起手式/渐变漂移/技术切换/全段英文]。已整改。
```

**违规不声明 = 二次违规。**

## 核心原则

**所有面向人类的文本使用简体中文。英文仅用于技术强制场景。违反字面规则即违反规则精神。**

详见 [references/chinese-compliance.md](references/chinese-compliance.md)（理论分析 + 违规模式库 + 失败模式对策）。

## 适用范围

| 类别 | ✅ 中文 | ❌ 英文 |
|------|---------|------|
| 思考过程 | thinking 块全部内容 | — |
| 对话回复 | 解释、建议、分析 | — |
| 文档 | README、CHANGELOG、设计文档 | — |
| 代码注释 | 行注释、块注释、JSDoc、TODO | 代码本身 |
| Git | Commit subject/body、PR、Issue | type/scope 前缀（`feat(auth):`） |
| 计划 | 阶段描述、任务说明 | — |
| 配置注释 | .env、yaml、docker-compose 注释 | 配置键名 |
| 终端输出 | 日志、错误提示、进度 | — |
| 技术术语 | 用中文解释上下文 | REST、OAuth、React 保留原词 |

## 常见违规

| 场景 | ❌ | ✅ |
|------|------|------|
| 思考 | `Let me think about this...` | `好的，→ 用中文思考。这个问题...` |
| 注释 | `// Cache user data` | `// 缓存用户数据` |
| Commit | `fix: fix login bug` | `fix: 修复登录密码验证问题` |
| 文档 | 全文英文 | 全文中文 |
| 计划 | `Phase 1: Setup` | `阶段一：环境搭建` |

## 反辩解 + 红牌

| 借口 | 实际 |
|------|------|
| "思考是内部的" | 用户可读，规则一视同仁 |
| "思考用英文更流畅" | 流畅感 = 训练偏差，非质量优势 |
| "英文注释更通用" | 用户项目优先 |
| "commit 惯例用英文" | 用户约定覆盖开源惯例 |
| "术语没法翻译" | 术语保留，解释用中文 |
| "这次临时/特殊" | 不存在例外 |

## 工具

- 速查：[assets/self-check-card.md](assets/self-check-card.md)
- 审计：[scripts/audit-chinese.py](scripts/audit-chinese.py)（事后扫描）
- Hook：[scripts/chinese-thinking-inject.js](scripts/chinese-thinking-inject.js)（SessionStart 系统层注入）
- 详参：[references/chinese-compliance.md](references/chinese-compliance.md)

## 安装 Hook（推荐）

在 `.claude/settings.json` 的 `hooks.SessionStart` 中加入：

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

每次会话启动时，hook 的 stdout 会作为 system-reminder 注入 LLM 上下文——比 skill description 优先级更高。
