# AGENTS.md — 编码代理工作指引

本仓库是 [0xNyk/awesome-hermes-agent](https://github.com/0xNyk/awesome-hermes-agent) 的中文翻译与同步镜像，**正文内容以中文呈现，上游（英文）是唯一的内容事实来源**。

如果你（编码代理）被分配到本仓库的任务，请遵循以下规范。

---

## 一、上游同步流程（处理 `sync` 标签的 issue 时）

1. **拉取上游内容**：获取上游目标 commit（issue 正文中 `目标 SHA:` 指向的 commit）的这些文件：
   - `README.md`（核心，必须逐节比对）
   - `CONTRIBUTING.md`、`CHANGELOG.md`、`LICENSE`（如有变化）
   - README 中引用的 `assets/` 下**新增**图片（复制进本仓库 `assets/`，保持文件名不变）
2. **逐节比对**：上游 README 的每个章节（含目录、各列表分区、运维作战手册、进阶蓝图、页脚）与本仓库中文版逐一对比，把上游的所有差异翻译为中文合入。
3. **必须保留的本地适配项**（这些内容上游没有或不同，不要被上游覆盖）：
   - README 顶部“翻译自 awesome-hermes-agent 库，本仓库持续同步更新”声明
   - 「插件」分区中本地保留的 [Hermes Tweet](https://github.com/Xquik-dev/hermes-tweet) 条目
   - 「参与贡献」章节的 issue 链接指向本仓库 `jefferyjob/awesome-hermes-agent-zh`
   - 每个章节标题前的显式英文锚点 `<a id="..."></a>`（目录链接依赖它们）
   - 图片使用本仓库 `assets/` 的相对路径（不是 raw.githubusercontent URL）
4. **条目格式**：`- **[production|beta|experimental]** [名称](URL) by [作者](URL) - 中文描述`；成熟度标签、排序、分区归属一律跟随上游，描述忠实翻译，不增删事实。
5. **自检**：对每个列表分区统计 `- **[` 开头的条目数，与上游同分区数量核对（本地允许且仅允许多出 Hermes Tweet 一条）。锚点与目录链接要一一对应。
6. **许可证跟随上游**：上游当前为 CC BY 4.0；若上游变更许可证，同步变更本仓库 `LICENSE` 与 README 许可证章节。

### 提交规范

- 分支名：`sync/<目标SHA前7位>`
- PR 描述**必须包含**：`Closes #<同步issue编号>` 和一行 `Upstream-SHA: <完整的40位SHA>`（合并工作流依赖该行推进基线）
- 先开 **草稿 PR**，不要直接 push 到 `main`
- 不要关闭他人开启的 issue / PR；不要改动 `CONTRIBUTING.md`、`CODE_OF_CONDUCT.md` 的中文内容（除非上游对应文件发生变化）

## 二、收录新资源（处理资源推荐 issue 时）

按 `CONTRIBUTING.md` 的质量标准执行：

1. **先核验**推荐指向的仓库：存在、未归档、非 fork、有明确许可证、近期有维护、README 完整、未与现有条目重复。仓库核验脚本是 `.github/scripts/verify_resources.py`（triage 工作流会自动运行并评论结果，优先参考其结论）。
2. **条目格式**见上文；描述控制在 1–3 句，包含“它是什么 + 对 Hermes 用户的价值”，涉及凭据/付费/权限的要像上游一样写明边界。
3. **分类**按上游现有分区（社区技能 / agentskills.io 生态 / 插件 / 技能注册表 / 记忆提供方 / 工具与实用程序 / 部署 / 集成与桥接 / 检测与媒体取证 / 多 Agent / 领域应用 / 分叉衍生 / 指南文档）。
4. **新收录条目追加到对应分区末尾**，不要插入上游同步条目之间，以便后续同步 diff 干净。
5. **成熟度标签**保守判定：项目新（<3 个月）且无公开采用记录 → experimental；有发布/测试/文档但采用有限 → beta；仅当上游已给 production 或有明显生产证据 → production。
6. 收录后在 issue 评论收录位置（锚点链接）与标签理由；**不合规的推荐不要收录**，评论说明原因（无许可证 / 闭源推广 / 与 Hermes 或 agentskills.io 无关联等），由维护者关闭。

## 三、安全边界

- 只在 `README.md`、`assets/`、`LICENSE`、`.github/upstream-sync-ref` 范围内做内容变更；工作流与脚本变更需维护者明确要求。
- 不在仓库中引入密钥、远程安装脚本或未核验的外部代码。
- 所有输出（PR/评论）使用中文。
