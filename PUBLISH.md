# 把 Tiny Todo 发布到 GitHub

建议仓库名：`tiny-todo`

建议描述：`一个零第三方依赖的 Python 命令行待办清单，支持本地 JSON 存储。`

发布代码后，访问者可以查看、下载代码；这个项目通过本地终端运行。

## 方式一：网页上传

适合第一次使用 GitHub，还不熟悉 Git 命令的情况。

1. 下载并解压项目压缩包，进入 `tiny-todo` 文件夹。
2. 登录 GitHub，打开 [创建仓库页面](https://github.com/new)。
3. 仓库名填 `tiny-todo`，填写描述。希望所有人都能看到时选择 **Public**；只自己查看时选择 **Private**。
4. 保持新仓库为空：不要额外创建 README、`.gitignore` 或许可证文件，点击 **Create repository**。
5. 在空仓库提示中点击 **uploading an existing file**；已有文件的仓库可以点 **Add file → Upload files**。
6. 把解压后 `tiny-todo` 文件夹里面的文件和 `tests` 文件夹拖入上传区。直接上传压缩包只会保存 ZIP，无法把代码文件展开为仓库目录。
7. 确认仓库根目录会出现 `todo.py`、`README.md`、`PUBLISH.md`、`.gitignore` 和 `tests/test_todo.py`。部分系统会隐藏 `.gitignore`，请显示隐藏文件后一起上传。不要上传运行产生的 `tasks.json`。
8. 提交说明填 `Initial commit: add Tiny Todo`，按页面按钮完成提交。
9. 回到仓库首页，检查 README 正常显示、可以打开 `todo.py`。复制浏览器地址栏中的仓库链接即可分享。

## 方式二：使用 Git

已安装 Git 时，在解压后的 `tiny-todo` 文件夹打开终端。

首次使用 Git 时，先设置提交署名；把示例值替换成自己的名字和提交邮箱。需要隐藏真实邮箱时，可以使用 GitHub 邮箱设置页提供的 noreply 邮箱。

```bash
git config --global user.name "你的名字"
git config --global user.email "你的提交邮箱"
```

在 GitHub 创建一个空的 `tiny-todo` 仓库，不额外创建 README、`.gitignore` 或许可证文件。然后运行：

```bash
git init -b main
git add .
git commit -m "Initial commit: add Tiny Todo"
```

把下一行中的 `YOUR_USERNAME` 换成你的 GitHub 用户名，再运行：

```bash
git remote add origin https://github.com/YOUR_USERNAME/tiny-todo.git
git push -u origin main
```

首次推送需要按 Git 的提示完成 GitHub 身份验证。完成后刷新仓库页面。

以后修改代码后，可以继续提交：

```bash
git add .
git commit -m "Describe your change"
git push
```

## 官方参考

- [创建仓库](https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories)
- [网页上传文件](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
- [把本地代码推送到 GitHub](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)
