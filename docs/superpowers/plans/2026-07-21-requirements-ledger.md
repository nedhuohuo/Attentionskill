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

- [x] 编写压力场景：交接时间紧、已有完成记录、新旧规则冲突，包含混合完成、未确认推测和必须保留的细节。
- [x] 在 5 个独立目录中不加载 skill 执行相同情景；评估遗漏与不当状态变化，保留原始产物但不发布日志。10 项语义检查均通过，未伪造失败；补充记录复合状态与目标契约的差异。
- [x] 编写标准库包检查并运行 `python3 tests/check_package.py`，确认在包尚未实现时因缺少交付物失败（4 个预期失败）。
- [x] 报告基线通过的结果，将本次交付定位为标准化台账协议，不宣称已证明降低遗漏。

## Task 2: 实现最小 skill 包

**Files:** 创建 `skills/requirements-ledger/SKILL.md`、`skills/requirements-ledger/templates/ledger.md`、`README.md`。
**Interfaces:** 宿主加载 SKILL.md 并按相对链接读取模板；业务台账默认 `requirements/<需求名>.md`。

- [x] SKILL.md 写入触发条件、双状态、增量更新、疑问确认、完成依据、重新打开、恢复与保存失败处理。
- [x] 模板定义索引与细节的相同编号、来源/依据、疑问/变更、未归位片段和继续入口。
- [x] README 提供复制安装、显式启用、交互示例、恢复方式、隐私与不支持事项；不声称自动激活或全局安装已完成。
- [x] 运行 `python3 tests/check_package.py`，4 项通过，结构和本地引用有效。
- [x] 使用同样场景在 5 个独立目录加载 skill 运行。首轮提供方限额中断且产物不一致，不计通过；获用户继续指示后同工具串行重试一次，5/5 完成并人工逐项审阅通过，无需修改 skill。

## Task 3: 边界验证与发布

**Files:** 创建 `tests/results.md`；按实际验证结果更新本计划和设计。
**Interfaces:** 输入原始测试产物，输出不含机器路径和用户数据的人工审阅结论；发布 Git commit 与仓库 URL。

- [x] 在独立测试会话中检查断点恢复和不可写目录的保存失败；恢复反馈正确但未生成测试附加的 RESPONSE.md，已注明；编辑实际返回 EACCES，原台账哈希不变，未绕过权限。
- [x] 记录样本数、模型/方法、逐项结果、观察到的失败与未验证边界，不把静态检查当行为成功。
- [x] 人工自审契约、模板、文档、测试覆盖；运行包检查及 `git diff --cached --check`，扫描提交中的敏感信息。
- [x] 明确暂存交付文件并提交实现 `d446941`；创建公开仓库 `https://github.com/nedhuohuo/Attentionskill`，推送 main，设置本地 main 跟踪 origin/main。
- [x] GitHub API 确认 visibility=PUBLIC、默认分支 main；首次发布远端 main SHA 与本地实现提交完全一致。收尾文档更新后再次重跑检查及远端核对。
