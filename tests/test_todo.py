"""从真实命令行入口验证功能和数据保护，不依赖第三方测试框架。"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "todo.py"


class TodoCLITests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.data_file = Path(self.temporary.name) / "data" / "tasks.json"

    def run_cli(self, *args, input_text=""):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--file", str(self.data_file), *args],
            input=input_text, capture_output=True, text=True, encoding="utf-8",
            timeout=10,
        )

    def test_add_complete_filter_and_undo_survive_restarts(self):
        self.assertEqual(self.run_cli("add", "写中文 README").returncode, 0)
        self.assertEqual(self.run_cli("add", "发布到 GitHub").returncode, 0)
        self.assertEqual(self.run_cli("done", "1").returncode, 0)
        result = self.run_cli("list", "--status", "done")
        self.assertEqual(result.returncode, 0)
        self.assertIn("[x] #1  写中文 README", result.stdout)
        self.assertNotIn("发布到 GitHub", result.stdout)
        result = self.run_cli("list", "--status", "todo")
        self.assertIn("[ ] #2  发布到 GitHub", result.stdout)
        self.assertNotIn("写中文 README", result.stdout)
        self.assertEqual(self.run_cli("undo", "1").returncode, 0)
        self.assertIn("[ ] #1", self.run_cli("list").stdout)

    def test_delete_requires_confirmation_and_ids_are_not_reused(self):
        self.run_cli("add", "第一个任务")
        result = self.run_cli("remove", "1")
        self.assertIn("已取消删除", result.stdout)
        self.assertIn("第一个任务", self.run_cli("list").stdout)
        self.assertEqual(self.run_cli("remove", "1", input_text="y\n").returncode, 0)
        self.assertIn("没有符合条件", self.run_cli("list").stdout)
        self.run_cli("add", "第二个任务")
        self.assertIn("#2", self.run_cli("list").stdout)
        self.assertEqual(self.run_cli("remove", "2", "--yes").returncode, 0)
        self.assertEqual(json.loads(self.data_file.read_text()) ["tasks"], [])

    def test_empty_task_is_rejected_without_creating_data(self):
        result = self.run_cli("add", "   ")
        self.assertEqual(result.returncode, 1)
        self.assertIn("不能为空", result.stderr)
        self.assertFalse(self.data_file.exists())

    def test_missing_id_does_not_change_existing_data(self):
        self.run_cli("add", "保留这条任务")
        before = self.data_file.read_bytes()
        result = self.run_cli("done", "999")
        self.assertEqual(result.returncode, 1)
        self.assertIn("找不到任务", result.stderr)
        self.assertEqual(self.data_file.read_bytes(), before)

    def test_corrupt_json_is_not_overwritten(self):
        self.data_file.parent.mkdir()
        self.data_file.write_bytes(b'{"tasks": [')
        before = self.data_file.read_bytes()
        result = self.run_cli("add", "不要覆盖旧数据")
        self.assertEqual(result.returncode, 1)
        self.assertIn("无法解析", result.stderr)
        self.assertEqual(self.data_file.read_bytes(), before)

    def test_invalid_schema_is_not_overwritten(self):
        self.data_file.parent.mkdir()
        for data in [[], {"tasks": []}, {"next_id": 0, "tasks": []},
                     {"next_id": 2, "tasks": [{"id": 1, "text": "任务", "done": "false"}]},
                     {"next_id": 1, "tasks": [{"id": 1, "text": "任务", "done": False}]}]:
            with self.subTest(data=data):
                self.data_file.write_text(json.dumps(data), encoding="utf-8")
                before = self.data_file.read_bytes()
                result = self.run_cli("add", "新任务")
                self.assertEqual(result.returncode, 1)
                self.assertEqual(self.data_file.read_bytes(), before)

    def test_missing_parent_is_created_and_write_errors_are_readable(self):
        self.assertEqual(self.run_cli("add", "自动建立目录").returncode, 0)
        self.assertTrue(self.data_file.is_file())
        blocker = Path(self.temporary.name) / "blocked"
        blocker.write_text("这里是文件", encoding="utf-8")
        self.data_file = blocker / "tasks.json"
        result = self.run_cli("add", "无法写入")
        self.assertEqual(result.returncode, 1)
        self.assertIn("错误：", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
