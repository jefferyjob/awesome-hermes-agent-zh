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
| `OPENAI_BASE` | **Variable**（明文） | `https://api.openai.com/v1` | API 地址（走代理/中转时修改）|

**Web 界面配置路径**：同上页面 → 切到「**Variables**」标签页 → `New repository variable` → Name / Value。
**命令行**：`gh variable set OPENAI_MODEL --repo jefferyjob/awesome-hermes-agent-zh --body "gpt-5.1"`

## 二、三个工作流的入口与手动触发

| 工作流 | 触发方式 | 手动触发路径 |
|---|---|---|
| `sync-check.yml` 上游同步检查 | 每日 03:23 UTC 定时 + 手动 | 仓库 **Actions** 标签页 → 左侧「上游同步检查」→ Run workflow |
| `triage.yml` issue/PR 自动核验 | issue/PR 打开时自动 + 手动 | Actions →「自动核验 issue 与 PR」→ Run workflow → 选 kind（issue/pr）+ 编号 |
| `sync-merged.yml` 合并后推进基线 | 同步 PR 合并时自动 | 无需手动 |

直达链接：https://github.com/jefferyjob/awesome-hermes-agent-zh/actions

## 三、运行状态与排障

- **查看某次运行**：Actions → 点对应工作流 → 点运行记录 → 看各步骤日志（失败步骤有红叉，展开即见报错）
- **密钥无效 / 401**：检查 `OPENAI_API_KEY` 是否为平台 API key（非 ChatGPT 登录态）、账户是否有余额
- **定时任务被停用**：GitHub 在仓库 60 天无活动后自动停用定时工作流，到 Actions 页手动 Run workflow 一次即恢复
- **翻译质量闸门失败**：`.github/scripts/validate_sync.py` 校验未过（条目覆盖/锚点/格式等）→ 同步 issue 会收到失败评论，按 `AGENTS.md` 人工同步；校验报告在 PR/评论的 details 里
- **同步基线**：`.github/upstream-sync-ref` 存放已处理的上游 commit SHA；异常时可比对该文件与上游 HEAD

## 四、成本与安全备忘

- 翻译成本：全量同步约 **$0.3–0.8/次**（gpt-5.1）；单条 issue 条目起草约 **$0.01–0.05**
- 所有自动化产物均为草稿 PR / 评论，**合并与收录决定权始终在维护者**
- Copilot coding agent / code review 不可用原因：账号为 Business 席位（组织 DoushenAI 分配，本人在该组织为普通成员），Business 席位仅覆盖组织仓库，个人仓库无此开关（实测分配报 `Bot does not have access to the repository`）。如需启用：升级个人 Pro+，或将仓库迁入组织并由管理员开启策略
- `AGENTS.md` 在 `.gitignore` 中被全局忽略规则覆盖，属功能性文件，已用 `git add -f` 强制纳入版本管理
