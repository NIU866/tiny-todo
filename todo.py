#!/usr/bin/env python3
"""Tiny Todo：只使用 Python 标准库的本地待办清单。"""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


DEFAULT_FILE = Path.home() / ".tiny-todo" / "tasks.json"


class TodoError(Exception):
    """可以直接展示给用户的错误。"""


def load_data(path):
    """读取并校验数据；损坏的数据不会被自动覆盖。"""
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {"next_id": 1, "tasks": []}
    try:
        data = json.loads(raw)
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise TodoError(f"数据文件无法解析，请先检查或备份：{path}") from exc

    valid = isinstance(data, dict) and isinstance(data.get("tasks"), list)
    ids = set()
    if valid:
        for task in data["tasks"]:
            if (
                not isinstance(task, dict)
                or type(task.get("id")) is not int
                or task["id"] < 1
                or task["id"] in ids
                or not isinstance(task.get("text"), str)
                or not task["text"].strip()
                or type(task.get("done")) is not bool
            ):
                valid = False
                break
            ids.add(task["id"])
    if (
        not valid
        or type(data.get("next_id")) is not int
        or data["next_id"] <= max(ids, default=0)
    ):
        raise TodoError(f"数据格式不正确，请先检查或备份：{path}")
    return data


def save_data(path, data):
    """先写同目录临时文件，再替换原文件，避免写到一半留下残缺 JSON。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=".todo-", suffix=".tmp", delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def find_task(data, task_id):
    for task in data["tasks"]:
        if task["id"] == task_id:
            return task
    raise TodoError(f"找不到任务 #{task_id}。请先运行 list 查看任务编号。")


def build_parser():
    parser = argparse.ArgumentParser(description="Tiny Todo · 简单的本地待办清单")
    parser.add_argument(
        "--file", type=Path, default=DEFAULT_FILE,
        help=f"数据文件路径（默认：{DEFAULT_FILE}）；放在子命令前",
    )
    commands = parser.add_subparsers(dest="command", title="子命令")
    add = commands.add_parser("add", help="添加任务")
    add.add_argument("text", help="任务内容；包含空格时请加引号")
    listing = commands.add_parser("list", help="查看任务")
    listing.add_argument("--status", choices=["all", "todo", "done"], default="all",
                         help="all=全部，todo=未完成，done=已完成")
    for name, help_text in [("done", "标记完成"), ("undo", "恢复为未完成"),
                            ("remove", "删除任务")]:
        command = commands.add_parser(name, help=help_text)
        command.add_argument("id", type=int, help="任务编号")
        if name == "remove":
            command.add_argument("-y", "--yes", action="store_true", help="跳过删除确认")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0

    try:
        path = args.file.expanduser()
        data = load_data(path)
        if args.command == "list":
            tasks = [task for task in data["tasks"] if args.status == "all"
                     or task["done"] == (args.status == "done")]
            if not tasks:
                print("没有符合条件的任务。试试：python todo.py add \"发布第一个 GitHub 项目\"")
            for task in tasks:
                mark = "x" if task["done"] else " "
                print(f"[{mark}] #{task['id']}  {task['text']}")
            return 0

        if args.command == "add":
            text = args.text.strip()
            if not text:
                raise TodoError("任务内容不能为空。")
            task = {"id": data["next_id"], "text": text, "done": False}
            data["tasks"].append(task)
            data["next_id"] += 1
            message = f"已添加 #{task['id']}：{text}"
        else:
            task = find_task(data, args.id)
            if args.command == "remove":
                if not args.yes:
                    try:
                        answer = input(f"删除 #{task['id']}「{task['text']}」？[y/N] ")
                    except EOFError:
                        answer = ""
                    if answer.strip().lower() != "y":
                        print("已取消删除。")
                        return 0
                data["tasks"].remove(task)
                message = f"已删除 #{task['id']}。"
            else:
                task["done"] = args.command == "done"
                state = "已完成" if task["done"] else "未完成"
                message = f"#{task['id']} 已设为{state}。"
        save_data(path, data)
        print(message)
        return 0
    except (TodoError, OSError, UnicodeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n已取消。", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
