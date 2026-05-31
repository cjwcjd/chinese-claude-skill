// 中文化注入 — SessionStart hook
// stdout 内容会作为 system-reminder 注入 LLM 上下文
console.log(`<system-reminder>
🔴 中文锁定：本会话所有输出必须使用简体中文，包括但不限于：
  - thinking 块（思考过程）
  - 对话回复
  - TodoWrite 任务列表
  - 对话标题（如有标题生成机会，必须用中文，如"安装 OpenCLI Chrome 扩展"而非"Help installing OpenCLI extension"）
  违反此规则 = 未执行基本指令。
</system-reminder>`);
