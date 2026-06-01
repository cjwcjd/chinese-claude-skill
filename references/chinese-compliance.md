# 中文化合规参考——理论 + 操作 + 模式库

> SKILL.md 的详细参考。按需翻看，不需要每次加载。

## 一、为什么思考必须强制中文

训练数据约 90% 英文，推理链几乎全是英文。进入 thinking 块时默认语言就是英文——不是"选择"，是训练偏差（母语干扰级别）。

英文思考的"流畅感"来自统计频率，不是质量优势。用中文表达同样推理不损失任何信息——只是统计上不占优，需要主动切换。

## 二、违规模式库

### thinking 块红灯句式

| 句式 | 正则 | 说明 |
|------|------|------|
| Let me think about... | `^(Let me\|Let's) [a-z]` | 英文起手式 |
| The user wants... | `^The [a-z].* (wants\|needs\|is)` | 英文主语结构 |
| I need to... | `^I (need\|want\|have\|should\|can\|will)` | 英文第一人称 |
| First, I should... | `^(First\|Next\|Then\|Finally\|Also\|Now),? [A-Za-z]` | 英文序列思维 |
| Looking at this... | `^(Looking\|Going\|Checking\|Reading\|Based) [a-z]` | 英文分词引导 |
| This is because... | `^(This\|That\|It\|There) [a-z].* (is\|was\|are\|were)` | 英文指示代词 |
| We can... | `^(We\|You) (can\|could\|should\|might\|will\|would)` | 英文祈使/建议 |

对应的中文表达：

| 违规 | ✅ |
|------|------|
| "Let me think about this..." | "这个问题需要分析..." |
| "The user wants me to..." | "用户要求我..." |
| "I need to check..." | "需要检查..." |
| "First, I should read..." | "首先读取..." |
| "Looking at the code..." | "看这段代码..." |

### 代码 / 文档 / 对话违规

| 维度 | ❌ | ✅ |
|------|------|------|
| 行注释 | `// Create a new user` | `// 创建新用户` |
| Docstring | `/** Get user by ID */` | `/** 根据 ID 获取用户 */` |
| TODO | `// TODO: add validation` | `// TODO: 添加验证` |
| 文档标题 | `## Installation` | `## 安装` |
| 文档表格头 | `\| Name \| Description \|` | `\| 名称 \| 说明 \|` |
| 对话回复 | 完整英文句 | 全部中文，术语可保留 |

### 豁免规则

以下不算违规：代码块内容、技术术语（REST/OAuth/GraphQL）、包名/库名（React/webpack）、API 端点、单字母缩写（id/url/DB）、commit type 前缀（`feat(auth):`）。

## 三、失败模式与对策

| 模式 | 表现 | 对策 |
|------|------|------|
| 起手式英文 | thinking 块第一句就是英文 | 锚点："好的，→ 用中文思考" |
| 渐变漂移 | 中文开头 → 不知不觉切英文 | 每 3 句自检 |
| 技术切换 | 遇到术语后整段切英文 | 术语保留，其余全部中文 |
| 长链惯性 | 推理链越长越易回英文 | 每个子问题重念锚点 |
| 工具调用后 | 工具结果返回第一句易用英文 | 刻意用中文重组思路 |
| hook 措辞过弱 | system-reminder 只描述"要做什么"，不说"怎么做"——模型当规范读，不当命令执行 | hook 中写入具体锚点指令 + 自检步骤 + 违规自首要求，用编号列表给出可执行动作 |
