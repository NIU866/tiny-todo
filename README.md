# Tiny Todo

一个简单的 Python 命令行待办清单。添加任务、标记完成、筛选列表，数据保存在本地。只使用 Python 标准库，不需要安装第三方依赖。

## 运行效果

```text
> python todo.py add "写好项目 README"
已添加 #1：写好项目 README

> python todo.py add "发布第一个 GitHub 项目"
已添加 #2：发布第一个 GitHub 项目

> python todo.py done 1
#1 已设为已完成。

> python todo.py list
[x] #1  写好项目 README
[ ] #2  发布第一个 GitHub 项目
```

上面的编号假设使用的是一份新的数据文件；实际操作时以列表中的编号为准。

## 快速开始

需要 Python 3.11 或更新版本。当前版本已在 Python 3.12 上验证。

1. 下载或克隆项目，进入包含 `todo.py` 的文件夹。
2. 在这个文件夹打开终端，运行：

```bash
python todo.py add "完成第一件小事"
python todo.py list
```

如果系统没有 `python` 命令，macOS / Linux 可尝试 `python3`，Windows 可尝试 `py`。后续命令也作相同替换。

## 常用命令

| 操作 | 命令 |
| --- | --- |
| 添加任务 | `python todo.py add "阅读十页书"` |
| 查看全部 | `python todo.py list` |
| 只看未完成 | `python todo.py list --status todo` |
| 只看已完成 | `python todo.py list --status done` |
| 标记完成 | `python todo.py done 1` |
| 恢复为未完成 | `python todo.py undo 1` |
| 删除任务（需输入 y 确认） | `python todo.py remove 1` |
| 跳过确认删除 | `python todo.py remove 1 --yes` |
| 查看帮助 | `python todo.py --help` |

任务编号从 1 开始，删除任务后不会重复使用旧编号。

## 数据保存在哪里

默认保存在用户主目录下的 `.tiny-todo/tasks.json`，换一个工作目录运行程序也能读取同一份清单。程序离线运行，不上传数据。

也可以指定数据文件；`--file` 要放在子命令前面：

```bash
python todo.py --file ./tasks.json add "使用独立清单"
python todo.py --file ./tasks.json list
```

备份时复制这份 JSON 文件即可。程序先写临时文件再替换原文件；如果发现 JSON 损坏或格式不正确，会报错并保留原文件。这个入门版本适合单人顺序操作，不支持多个进程同时修改同一份清单。

## 项目结构

| 文件 | 作用 |
| --- | --- |
| `todo.py` | 命令解析、任务操作和 JSON 存储 |
| `tests/test_todo.py` | 命令行功能与数据保护测试 |
| `PUBLISH.md` | GitHub 发布教程 |
| `.gitignore` | 忽略本地数据和临时文件 |

## 运行测试

在项目文件夹运行：

```bash
python -m unittest discover -s tests -v
```

测试使用独立的临时文件，不会修改你的真实清单。

## 可以练习的小改进

- 给任务增加优先级。
- 给任务增加截止日期。
- 把清单导出为 Markdown。

先完成一个小功能，再提交一次 Git commit，方便观察项目如何逐步变化。

准备发布时，按 [GitHub 发布教程](PUBLISH.md) 操作。
