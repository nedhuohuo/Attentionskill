# Requirements Ledger Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Implementation stays in the parent session; independent children are authorized only for tests.

**Goal:** 交付能持续记录、修订、确认并标记落实情况的需求台账 skill。

**Architecture:** 一个自包含 SKILL.md 加一份 Markdown 台账模板。由宿主代理直接读写项目文档，不增加运行时服务。

**Tech Stack:** Markdown、Python 3 标准库检查、Git/GitHub CLI。

**Spec:** `docs/superpowers/specs/2026-07-21-requirements-ledger-design.md`

## Global Constraints

- 确认状态：`待确认`、`已明确`。
- 落实状态：`待处理`、`进行中`、`已完成`、`暂缓`、`已取消`、`不适用`。
- 一个业务一份台账，稳定编号；推测不是确认，说清楚不是做完。
- 不实现数据库、插件、后台提醒、自动开发或云同步。
- 子代理仅用于隔离行为测试；实现由当前会话完成。
- 公开仓库 `nedhuohuo/Attentionskill`；不发布真实业务台账、凭据或原始日志。

## Task 1: 建立失败基线

**Files:** 创建 `tests/scenario.md`、`tests/check_package.py`；测试工作目录为忽略的 `.test-runs/`。
**Interfaces:** 输入虚构订单业务与相同的历史台账，输出更新台账、简短反馈及人工评分证据。

- [ ] 编写压力场景：交接时间紧、已有完成记录、新旧规则冲突，包含混合完成、未确认推测和必须保留的细节。
- [ ] 在 5 个独立目录中不加载 skill 执行相同情景；评估遗漏与不当状态变化，摘录真实失败，保留原始产物但不发布日志。
- [ ] 编写标准库包检查并运行 `python3 tests/check_package.py`，确认在包尚未实现时因缺少交付物失败。
- [ ] 如所有基线均满足全部目标，不伪造失败；报告结果并调整必要范围。

## Task 2: 实现最小 skill 包

**Files:** 创建 `skills/requirements-ledger/SKILL.md`、`skills/requirements-ledger/templates/ledger.md`、`README.md`。
**Interfaces:** 宿主加载 SKILL.md 并按相对链接读取模板；业务台账默认 `requirements/<需求名>.md`。

- [ ] SKILL.md 写入触发条件、双状态、增量更新、疑问确认、完成依据、重新打开、恢复与保存失败处理。
- [ ] 模板定义索引与细节的相同编号、来源/依据、疑问/变更、未归位片段和继续入口。
- [ ] README 提供复制安装、显式启用、交互示例、恢复方式、隐私与不支持事项；不声称自动激活或全局安装已完成。
- [ ] 运行 `python3 tests/check_package.py`，检查结构和本地引用。
- [ ] 使用同样场景在 5 个独立目录加载 skill 运行，人工逐项检查真实文件，失败则以观察到的偏差修改并重测。

## Task 3: 边界验证与发布

**Files:** 创建 `tests/results.md`；按实际验证结果更新本计划和设计。
**Interfaces:** 输入原始测试产物，输出不含机器路径和用户数据的人工审阅结论；发布 Git commit 与仓库 URL。

- [ ] 在独立测试会话中检查断点恢复和不可写目录的保存失败；不得修改权限控制或改写其他位置绕过失败。
- [ ] 记录样本数、模型/方法、逐项结果、观察到的失败与未验证边界，不把静态检查当行为成功。
- [ ] 人工自审契约、模板、文档、测试覆盖；运行包检查及 `git diff --check`，扫描提交中的敏感信息。
- [ ] `git add` 明确交付文件并提交；创建公开仓库、将交付分支推为 main，设置跟踪分支。
- [ ] 通过 GitHub API 确认可见性，并比较远端 main SHA 与本地 HEAD；如推送失败明确报告，不声称已发布。
