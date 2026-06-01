// 中文化注入 — SessionStart hook
// stdout 内容会作为 system-reminder 注入 LLM 上下文
console.log(`<system-reminder>
🔴 中文锁定：用户未明确要求英文产物时，本会话所有面向人类的输出必须使用简体中文，包括但不限于：
  - thinking 块（思考过程）
  - 对话回复
  - TodoWrite 任务列表
  - 对话标题（如有标题生成机会，必须用中文，如"安装 OpenCLI Chrome 扩展"而非"Help installing OpenCLI extension"）
  - 代码注释、文档标题、Git commit/PR/Issue 文本
  允许保留英文：代码标识符、包名、API、路径、命令、错误原文、标准 commit type/scope 和必要技术术语。
  违反此规则 = 未执行基本指令。
</system-reminder>`);
