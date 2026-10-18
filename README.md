# GitHub PR Helper

一个只包含 Skill 的 Codex/ChatGPT 插件，用于审查 GitHub Pull Request 和本地分支差异。它优先报告可验证的正确性、回归、安全和测试风险，并给出文件级证据与最小修复方向。

## 功能

- 读取 PR 的 base/head 范围，而不是只检查当前工作区。
- 审查调用方、兼容性、错误处理、安全边界和测试覆盖。
- 在安全且可执行时运行相关测试、类型检查或构建。
- 默认只输出审查结论，不修改代码、不提交 GitHub Review。

## 本地安装

在本仓库根目录执行：

```powershell
codex plugin marketplace add .
codex plugin add github-pr-helper@github-pr-helper-plugins
```

安装后新建 Codex 任务，然后输入：

```text
$github-pr-review 审查这个 Pull Request：<PR URL>
```

也可以直接描述任务，让 Codex 根据 Skill 描述自动选择。

## 通过 GitHub 安装

仓库发布到 GitHub 后，用户执行：

```powershell
codex plugin marketplace add <OWNER>/<REPO>
codex plugin add github-pr-helper@github-pr-helper-plugins
```

不要添加 `--sparse .agents/plugins`，因为本插件的实际文件位于仓库的 `plugins/` 目录。

## 仓库结构

```text
github-pr-helper-plugin/
├── .agents/plugins/marketplace.json
├── plugins/github-pr-helper/
│   ├── plugin.json
│   ├── .codex-plugin/plugin.json
│   └── skills/github-pr-review/SKILL.md
├── scripts/validate_repo.py
└── .github/workflows/validate.yml
```

`plugin.json` 是便携式 Agent Plugins 清单；`.codex-plugin/plugin.json` 是 Codex 兼容清单。

## 验证

```powershell
python scripts/validate_repo.py
```

GitHub Actions 会在每次 push 和 pull request 时运行同一套检查。

## 发布前修改

发布到公共目录前，请补充真实作者、仓库地址、网站、隐私政策与服务条款，并按 OpenAI 插件提交要求打包 ZIP。
