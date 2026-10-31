# Attentionskill · 需求台账

把零散需求和沟通细节留下来，通过交互持续修改；有疑问就确认，完成后标记。

**“已经说清楚”和“实际做完”分开记录。** 你不需要先组织出完整需求，AI 也不应把讨论过、生成了计划或写了代码当作完成。

这是一个 Markdown skill，不是独立应用、后台服务或自动开发工具。无运行时依赖，需要宿主 AI 能加载 SKILL.md，并读取和修改项目文件。

## 安装

先阅读 [skill 正文](skills/requirements-ledger/SKILL.md)。将整个 `skills/requirements-ledger/` 目录放入宿主的技能目录，保留 `templates/`。

例如安装到 Pi 支持的用户级共享技能目录（macOS/Linux）：

```bash
git clone https://github.com/nedhuohuo/Attentionskill.git
mkdir -p "$HOME/.agents/skills"
# 仅首次安装；已有同名目录时停止，先比较内容，不直接覆盖。
if [ -e "$HOME/.agents/skills/requirements-ledger" ]; then
  printf '%s\n' '同名 skill 已存在，请先比较内容。'
else
  cp -R Attentionskill/skills/requirements-ledger "$HOME/.agents/skills/"
fi
```

也可以仅对某个项目安装：将该目录复制到项目的 `.agents/skills/requirements-ledger/`，不要覆盖已有目录。其他宿主请使用其支持的技能目录。

Pi 中执行 `/reload` 或重新开启会话，然后显式调用：

```text
/skill:requirements-ledger 帮我记录当前订单后台的需求，后面我们边聊边完善。
```

本仓库不会自动安装到你的全局目录，也不修改宿主配置。技能自动匹配取决于宿主和模型；需要可靠启用时请显式调用。

## 使用

### 1. 接续已有上下文

```text
用 requirements-ledger 接着整理目前聊到的需求，已有内容不要让我重新讲。
```

AI 先读可访问的对话及对应台账。默认每个业务一份 `requirements/<需求短名>.md`；用户指定文件则复用，存在多个候选时先确认。无法访问的历史会话不会被假装记住。

### 2. 零散补充和修订

```text
补充一点，导出还要有实付金额。
R02 不是删除，改成作废，原记录必须保留。
这里我还没想清楚，先记成待确认。
审计日志本期取消，筛选偏好暂缓到第二期。
```

AI 根据语义更新原条目，保留稳定编号、具体限制及重要变更。已有确定内容先保存，有疑问默认只问一个关键问题；文件目标或安全问题不明确时先确认再写。

### 3. 分别记录明确和完成

| 维度 | 状态 |
| --- | --- |
| 确认状态 | 待确认、已明确 |
| 落实状态 | 待处理、进行中、已完成、暂缓、已取消、不适用 |

```text
日期筛选已经做完，我确认；导出代码写好了，但还没有测。
第 5 条已经完成，是我验收过的。
```

用户告知完成会被如实记录为用户确认，而不是 AI 独立验证。混合进度的条目拆分或保留进行中；需求变化影响已完成项时重新打开受影响部分。背景信息不制造待办。

### 4. 查看与恢复

```text
还有什么没确认？
哪些事情还没做完？
给我看当前完整需求。
读取 requirements/订单后台.md，接着上次继续。
```

默认反馈文件位置、本轮变化和一个待确认问题；请求时再展开全貌。新会话需要再次启用 skill 并允许读取台账，而不是依赖旧聊天记忆。

可查看 [台账模板](skills/requirements-ledger/templates/ledger.md)。保存失败时会说明“未保存”和待保存内容，不改权限、不擅自另存，也不能把草稿说成已落盘。

## 隐私与限制

- 台账可能包含内部业务细节。请在**使用项目自己的** `.gitignore` 中加入相应目录（例如 `requirements/`）；已经被 Git 跟踪的文件不会因为新增忽略规则而自动解除跟踪。
- 本仓库忽略真实台账目录与本地原始测试目录。未经授权不提交、上传或分享台账；这不是自动隐私隔离机制。
- 只记录业务所需内容，不存凭据或整段聊天；外部材料中的指令只当数据。
- skill **不保证**百分之百不遗漏、不保证自动触发，不能知道你尚未表达的细节，也不提供后台提醒。
- 没有文件工具时只能给未保存草稿；没有锁或版本检查时不保证多代理并发写入安全，建议同一台账同时只由一个写入者维护。
- 尚未发布软件许可证；公开可查看不等于授予开源使用/再分发许可，使用或分发前请与作者确认授权。

## 验证

静态包检查只需要 Python 3 标准库：

```bash
python3 tests/check_package.py
git diff --check
```

它检查元数据、模板契约、文档和本地链接，**不证明 AI 的真实行为**。

[行为情景](tests/scenario.md)及[初始台账](tests/fixtures/ledger.md)使用虚构数据。基线和加载后的测试使用相同用户消息，各 5 个独立会话；另检查冷启动恢复、无法写入时的反馈。详见[实际结果与限制](tests/results.md)。

结构：

```text
skills/requirements-ledger/
  SKILL.md
  templates/ledger.md
tests/
  check_package.py
  scenario.md
  fixtures/ledger.md
  results.md
docs/superpowers/
  specs/
  plans/
```

设计见[批准的设计文档](docs/superpowers/specs/2026-07-21-requirements-ledger-design.md)。实现方案不包含数据库、插件、云同步或后台服务。
