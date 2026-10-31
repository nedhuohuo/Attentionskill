"""Standard-library checks for packaging only; not an agent-behavior test."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/requirements-ledger/SKILL.md"
TEMPLATE = ROOT / "skills/requirements-ledger/templates/ledger.md"


class PackageTests(unittest.TestCase):
    def read_required(self, file):
        self.assertTrue(file.is_file(), f"missing deliverable: {file.relative_to(ROOT)}")
        return file.read_text(encoding="utf-8")

    def test_skill_metadata(self):
        text = self.read_required(SKILL)
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        self.assertIsNotNone(match, "SKILL.md needs YAML frontmatter")
        metadata = dict(line.split(":", 1) for line in match[1].splitlines())
        name = metadata["name"].strip()
        description = metadata["description"].strip()
        self.assertEqual(name, SKILL.parent.name)
        self.assertRegex(name, r"^[a-z][a-z0-9-]{0,63}$")
        self.assertTrue(description.startswith("Use when"))
        self.assertLessEqual(len(match[1]), 1024)
        self.assertLessEqual(len(text.splitlines()), 180)

    def test_template_contract(self):
        text = self.read_required(TEMPLATE)
        for field in ("编号", "内容", "确认状态", "落实状态", "来源", "疑问", "变更", "继续入口", "未归位"):
            with self.subTest(field=field):
                self.assertIn(field, text)
        guide = self.read_required(SKILL)
        for state in ("待确认", "已明确", "待处理", "进行中", "已完成", "暂缓", "已取消", "不适用"):
            with self.subTest(state=state):
                self.assertIn(state, guide)
        self.assertIn("templates/ledger.md", guide)

    def test_relative_markdown_links(self):
        files = [ROOT / "README.md", SKILL, TEMPLATE]
        for file in files:
            text = self.read_required(file)
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
                if "://" in target or target.startswith("#"):
                    continue
                target = target.split("#", 1)[0]
                with self.subTest(file=str(file.relative_to(ROOT)), target=target):
                    self.assertTrue((file.parent / target).is_file(), "broken local link")

    def test_readme_documents_installation_and_limits(self):
        text = self.read_required(ROOT / "README.md")
        for section in ("安装", "使用", "隐私", "验证", "不保证"):
            with self.subTest(section=section):
                self.assertIn(section, text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
