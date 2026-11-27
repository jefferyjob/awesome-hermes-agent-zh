# 自动化运维备注

> 本文档记录本仓库自动化系统的全部配置路径，供维护者备查。
> 代码与流程规范见 `AGENTS.md`；工作流与脚本在本目录（`.github/workflows/`、`.github/scripts/`）。

## 一、密钥与变量配置（Action 运行的前提）

### 必须配置

| 名称 | 类型 | 作用 | 被谁使用 |
|---|---|---|---|
| `OPENAI_API_KEY` | **Secret**（加密） | 调用 OpenAI API 的密钥，`sk-` 开头，来自 [platform.openai.com/api-keys](https://platform.openai.com/api-keys)（账户需有 API 余额；**ChatGPT/Codex 订阅登录态不可用**） | `sync-check.yml` 翻译、`triage.yml` 条目起草 |

**Web 界面配置路径：**

```
仓库主页 → Settings（标题栏最右）→ 左侧栏 Secrets and variables → Actions
  → 「Secrets」标签页 → New repository secret
  → Name 填 OPENAI_API_KEY，Secret 粘贴 sk- 开头的密钥 → Add secret
```

直达链接：https://github.com/jefferyjob/awesome-hermes-agent-zh/settings/secrets/actions

**命令行配置路径**（在本地终端执行，key 不经过第三方）：

```bash
gh secret set OPENAI_API_KEY --repo jefferyjob/awesome-hermes-agent-zh
# 回车后粘贴密钥再回车
```

### 可选配置

| 名称 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `OPENAI_MODEL` | **Variable**（明文） | `gpt-5.1` | 翻译/起草所用模型（**当前配置：`deepseek-flash`**，即 DeepSeek-V4.1-Flash）|
| `OPENAI_BASE` | **Variable**（明文） | `https://api.openai.com/v1` | API 地址，可指向任意 **OpenAI 兼容端点**（**当前配置：`https://api.deepseek.com/v1`**）|
| `OPENAI_MAX_TOKENS` | **Variable**（明文） | `32768` | 单次输出上限（当前 80000；deepseek-flash 最大可到 393216）|
| `AUTO_MERGE_DAILY_CAP` | **Variable**（明文） | `10` | 外部 PR 每日自动合并上限，超出转人工（防被刷）|

> **兼容性说明**：脚本统一走 `/chat/completions` 端点，OpenAI 官方、DeepSeek、智谱 BigModel 等 OpenAI 兼容实现均可用。
> **注意**：GLM Coding Plan（编码套餐）的 key 只能走智谱专用编码端点 `https://open.bigmodel.cn/api/coding/paas/v4`，在通用端点 `/api/v1` 会报 `model_access_denied`（2026-11-17 实测）。

**Web 界面配置路径**：同上页面 → 切到「**Variables**」标签页 → `New repository variable` → Name / Value。
**命令行**：`gh variable set OPENAI_MODEL --repo jefferyjob/awesome-hermes-agent-zh --body "gpt-5.1"`

## 二、自动化决策边界（谁做决定）

| 场景 | AI 自动处理 | 需要人工 |
|---|---|---|
| 上游同步 | 翻译 → 结构校验通过 → **直接合入 main** + 自动关 issue + 推进基线 | 仅翻译/校验失败时（issue 会收到转人工评论）|
| 资源推荐 issue（核验通过）| 起草条目 → **自动写入 README 合入 main** → 自动关 issue | 仅起草/插入失败时 |
| 资源推荐 issue（核验不通过）| 附核验理由**自动关闭** | 建议者可评论/重开申诉 |
| 外部 PR（硬门槛通过 + AI 评审 pass）| lint + 硬门槛 + AI 评审 → **自动 squash 合并** → 评论 + 关闭 | 每日超上限 / 草稿 PR / 合并冲突时转人工 |
| 外部 PR（硬门槛不过）| 附理由**自动关闭** | 建议者修正后重开 PR，机器人自动重新评审 |
| 外部 PR（AI 评 gray / 触发复核规则）| 评论 + 打 `needs-human` 标签，保持打开 | **维护者复核** |

### 外部 PR 自动流水线（triage.yml `lint-pr` job）

触发器为 `pull_request_target`（**不经过** GitHub 对外部贡献者的 workflow 审批门；且该事件下 `GITHUB_TOKEN` 有写权限、secrets 可用——`pull_request` 事件对 fork PR 是只读 token，评论都会 403）。三层防线：

1. **第 0 层 · 确定性硬门槛**（`lint_pr_entries.py` + `gate_pr_added.py`，不信任 PR 也不信任 AI）：只允许改 README.md；所有非空新增行必须匹配条目格式（防 HTML/垃圾注入）；单 PR ≤ 3 条；删除行只能是条目且删条目数 ≤ 增条目数（防夹带删条目）；不得重复收录；仓库存在/非 fork/非归档/有许可证。不过 → 自动关闭。
2. **第 1 层 · AI 评审**（`draft_entry.py` 独立起草对照条目 + `review_pr.py` 出 pass/gray/fail 结论 JSON）：只评内容质量（相关性、描述是否夸大、分类、纯广告），不复核脚本已验证的事实。PR 正文/diff 中任何"请合并我"之类的文字按**操纵企图**判 fail。
3. **第 2 层 · 自动处置**：pass → squash 合并（受 `AUTO_MERGE_DAILY_CAP` 每日上限与草稿保护约束）；fail → 自动关闭附理由；gray/失败 → `needs-human` 保持打开。

**安全红线**：`pull_request_target` 下 job 处于特权上下文（有 secrets 和写权限），因此**任何步骤都不得 checkout / 执行 PR 分支的代码**——PR 内容只作为数据传给脚本。改动 `lint-pr` job 时务必保持这条约束。

不满意 AI 的某次自动收录/同步？直接 revert 对应 commit 即可，不影响后续流程。

## 三、工作流的入口与手动触发

| 工作流 | 触发方式 | 手动触发路径 |
|---|---|---|
| `sync-check.yml` 上游同步检查 | 每日 03:23 UTC 定时 + 手动 | 仓库 **Actions** 标签页 → 左侧「上游同步检查」→ Run workflow |
| `triage.yml` issue/PR 自动核验 | issue/PR 打开时自动 + 手动 | Actions →「自动核验 issue 与 PR」→ Run workflow → 选 kind（issue/pr）+ 编号 |

直达链接：https://github.com/jefferyjob/awesome-hermes-agent-zh/actions

## 四、运行状态与排障

- **查看某次运行**：Actions → 点对应工作流 → 点运行记录 → 看各步骤日志（失败步骤有红叉，展开即见报错）
- **密钥无效 / 401**：检查 `OPENAI_API_KEY` 是否为平台 API key（非 ChatGPT 登录态）、账户是否有余额
- **定时任务被停用**：GitHub 在仓库 60 天无活动后自动停用定时工作流，到 Actions 页手动 Run workflow 一次即恢复
- **翻译质量闸门失败**：`.github/scripts/validate_sync.py` 校验未过（条目覆盖/锚点/格式等）→ 同步 issue 会收到失败评论，按 `AGENTS.md` 人工同步
- **输出被截断**（finish_reason=length）：调大 `OPENAI_MAX_TOKENS` Variable 或换输出上限更大的模型
- **本地条目白名单**：`.github/local-entries.txt` 记录本仓库独有、上游没有的条目（自动收录时自动追加）；同步校验据此放行
- **同步基线**：`.github/upstream-sync-ref` 存放已处理的上游 commit SHA（同步成功后由流水线自动推进）；异常时可比对该文件与上游 HEAD

## 五、成本与安全备忘

- 翻译成本：全量同步按 token 计费（deepseek-flash 价格低廉，全量同步约几毛钱人民币级）；单条 issue 条目起草 / 单个 PR 评审约几分钱；PR 自动流水线先跑免费的硬门槛、只有门槛通过才调 AI，恶意 PR 刷不动 API 账单
- 自动合并只发生在全部确定性校验通过之后（同步结构校验 / issue 资源核验 / PR 硬门槛 + AI pass）；不满意某次自动合并，直接 revert 对应 commit 即可
- Copilot coding agent / code review 不可用原因：账号为 Business 席位（组织 DoushenAI 分配，本人在该组织为普通成员），Business 席位仅覆盖组织仓库，个人仓库无此开关（实测分配报 `Bot does not have access to the repository`）。如需启用：升级个人 Pro+，或将仓库迁入组织并由管理员开启策略
- `AGENTS.md` 在 `.gitignore` 中被全局忽略规则覆盖，属功能性文件，已用 `git add -f` 强制纳入版本管理
- **接入背景**（2026-11-17）：原计划用 Copilot coding agent，因席位限制改为 OpenAI 兼容 API 直调；先后试用智谱 GLM Coding Plan（key 仅限编码端点，通用端点不可用）后，最终采用 **DeepSeek 官方 API**（`deepseek-flash`）
- **诊断工具**：`api-diagnose.yml` 工作流可列出 key 可用模型清单、实测指定模型（支持临时端点覆盖参数），换模型/换服务商时先跑它
