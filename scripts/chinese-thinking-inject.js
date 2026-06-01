// 中文化注入 — SessionStart / PreToolUse hook
// stdout 内容会作为 system-reminder 注入 LLM 上下文
console.log(`<system-reminder>
🔴 中文锁定（强制执行，无例外）：

1. thinking 块第一句必须是 "好的，→ 用中文思考。" ——这是语言锚点，不可跳过。
2. thinking 块后续全部用简体中文。每写 3 句回头自检一次。
3. 对话回复、TodoWrite 任务列表、对话标题全部用简体中文。
4. 如 thinking 块出现英文完整句，正文第一行必须公开声明自首。

技术术语（REST、OAuth）可保留。代码本身不受影响。

违反以上任何一条 = 未执行基本指令。
</system-reminder>`);
