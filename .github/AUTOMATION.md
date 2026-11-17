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
| `OPENAI_MODEL` | **Variable**（明文） | `gpt-5.1` | 翻译/起草所用模型，可在 Variable 里改 |
| `OPENAI_BASE` | **Variable**（明文） | `https://api.openai.com/v1` | API 地址，可指向任意 **OpenAI 兼容端点**（当前配置：智谱 `https://open.bigmodel.cn/api/v1`）|
| `OPENAI_MAX_TOKENS` | **Variable**（明文） | `32768` | 单次输出上限，报「输出被截断」时调大 |

> **兼容性说明**：脚本统一走 `/chat/completions` 端点，OpenAI 官方与智谱 BigModel 等 OpenAI 兼容实现均可用。智谱有 `/api/v1` 与 `/api/paas/v4` 两个兼容端点（实测均有效），使用智谱时 `OPENAI_MODEL` 填 GLM 系列模型名（如 `glm-5.3-flash`）。

**Web 界面配置路径**：同上页面 → 切到「**Variables**」标签页 → `New repository variable` → Name / Value。
**命令行**：`gh variable set OPENAI_MODEL --repo jefferyjob/awesome-hermes-agent-zh --body "gpt-5.1"`

## 二、自动化决策边界（谁做决定）

| 场景 | AI 自动处理 | 需要人工 |
|---|---|---|
| 上游同步 | 翻译 → 结构校验通过 → **直接合入 main** + 自动关 issue + 推进基线 | 仅翻译/校验失败时（issue 会收到转人工评论）|
| 资源推荐 issue（核验通过）| 起草条目 → **自动写入 README 合入 main** → 自动关 issue | 仅起草/插入失败时 |
| 资源推荐 issue（核验不通过）| 附核验理由**自动关闭** | 建议者可评论/重开申诉 |
| 外部 PR | 仅 lint + 核验 + 评论 + 标签 | **合并由人工决定**（内容注入风险）|

不满意 AI 的某次自动收录/同步？直接 revert 对应 commit 即可，不影响后续流程。

## 三、工作流的入口与手动触发

| 工作流 | 触发方式 | 手动触发路径 |
|---|---|---|
| `sync-check.yml` 上游同步检查 | 每日 03:23 UTC 定时 + 手动 | 仓库 **Actions** 标签页 → 左侧「上游同步检查」→ Run workflow |
| `triage.yml` issue/PR 自动核验 | issue/PR 打开时自动 + 手动 | Actions →「自动核验 issue 与 PR」→ Run workflow → 选 kind（issue/pr）+ 编号 |

直达链接：https://github.com/jefferyjob/awesome-hermes-agent-zh/actions

## 三、运行状态与排障

- **查看某次运行**：Actions → 点对应工作流 → 点运行记录 → 看各步骤日志（失败步骤有红叉，展开即见报错）
- **密钥无效 / 401**：检查 `OPENAI_API_KEY` 是否为平台 API key（非 ChatGPT 登录态）、账户是否有余额
- **定时任务被停用**：GitHub 在仓库 60 天无活动后自动停用定时工作流，到 Actions 页手动 Run workflow 一次即恢复
- **翻译质量闸门失败**：`.github/scripts/validate_sync.py` 校验未过（条目覆盖/锚点/格式等）→ 同步 issue 会收到失败评论，按 `AGENTS.md` 人工同步
- **输出被截断**（finish_reason=length）：调大 `OPENAI_MAX_TOKENS` Variable 或换输出上限更大的模型
- **本地条目白名单**：`.github/local-entries.txt` 记录本仓库独有、上游没有的条目（自动收录时自动追加）；同步校验据此放行
- **同步基线**：`.github/upstream-sync-ref` 存放已处理的上游 commit SHA（同步成功后由流水线自动推进）；异常时可比对该文件与上游 HEAD

## 四、成本与安全备忘

- 翻译成本：全量同步按 token 计费（gpt-5.1 约 $0.3–0.8/次；智谱 GLM-5.3-Flash 价格远低于此）；单条 issue 条目起草约几分钱
- 所有自动化产物均为草稿 PR / 评论，**合并与收录决定权始终在维护者**
- Copilot coding agent / code review 不可用原因：账号为 Business 席位（组织 DoushenAI 分配，本人在该组织为普通成员），Business 席位仅覆盖组织仓库，个人仓库无此开关（实测分配报 `Bot does not have access to the repository`）。如需启用：升级个人 Pro+，或将仓库迁入组织并由管理员开启策略
- `AGENTS.md` 在 `.gitignore` 中被全局忽略规则覆盖，属功能性文件，已用 `git add -f` 强制纳入版本管理
- **接入背景**（2026-11-17）：原计划用 Copilot coding agent，因上述席位限制改为 OpenAI 兼容 API 直调方案
