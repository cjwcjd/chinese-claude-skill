// 中文化思考注入 — SessionStart hook
// stdout 内容会作为 system-reminder 注入 LLM 上下文
console.log(`<system-reminder>
🔴 中文思考锁定：本会话所有 thinking 块必须以简体中文书写。进入 thinking 块前，第一句固定为"好的，→ 用中文思考。"。违反此规则 = 未执行基本指令。
</system-reminder>`);
