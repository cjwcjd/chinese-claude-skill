import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "audit-chinese.py"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("audit_chinese", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditChineseTests(unittest.TestCase):
    def setUp(self):
        self.audit = load_audit_module()
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.tmp = Path(self.tmpdir.name)

    def write_text(self, name, content, encoding="utf-8"):
        path = self.tmp / name
        path.write_text(content, encoding=encoding)
        return path

    def test_detects_bom_prefixed_thinking_red_flag(self):
        path = self.write_text(
            "bom.md",
            "\ufeffLet me think about this carefully.\n",
        )

        violations = self.audit.scan_file(str(path))

        self.assertEqual(violations[0]["type"], "thinking")
        self.assertEqual(violations[0]["line"], 1)

    def test_detects_english_markdown_heading(self):
        path = self.write_text("heading.md", "## Installation\n中文正文。\n")

        violations = self.audit.scan_file(str(path))

        self.assertEqual(violations[0]["type"], "document")
        self.assertEqual(violations[0]["line"], 1)

    def test_detects_english_markdown_heading_after_icon(self):
        path = self.write_text("icon-heading.md", "## 📄 License\n")

        violations = self.audit.scan_file(str(path))

        self.assertEqual(violations[0]["type"], "document")
        self.assertEqual(violations[0]["line"], 1)

    def test_report_does_not_crash_on_non_utf8_stdout(self):
        stream = io.TextIOWrapper(io.BytesIO(), encoding="cp936", errors="strict")

        with redirect_stdout(stream):
            self.audit.print_report([], "transcript.md")

        stream.flush()

    def test_ignores_english_inside_fenced_code_blocks(self):
        path = self.write_text(
            "code.md",
            "```js\n// Cache user data\nconst message = 'This should stay English.';\n```\n",
        )

        violations = self.audit.scan_file(str(path))

        self.assertEqual(violations, [])


if __name__ == "__main__":
    unittest.main()
