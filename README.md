<p align="center">
  <picture>
    <img src="https://raw.githubusercontent.com/NousResearch/hermes-agent/main/assets/banner.png" alt="Awesome Hermes Agent" width="600">
  </picture>
</p>

# Awesome Hermes Agent

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> 一个精选的技能、工具、集成与资源清单，用于增强你的 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 工作流 —— 这是由 [Nous Research](https://nousresearch.com) 打造的可自我改进 AI Agent。

Hermes Agent 是目前唯一内置学习闭环的 agent —— 它能够从经验中创建技能，在使用中持续改进，搜索自己过去的对话，并在跨会话过程中逐步建立关于你的更深层模型。你可以把它运行在 5 美元的 VPS、GPU 集群或无服务器基础设施上。当它在云端虚拟机上工作时，你还能通过 Telegram 与它交流。

这份列表跟踪其不断增长的生态系统。

> 生态状态（最后审查时间：2026-04-03）
> - Hermes Agent: [v0.6.0 (v2026.3.30)](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.3.30)
> - 核心仓库: [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)（23k+ stars）
> - 最新发布说明: [Hermes releases](https://github.com/NousResearch/hermes-agent/releases)

---

<a id="where-do-i-start"></a>
## 从哪里开始？

刚接触 Hermes？不要一上来就试图把所有东西都装上。下面是从零到高效使用的三步路径：

1. **先跑起来** —— 按照[官方文档快速开始](https://hermes-agent.nousresearch.com/docs/)操作。它涵盖安装、CLI、配置以及你的第一次对话。
2. **添加你的第一批技能** —— 安装 [wondelai/skills](https://github.com/wondelai/skills)（380+ stars，持续维护中）—— 这是一个可用于 Hermes 和其他 agent 的跨平台技能库。或者试试 [litprog-skill](https://github.com/tlehman/litprog-skill)（75+ stars），它支持在 Claude Code、OpenCode 和 Hermes 中进行文学化编程。
3. **配一个 GUI** —— 设置 [hermes-workspace](https://github.com/outsourc-e/hermes-workspace)（500+ stars），获得一个原生面向 Hermes 的工作区，包含聊天、终端和技能管理器。或者使用 [mission-control](https://github.com/builderz-labs/mission-control)（3.7k+ stars），它提供更广泛的 agent 编排仪表盘，支持 fleet 管理、任务分发和成本跟踪。

熟悉之后，再浏览下面的完整列表。每个资源都带有成熟度标签，方便你了解它的当前状态：

| 标签 | 含义 |
|-----|------|
| **production** | 稳定、文档完善、持续维护 —— 可以放心在其基础上构建 |
| **beta** | 可以使用，但仍在持续演进 —— 预计会有一些粗糙边角 |
| **experimental** | 概念验证或早期阶段 —— 可以借鉴学习，但不建议依赖 |

---

<a id="contents"></a>
## 目录

- [从哪里开始？](#where-do-i-start)
- [官方资源](#official-resources)
- [技能与插件](#skills--plugins)
  - [社区技能](#community-skills)
  - [插件](#plugins)
  - [agentskills.io 生态](#agentskillsio-ecosystem)
  - [技能注册表与发现](#skill-registries--discovery)
- [工具与实用程序](#tools--utilities)
  - [部署](#deployment)
- [集成与桥接](#integrations--bridges)
- [多 Agent 与 Swarm](#multi-agent--swarms)
- [领域应用](#domain-applications)
- [分叉与衍生项目](#forks--derivatives)
- [指南与文档](#guides--documentation)
- [运维作战手册](#operational-playbooks)
- [参与贡献](#contributing)
- [许可证](#license)

---

<a id="official-resources"></a>
## 官方资源

> 由 Nous Research 维护的核心仓库和资源。

- [Hermes Agent](https://github.com/NousResearch/hermes-agent) by [Nous Research](https://nousresearch.com) - 核心项目。具备封闭学习回路的可自我改进 AI agent，支持多平台网关（Telegram、Discord、Slack、WhatsApp、Signal、Feishu/Lark、WeCom）、六种终端后端、cron 调度、MCP 集成、profiles（多实例）和 fallback providers。23k+ stars。包含从 OpenClaw 自动迁移功能。
- [autonovel](https://github.com/NousResearch/autonovel) by [Nous Research](https://nousresearch.com) - 基于 Hermes 构建的自主小说写作流水线。使用 agent 循环端到端生成长篇手稿（100k+ 字）。
- [hermes-paperclip-adapter](https://github.com/NousResearch/hermes-paperclip-adapter) by [Nous Research](https://nousresearch.com) - 让 Hermes 作为 Paperclip 公司中的托管员工运行。将 agent 接入 Paperclip 的任务管理和治理系统。
- [hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) by [Nous Research](https://nousresearch.com) - 使用 DSPy 和 GEPA（Genetic Evolution of Prompt Architectures）进行进化式自我改进。这是用于优化 Hermes 自身提示词和行为的研究流水线。
- [Official Documentation](https://hermes-agent.nousresearch.com/docs/) - 全面的官方文档，涵盖快速开始、CLI、配置、消息网关、安全、工具、技能、记忆、MCP、cron、ACP、API server 和架构。
- [Release Notes](https://github.com/NousResearch/hermes-agent/releases) - 官方更新日志，包含每个 Hermes 版本的功能亮点、迁移说明和可靠性修复。
- [tinker-atropos](https://github.com/NousResearch/tinker-atropos) by [Nous Research](https://nousresearch.com) - 独立的 Atropos 集成，接入 Thinking Machines Tinker API。用于在真实 agent 轨迹上微调工具调用模型的 RL 训练基础设施。
- [Skills Hub](https://agentskills.io) - 面向 agent 技能的开放标准。兼容 Hermes、Claude Code、Cursor、Codex 和其他 agent。
- [Discord](https://discord.gg/NousResearch) - Nous Research 社区。用于提交 bug、提出功能请求以及一般讨论。

<br>

<a id="skills--plugins"></a>
## 技能与插件

> 技能是过程记忆 —— 是 Hermes 从经验中形成并在使用中持续改进的可复用能力。插件则扩展核心功能。

<a id="community-skills"></a>
### 社区技能

- **[beta]** [hermes-plugins](https://github.com/42-evey/hermes-plugins) by [42-evey](https://github.com/42-evey) - 目标管理、agent 间桥接、模型选择和成本控制。四个插件覆盖了最常见的运维需求。如果你运行多个 Hermes 实例，其中的 inter-agent bridge 会特别有用。
- **[beta]** [hermes-skill-factory](https://github.com/Romanescu11/hermes-skill-factory) by [Romanescu11](https://github.com/Romanescu11) - 可自动从你的工作流中生成可复用技能的元技能。把重复执行的任务交给它，它会为该任务创建一个技能。
- **[beta]** [litprog-skill](https://github.com/tlehman/litprog-skill) by [tlehman](https://github.com/tlehman) - 适用于 Claude Code、OpenCode 和 Hermes 的文学化编程技能。把代码与文字说明编织为有文档、可执行的笔记。
- **[experimental]** [Wizards-of-the-Ghosts](https://github.com/Hmbown/Wizards-of-the-Ghosts) by [Hmbown](https://github.com/Hmbown) - 幻想法术主题技能包。将真实开发操作（重构、lint、测试）包装进桌面 RPG 风格界面中。
- **[experimental]** [super-hermes](https://github.com/Cranot/super-hermes) by [Cranot](https://github.com/Cranot) - 教 Hermes 为自己编写分析型提示词。增加一层元推理能力，让 agent 在执行任务前先为自己生成更好的提示词。
- **[experimental]** [hermes-life-os](https://github.com/Lethe044/hermes-life-os) by [Lethe044](https://github.com/Lethe044) - 个人 OS agent，可检测日常模式并随着时间学习你的习惯。它将 Hermes 的记忆系统用于生活方式追踪，而不只是代码。
- **[beta]** [hermes-incident-commander](https://github.com/Lethe044/hermes-incident-commander) by [Lethe044](https://github.com/Lethe044) - 面向生产事故检测与自愈的自主 SRE agent。它可监控服务、诊断故障并应用修复。与 Hermes 的 cron 调度搭配良好。
- **[beta]** [hermes-dojo](https://github.com/Yonkoo11/hermes-dojo) by [Yonkoo11](https://github.com/Yonkoo11) - 自我改进系统，可监控 agent 性能、识别薄弱技能并自动迭代改进。
- **[experimental]** [hermes-skill-marketplace](https://github.com/Lethe044/hermes-skill-marketplace) by [Lethe044](https://github.com/Lethe044) - 能够自主编写、测试并发布新技能的 agent。自动化技能创建与分发生命周期。


<a id="agentskillsio-ecosystem"></a>
### agentskills.io 生态

> 基于 [agentskills.io](https://agentskills.io) 开放标准构建的技能 —— 可在 Hermes 和其他 agent 平台之间兼容使用。

- **[production]** [wondelai/skills](https://github.com/wondelai/skills) by [wondelai](https://github.com/wondelai) - 面向 Claude Code 和 agentskills.io 兼容平台的跨平台 agent 技能。
- **[production]** [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) by [mukul975](https://github.com/mukul975) - 753+ 个结构化网络安全技能，映射 MITRE ATT&CK。当前最全面的安全技能集合。4k+ stars。
- **[production]** [chainlink-agent-skills](https://github.com/smartcontractkit/chainlink-agent-skills) by [Chainlink](https://github.com/smartcontractkit) - 基于 agentskills.io 规范的官方 Chainlink agent 技能。支持预言机网络数据、CCIP 和智能合约交互。
- **[production]** [black-forest-labs/skills](https://github.com/black-forest-labs/skills) by [Black Forest Labs](https://github.com/black-forest-labs) - 用于图像生成的官方 FLUX 模型技能。来自 FLUX 创建者的一方技能。
- **[production]** [pydantic-ai-skills](https://github.com/DougTrajano/pydantic-ai-skills) by [DougTrajano](https://github.com/DougTrajano) - 支持 agentskills.io 的 Pydantic AI。为 agent 技能输入和输出增加类型安全的 schema 校验。
- **[beta]** [cognify-skills](https://github.com/Yarmoluk/cognify-skills) by [Yarmoluk](https://github.com/Yarmoluk) - 19 个面向业务运营的技能，覆盖 CRM、开票和项目管理。
- **[beta]** [execplan-skill](https://github.com/tiann/execplan-skill) by [tiann](https://github.com/tiann) - 以完善的生命周期管理方式执行复杂、长时间运行的任务 —— 支持进度跟踪、检查点和故障恢复。
- **[beta]** [maestro](https://github.com/ReinaMacCredy/maestro) by [ReinaMacCredy](https://github.com/ReinaMacCredy) - 使用 Conductor 规划与 Beads 跟踪进行技能编排。把多步骤技能执行组织成可观测的流水线。
- **[beta]** [bmad-module-skill-forge](https://github.com/armelhbobdad/bmad-module-skill-forge) by [armelhbobdad](https://github.com/armelhbobdad) - 将仓库和文档转换为符合 agentskills.io 标准的技能。输入代码库，输出可安装技能。
- **[beta]** [Agentic-MCP-Skill](https://github.com/cablate/Agentic-MCP-Skill) by [cablate](https://github.com/cablate) - 带有 agentskills.io 校验能力的 MCP 客户端。桥接 MCP 工具服务器与技能标准。
- **[experimental]** [ripley-xmr-gateway](https://github.com/KYC-rip/ripley-xmr-gateway) by [KYC-rip](https://github.com/KYC-rip) - 面向 agent 的 Monero（XMR）区块链网关。让 agent 工作流能够发起私密加密货币交易。
- **[beta]** [skillsdotnet](https://github.com/PederHP/skillsdotnet) by [PederHP](https://github.com/PederHP) - 带 MCP 集成的 agentskills.io C# 实现。是 Python/TypeScript SDK 的 .NET 替代方案。

<a id="plugins"></a>
### 插件

- **[beta]** [plur](https://github.com/plur-ai/plur) by [plur-ai](https://github.com/plur-ai) - 采用开放 engram 格式（YAML）的 AI agent 共享记忆层。适合在 Hermes 工作流中实现持久化学习模式。
- **[experimental]** [hermes-payguard](https://github.com/nativ3ai/hermes-payguard) by [nativ3ai](https://github.com/nativ3ai) - 安全的 USDC 和 x402 支付插件。允许 Hermes 在可配置消费上限和审批流下收付款。
- **[beta]** [hermes-web-search-plus](https://github.com/robbyczgw-cla/hermes-web-search-plus) by [robbyczgw-cla](https://github.com/robbyczgw-cla) - 多提供商网页搜索，支持在 Serper、Tavily、Exa 等之间智能路由。用更好的结果质量和来源多样性替代内置搜索。
- **[beta]** [hermes-weather-plugin](https://github.com/FahrenheitResearch/hermes-weather-plugin) by [FahrenheitResearch](https://github.com/FahrenheitResearch) - 专业级天气插件，包含 NWS 模型图像、NEXRAD 雷达和气象计算。
- **[experimental]** [hermes-wxtrain-plugin](https://github.com/FahrenheitResearch/hermes-wxtrain-plugin) by [FahrenheitResearch](https://github.com/FahrenheitResearch) - 用于从 HRRR/GFS/ERA5 天气模型构建训练数据集的 ML 流水线插件。是天气插件的配套项目，用于构建天气 ML 流程。
- **[experimental]** [hermes-plugin-chrome-profiles](https://github.com/anpicasso/hermes-plugin-chrome-profiles) by [anpicasso](https://github.com/anpicasso) - 通过 CDP 在不同 Chrome profile 间切换浏览器工具。适用于多账号测试或使用不同已保存会话进行浏览。
- **[experimental]** [hermes-cloudflare](https://github.com/raulvidis/hermes-cloudflare) by [raulvidis](https://github.com/raulvidis) - Cloudflare 浏览器渲染插件。通过 Cloudflare 基础设施进行无头浏览，而不是本地浏览器自动化。
- **[beta]** [evey-bridge-plugin](https://github.com/42-evey/evey-bridge-plugin) by [42-evey](https://github.com/42-evey) - 用于与 Evey（hermes-agent）桥接的 Claude Code 插件。让 Claude Code 与 Hermes 共享上下文并相互交接任务。

<a id="skill-registries--discovery"></a>
### 技能注册表与发现

- **[beta]** [hermeshub](https://github.com/amanning3390/hermeshub) by [amanning3390](https://github.com/amanning3390) - 浏览、分享和安装 Hermes 社区技能。面向技能发现的社区中心，目前仍较早期，但在持续增长。
- **[production]** [skilldock.io](https://github.com/chigwell/skilldock.io) by [chigwell](https://github.com/chigwell) - 兼容 OpenClaw、Claude Code 和 Hermes 的可复用 AI 技能注册表。成熟的跨平台技能市场，拥有活跃目录。

<br>

<a id="tools--utilities"></a>
## 工具与实用程序

> 构建在 Hermes Agent 之上或围绕它构建的应用、CLI 和实用工具。

- **[production]** [hermes-workspace](https://github.com/outsourc-e/hermes-workspace) by [outsourc-e](https://github.com/outsourc-e) - 基于 Web 的工作区，包含聊天、终端、记忆浏览器、技能管理器和检查器。是目前最完整的 Hermes GUI。诞生于 Nous Hackathon 2026。
- **[production]** [mission-control](https://github.com/builderz-labs/mission-control) by [builderz-labs](https://github.com/builderz-labs) - 面向 AI agent 编排的开源仪表盘。可管理 agent fleet、分发任务、跟踪成本并协调多 agent 工作流。自托管，基于 SQLite。3.7k+ stars。
- **[experimental]** [hermes-neurovision](https://github.com/Tranquil-Flow/hermes-neurovision) by [Tranquil-Flow](https://github.com/Tranquil-Flow) - 带 42 种动画主题的终端神经可视化器。为 agent 活动提供装饰性终端覆盖层。
- **[beta]** [lintlang](https://github.com/roli-lpci/lintlang) by [roli-lpci](https://github.com/roli-lpci) - 面向 AI agent 配置与提示词的静态 linter，带 HERM v1.1 评分。可捕捉那些会悄悄降低 agent 行为质量的配置错误。
- **[beta]** [nix-hermes-agent](https://github.com/0xrsydn/nix-hermes-agent) by [0xrsydn](https://github.com/0xrsydn) - Hermes 的 Nix 包和 NixOS 模块。通过 Nix flakes 实现完全可复现的部署。
- **[beta]** [openclaw-to-hermes](https://github.com/jefferyjob/awesome-hermes-agent-zh) by [jefferyjob](https://github.com/jefferyjob) - 从 OpenClaw 迁移到 Hermes 的社区工具。它诞生于原生 `hermes-migrate` 存在关键 bug 的时期。对于 Hermes v0.3.0+，更推荐使用原生 `hermes claw migrate` 命令 —— 现在它已经覆盖完整迁移路径。
- **[experimental]** [vessel-browser](https://github.com/unmodeled-tyler/vessel-browser) by [unmodeled-tyler](https://github.com/unmodeled-tyler) - 面向 AI 的原生 Linux 浏览器，支持 MCP 控制和自主浏览。这是为 agent 使用场景构建的完整浏览器，而不是无头浏览器封装。
- **[beta]** [portable-hermes-agent](https://github.com/rookiemann/portable-hermes-agent) by [rookiemann](https://github.com/rookiemann) - Windows 桌面应用，集成 100 个工具、GUI、本地模型、ComfyUI 和工作流于单个便携包中。
- **[beta]** [hermes-webui](https://github.com/sanchomuzax/hermes-webui) by [sanchomuzax](https://github.com/sanchomuzax) - 轻量级进程监控与配置仪表盘。比 hermes-workspace 更简单，更偏重运维。
- **[beta]** [evey-setup](https://github.com/42-evey/evey-setup) by [42-evey](https://github.com/42-evey) - 一条命令搭建完整 hermes-agent 技术栈，附带免费模型和 29 个插件。带有覆盖大多数使用场景的预设默认值。
- **[beta]** [flowstate-qmd](https://github.com/amanning3390/flowstate-qmd) by [amanning3390](https://github.com/amanning3390) - 面向 AI agent 的预期式记忆系统，支持 RAG 和向量搜索。在查询真正到达 agent 之前预取相关上下文。

<a id="deployment"></a>
### 部署

- **[beta]** [hermes-agent-docker](https://github.com/xmbshwll/hermes-agent-docker) by [xmbshwll](https://github.com/xmbshwll) - 面向 Hermes 的最小化 Docker 沙箱镜像。拉取、运行、完成。
- **[beta]** [hermes-agent-template](https://github.com/Crustocean/hermes-agent-template) by [Crustocean](https://github.com/Crustocean) - 面向 Crustocean 云端 Hermes 部署的生产就绪 Docker 镜像。基础设施连接已预先配置。
- **[experimental]** [portainer-stack-hermes](https://github.com/ellickjohnson/portainer-stack-hermes) by [ellickjohnson](https://github.com/ellickjohnson) - Docker Compose + Portainer + ttyd Web 终端。部署 Hermes，并可从任意浏览器访问。
- **[experimental]** [hermes-autonomous-server](https://github.com/JackTheGit/hermes-autonomous-server) by [JackTheGit](https://github.com/JackTheGit) - 在 Linux 服务器上使用 systemd 和 cron 进行无头 Hermes 部署。可无人值守运行。

<br>

<a id="integrations--bridges"></a>
## 集成与桥接

> 将 Hermes 连接到其他平台、设备和服务。

- **[beta]** [hermes-android](https://github.com/raulvidis/hermes-android) by [raulvidis](https://github.com/raulvidis) - 带完整 Python 工具集的 Android 设备桥接。让 Hermes 能与 Android 设备交互并进行控制。
- **[beta]** [hermes-miniverse](https://github.com/teknium1/hermes-miniverse) by [teknium1](https://github.com/teknium1) - 通往 Miniverse 像素世界的桥接工具。作者是 Nous Research 联合创始人之一。
- **[production]** [hindsight](https://github.com/vectorize-io/hindsight) by [Vectorize](https://github.com/vectorize-io) - 面向 agent 的长期记忆层，支持 retain / recall / reflect 工作流。可通过插件或 MCP 集成到 Hermes，并支持语义、图谱和时间检索。
- **[beta]** [honcho-self-hosted](https://github.com/elkimek/honcho-self-hosted) by [elkimek](https://github.com/elkimek) - 面向 Hermes 的自托管 Honcho 记忆后端部署。适用于需要更强跨会话记忆行为且希望本地可控的场景。
- **[experimental]** [zouroboros-swarm-executors](https://github.com/marlandoj/zouroboros-swarm-executors) by [marlandoj](https://github.com/marlandoj) - 用于 Claude Code + Hermes 集成的本地执行器桥接。支持两个 agent 之间的任务移交。
- **[beta]** [reina](https://github.com/Crustocean/reina) by [Crustocean](https://github.com/Crustocean) - 面向 Crustocean 平台的自主 AI agent。将 Hermes 深度集成到 Crustocean 产品中。
- **[beta]** [hermes-agent-acp-skill](https://github.com/Rainhoole/hermes-agent-acp-skill) by [Rainhoole](https://github.com/Rainhoole) - 连接 Hermes、Codex 和 Claude Code 的多 agent 委派技能。可自动将子任务路由给最适合的 agent。
- **[experimental]** [hermes-blockchain-oracle](https://github.com/gizdusum/hermes-blockchain-oracle) by [gizdusum](https://github.com/gizdusum) - Solana 区块链情报 MCP server。通过 MCP 为 Hermes 提供链上分析和钱包数据。
- **[experimental]** [hermes-council](https://github.com/Ridwannurudeen/hermes-council) by [Ridwannurudeen](https://github.com/Ridwannurudeen) - 对抗式多视角 council MCP server。在 agent 作出决定前，让多个 AI 观点先进行辩论。
- **[experimental]** [NemoHermes](https://github.com/Hmbown/NemoHermes) by [Hmbown](https://github.com/Hmbown) - NVIDIA 能力注册表与 Spark 感知路由层。将计算密集型任务路由到可用 GPU 基础设施。

<br>

<a id="multi-agent--swarms"></a>
## 多 Agent 与 Swarms

> 用于运行多个 Hermes agent，或让 Hermes 与其他 agent 协同工作的框架和工具。

- **[experimental]** [Ankh.md](https://github.com/Abruptive/Ankh.md) by [Abruptive](https://github.com/Abruptive) - TAW Agent x Hermes 多 agent swarm 框架。协调多个 agent 共享目标并分布式执行任务。
- **[experimental]** [gladiator](https://github.com/runtimenoteslabs/gladiator) by [runtimenoteslabs](https://github.com/runtimenoteslabs) - 两家自主 AI 公司为争夺 GitHub stars 而竞争。一个探索自主 agent 竞争动态的黑客松项目。
- **[beta]** [bigiron](https://github.com/supermodeltools/bigiron) by [supermodeltools](https://github.com/supermodeltools) - 基于 Hermes 和 Supermodel 代码图谱的 AI 原生 SDLC。通过协同 agent 驱动完整软件开发生命周期。
- **[beta]** [opencode-hermes-multiagent](https://github.com/1ilkhamov/opencode-hermes-multiagent) by [1ilkhamov](https://github.com/1ilkhamov) - 面向 OpenCode AI 的 17 个专用 agent。每个 agent 都有明确角色，并通过结构化接口通信。

<br>

<a id="domain-applications"></a>
## 领域应用

> 使用 Hermes 针对特定领域打造的专用应用。

- **[experimental]** [hermes-embodied](https://github.com/bryercowan/hermes-embodied) by [bryercowan](https://github.com/bryercowan) - 通过 VLA 模型微调实现自我改进机器人系统。将 Hermes 的学习闭环应用于真实机器人控制。Nous Hackathon 项目。
- **[beta]** [hermescraft](https://github.com/bigph00t/hermescraft) by [bigph00t](https://github.com/bigph00t) - 面向 Minecraft 的具身 AI 伙伴，具备持久记忆。可追踪库存、学习建造偏好并跨会话保留上下文。
- **[experimental]** [Hermes-mars-rover](https://github.com/Snehal707/Hermes-mars-rover) by [Snehal707](https://github.com/Snehal707) - 基于 ROS2 和 Gazebo 的火星车模拟器。使用 Hermes 的技能创建循环持续改进导航能力。
- **[beta]** [anihermes](https://github.com/rodmarkun/anihermes) by [rodmarkun](https://github.com/rodmarkun) - 本地动漫服务与追踪器，带自然语言界面。可通过对话浏览、追踪并获取推荐。
- **[beta]** [job-scout-agent](https://github.com/Christabel337/job-scout-agent) by [Christabel337](https://github.com/Christabel337) - 自主求职 agent。搜索职位、跟踪申请并管理求职流水线。
- **[beta]** [hermes-ai-infrastructure-monitoring-toolkit](https://github.com/JackTheGit/hermes-ai-infrastructure-monitoring-toolkit) by [JackTheGit](https://github.com/JackTheGit) - 通过 Telegram 实现基础设施监控、成本预测和告警。使用 cron 调度进行持续检查。
- **[experimental]** [hermes-genesis](https://github.com/Ridwannurudeen/hermes-genesis) by [Ridwannurudeen](https://github.com/Ridwannurudeen) - 自主“活世界”引擎，支持程序化生成。创建并维护会随着时间推移愈发复杂的虚拟世界。
- **[experimental]** [hermes-legal](https://github.com/Lethe044/hermes-legal) by [Lethe044](https://github.com/Lethe044) - 支持英语和土耳其语的合同风险分析。识别高风险条款并总结法律义务。
- **[beta]** [hermes-startup-architect](https://github.com/dlkakbs/hermes-startup-architect) by [dlkakbs](https://github.com/dlkakbs) - 从创业想法生成可直接面向投资人的资料包 —— 包括市场分析、路演 deck 和财务预测。
- **[beta]** [mercury](https://github.com/hxsteric/mercury) by [hxsteric](https://github.com/hxsteric) - 带 WebGL 仪表盘的多链区块链现金流分析器。支持链上取证与流向可视化。
- **[experimental]** [hermes-research-agent](https://github.com/Aum08Desai/hermes-research-agent) by [Aum08Desai](https://github.com/Aum08Desai) - 自主 LLM 研究 agent。端到端处理文献综述、假设生成和实验设计。

<br>

<a id="forks--derivatives"></a>
## 分叉与衍生项目

> 将 Hermes 带向新方向的知名分叉和衍生项目。

- **[beta]** [hermes-agent-camel](https://github.com/nativ3ai/hermes-agent-camel) by [nativ3ai](https://github.com/nativ3ai) - 集成 CaMeL 信任边界的 Hermes。为安全关键型部署在 agent 循环中加入正式的信任验证。
- **[experimental]** [orahermes-agent](https://github.com/jasperan/orahermes-agent) by [jasperan](https://github.com/jasperan) - Oracle AI Agent Harness —— 集成 OCI GenAI 与 Oracle 26ai。是面向 Oracle 环境的企业级入口方案。
- **[beta]** [hermes-alpha](https://github.com/kaminocorp/hermes-alpha) by [kaminocorp](https://github.com/kaminocorp) - 云端部署版 Hermes，附带预配置基础设施模板。跳过本地搭建。
- **[experimental]** [hermes-skill-distillation](https://github.com/beardthelion/hermes-skill-distillation) by [beardthelion](https://github.com/beardthelion) - 从真实任务中生成 agentic 训练轨迹。一个用来大规模产出微调数据的黑客松项目。

<br>

<a id="guides--documentation"></a>
## 指南与文档

> 教程、文档和学习资源。

- **[beta]** [hermes-agent-docs](https://github.com/mudrii/hermes-agent-docs) by [mudrii](https://github.com/mudrii) - 面向 Hermes Agent 的全面社区文档。详细覆盖 v0.2.0，对部署模式是官方文档之外的有用补充。
- **[production]** [hermes-wsl-ubuntu](https://github.com/metantonio/hermes-wsl-ubuntu) by [metantonio](https://github.com/metantonio) - 在 Windows 上通过 WSL2 Ubuntu 运行 Hermes 的分步搭建说明。
- **[beta]** [HermesWiki](https://github.com/martymcenroe/HermesWiki) by [martymcenroe](https://github.com/martymcenroe) - 社区维护的 wiki，汇集使用 Hermes 构建自主 agent 的实用模式与部署建议。

---

<a id="operational-playbooks"></a>
## 运维作战手册

> 在生产环境中反复证明对 Hermes 团队有帮助的实用工作流模式。

- **夜间自我进化 + 护栏评估** —— 按计划运行 [hermes-agent-self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution)，再运行第二个验证 cron 对质量进行评分并阻止优化循环作弊。
- **使用 Honcho/Hindsight 处理记忆压力** —— 如果你在重复上下文或丢失长期记忆，请查看 [Honcho Memory docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/honcho)，并评估 [hindsight](https://github.com/vectorize-io/hindsight) 或自托管记忆后端。
- **尽早调整 session timeout/expiry** —— 使用[配置文档](https://hermes-agent.nousresearch.com/docs/user-guide/configuration/)为推进较慢的线程调整会话保留时间，以便在需要时保留上下文。
- **OpenClaw 并行迁移** —— 在迁移过程中，使用 [openclaw-to-hermes](https://github.com/jefferyjob/awesome-hermes-agent-zh) 和 Hermes 原生迁移路径让两个系统并行运行，待 cron 与路由行为一致后再完成切换。
- **有意识地维护 USER.md 和 MEMORY.md** —— 将用户画像记忆视为高信号基础设施。保持条目简洁、持久，并聚焦偏好，而不是堆积原始笔记。

---

<a id="contributing"></a>
## 参与贡献

[在这里推荐新资源！](https://github.com/jefferyjob/awesome-hermes-agent-zh/issues/new)

提交前，请确保：

1. 该资源与 Hermes Agent 生态或 [agentskills.io](https://agentskills.io) 标准直接相关
2. 该资源拥有清晰的 README，并且维护状态合理
3. 你已经检查过列表，避免重复收录

如果你想对仓库本身提出建议，请[创建一个 issue](https://github.com/jefferyjob/awesome-hermes-agent-zh/issues/new)。

提交前请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。


---

<div align="center">

**你的团队需要构建 agent 基础设施、交易系统或 Solana 应用吗？**

[Builderz](https://builderz.dev) 已在 15 个国家交付了 32+ 个生产级 AI 系统。

[联系他们](https://builderz.dev) | [@nyk_builderz](https://x.com/nyk_builderz)

</div>

<a id="license"></a>
## 许可证

[![CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

本列表采用 [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) 许可。你可以出于任何目的共享和改编本材料，但前提是给出适当署名。

本列表中包含的所有资源各自适用其自身的许可证条款。
