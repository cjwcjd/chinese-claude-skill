#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文化审计脚本 — 扫描文本文件，检测英文违规模式。

用法:
    python audit-chinese.py <file>           # 扫描单个文件
    python audit-chinese.py <file> --json    # 输出 JSON 格式
    python audit-chinese.py <file> --fix     # 标记违规位置（不修改原文件）

检测维度:
    1. 英文完整句子（thinking 块红灯句式）
    2. 英文代码注释
    3. 英文文档标题/段落
    4. 英文对话回复

返回值:
    0 = 零违规
    1 = 发现违规
"""

import re
import sys
import json
import argparse
from pathlib import Path

# ── 违规模式定义 ──────────────────────────────────────────────

# 英文起手式（thinking 块红灯句式）
THINKING_RED_FLAGS = [
    (r"^Let me think about", "起手式：'Let me think about...'"),
    (r"^Let's [a-z]", "起手式：'Let's ...'"),
    (r"^The user (wants|needs|is|has|said|asked)", "主语结构：'The user ...'"),
    (r"^I (need|want|have|should|can|will|must)", "第一人称：'I need/want/...'"),
    (r"^(First|Next|Then|Finally|Also|Now),? [A-Za-z]", "序列思维：'First/Next/...'"),
    (r"^(Looking|Going|Checking|Reading|Based) [a-z]", "分词引导：'Looking at...'"),
    (r"^(This|That|It|There) [a-z].* (is|was|are|were|seems|appears)", "指示代词：'This is...'"),
    (r"^(We|You) (can|could|should|might|will|would|must)", "祈使/建议：'We can/You should...'"),
]

# 英文注释模式
COMMENT_PATTERNS = [
    (r"^\s*//\s*[A-Z][a-z]+ [a-z]+", "行注释英文"),
    (r"^\s*/\*\*\s*[A-Z][a-z]+", "Docstring 英文"),
    (r"^\s*#\s*[A-Z][a-z]+ [a-z]+", "Python 注释英文"),
    (r"^\s*/\*\s*[A-Z][a-z]+", "块注释英文"),
]

# 英文完整句模式（至少 5 个英文单词，含动词）
ENGLISH_SENTENCE = re.compile(
    r"\b[A-Z][a-z]+ [a-z]+ (is|are|was|were|will|would|can|could|should|may|might|has|have|had|does|do|did|says|said|goes|went|comes|came|makes|made|takes|took|gives|gave|finds|found|uses|used)\b",
    re.IGNORECASE,
)

# 豁免行（不算违规）
EXEMPT_PATTERNS = [
    re.compile(r"^```"),           # 代码块标记
    re.compile(r"^\s*$"),          # 空行
    re.compile(r"^\s*[#*/\s-]+$"), # 纯符号行
    re.compile(r"^[a-z_]+\("),    # 函数调用
    re.compile(r"^(import|from|export|const|let|var|function|class|def|return|if|for|while) "),  # 代码关键字
    re.compile(r"^(curl|git|npm|yarn|docker|kubectl|ssh|cd|ls|mkdir|rm|cp|mv) "),  # CLI 命令
    re.compile(r"^(feat|fix|docs|style|refactor|perf|test|chore|ci|build)[(:]"),  # Commit type
    re.compile(r"^\|"),           # 表格行
]


def is_exempt(line: str) -> bool:
    """检查是否为豁免行（代码块、命令、表格等）。"""
    for pattern in EXEMPT_PATTERNS:
        if pattern.search(line):
            return True
    return False


def scan_file(filepath: str) -> list[dict]:
    """扫描文件，返回违规列表。"""
    violations = []
    path = Path(filepath)
    if not path.exists():
        print(f"错误：文件不存在 — {filepath}", file=sys.stderr)
        sys.exit(2)

    lines = path.read_text(encoding="utf-8").split("\n")
    in_code_block = False

    for i, line in enumerate(lines, start=1):
        # 跟踪代码块
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if is_exempt(line):
            continue

        # 检查 thinking 红灯句式
        for pattern, desc in THINKING_RED_FLAGS:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append({
                    "line": i,
                    "type": "thinking",
                    "pattern": desc,
                    "content": line.strip()[:80],
                })
                break  # 每行只报一次

        # 检查英文注释
        for pattern, desc in COMMENT_PATTERNS:
            if re.search(pattern, line):
                violations.append({
                    "line": i,
                    "type": "comment",
                    "pattern": desc,
                    "content": line.strip()[:80],
                })
                break

        # 检查英文完整句
        match = ENGLISH_SENTENCE.search(line)
        if match:
            # 避免和上面的 thinking/comment 重复报告
            already_reported = any(v["line"] == i for v in violations[-5:])
            if not already_reported:
                violations.append({
                    "line": i,
                    "type": "sentence",
                    "pattern": f"英文完整句: ...{match.group(0)}...",
                    "content": line.strip()[:80],
                })

    return violations


def print_report(violations: list[dict], filepath: str):
    """打印人类可读的报告。"""
    if not violations:
        print(f"✅ {filepath} — 零违规")
        return

    print(f"❌ {filepath} — 发现 {len(violations)} 处违规\n")

    # 按类型分组
    by_type = {}
    for v in violations:
        by_type.setdefault(v["type"], []).append(v)

    for vtype, items in by_type.items():
        type_names = {
            "thinking": "🧠 thinking 块违规",
            "comment": "💬 代码注释违规",
            "sentence": "📝 英文完整句违规",
        }
        print(f"## {type_names.get(vtype, vtype)} ({len(items)} 处)")
        for item in items:
            print(f"  第 {item['line']} 行: {item['pattern']}")
            print(f"    → {item['content']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="中文化审计脚本")
    parser.add_argument("file", help="要扫描的文件路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--fix", action="store_true", help="标记违规位置（不修改文件）")
    args = parser.parse_args()

    violations = scan_file(args.file)

    if args.json:
        print(json.dumps(violations, ensure_ascii=False, indent=2))
    else:
        print_report(violations, args.file)
        if violations:
            print(f"共 {len(violations)} 处违规。")
            if args.fix:
                print("提示：--fix 模式暂不支持自动修改，请手动整改。")

    sys.exit(1 if violations else 0)


if __name__ == "__main__":
    main()
