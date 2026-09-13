# -*- coding: utf-8 -*-
"""生成 agent 论文知识库站点：index.html + papers/*.html + assets/style.css"""
import os, re

import os
BASE = os.environ.get("KB_SITE") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def md(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)

SHORT = {"R1": "AI 应用平台", "R2": "轮询框架", "R3": "性能优化", "R4": "Apache Fury", "R5": "团队管理"}

def rtag(item):
    key = item.split("：")[0].strip()
    return SHORT.get(key, key)

CATS = {
    "A": ("设计范式与工程方法论", "#2563eb"),
    "B": ("上下文工程与记忆", "#7c3aed"),
    "C": ("多智能体系统与失败分析", "#dc2626"),
    "D": ("Agentic 底座模型", "#059669"),
    "E": ("Agent RL 训练与深度研究", "#d97706"),
    "F": ("交互、评测与协议标准", "#0891b2"),
}

# 简历关联项目
RESUME = {
    "R1": "AI 应用平台（RAG 知识库 / 意图识别 / Prompt 迭代闭环 / 场景训练）",
    "R2": "分布式异步轮询框架（10× QPS，高并发工程）",
    "R3": "萝卜投资性能优化（O(1) 复杂度 / 100ms 实时计算 / 流量整形）",
    "R4": "Apache Fury Committer（高性能跨语言序列化）",
    "R5": "17 人跨地域团队管理与工程规范",
}

# (id, slug, title, org, date, form, links, cat, oneline, points, data, resume, interview, deep)
PAPERS = [
("p01", "anthropic-building-effective-agents", "Building Effective Agents",
 "Anthropic", "2024.12（2025 年成为事实标准）", "工程方法论",
 [("原文", "https://www.anthropic.com/engineering/building-effective-agents")], "A",
 "Agent 领域被引用最多的工程纲领：区分 workflow 与 agent，给出五种可组合的基础模式，主张从最简单的方案开始。",
 ["核心区分：workflow（代码编排 LLM，流程确定）vs agent（LLM 自主循环使用工具，过程开放）——大多数生产场景只需要 workflow，不要为了 agent 而 agent。",
  "五种基础模式：Prompt Chaining（链式）、Routing（路由）、Parallelization（并行）、Orchestrator-Workers（编排者-执行者）、Evaluator-Optimizer（生成-评审循环）。",
  "Agent = LLM 在循环中使用工具，基于环境反馈决定下一步；成功取决于 ACI（Agent-Computer Interface，工具与环境的接口设计）质量，而不是框架复杂度。",
  "三条原则：保持简单、透明（让规划步骤可见）、精心设计工具接口（参数含义清晰、用真实数据测试工具）。"],
 ["多家成功客户仅用单个 LLM 调用 + 检索就完成了生产部署；复杂 agent 仅在确有多步自由度需求时使用。",
  "该文发布后成为行业术语来源，'routing pattern''orchestrator-workers' 等说法在各大厂文档中沿用。"],
 ["R1：意图识别引擎就是 Routing 模式的落地——用户问题先分类（咨询/投诉/办理）再走不同链路，可直接引用 Anthropic 术语表达。",
  "R1：Prompt 版本管理 → 自动评估 → 灰度 的迭代闭环对应 Evaluator-Optimizer 模式。"],
 ["场景①被问'你如何设计 agent 架构'｜回答：先按 Anthropic 的 workflow/agent 二分判断任务是否需要自主循环，我负责的 RAG 知识库场景大多是确定性链路，用的是 Routing + Chaining；只有当步骤无法预先穷举时才引入 agent 循环。",
  "场景②被问'工具怎么设计'｜回答：重点讲 ACI——我在平台里给每个知识检索工具定义了最小参数集和结构化返回（来源、置信度），工具描述用真实 badcase 校准过。"],
 ["精读第一节的 workflow vs agent 判断标准；把五种模式各想一个自己项目中的对应物；思考：你的场景如果重做，哪一步最值得从 workflow 升级为 agent？"]),

("p02", "openai-practical-guide-building-agents", "A Practical Guide to Building Agents",
 "OpenAI", "2025.04", "工程指南",
 [("官方 PDF", "https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf"),
  ("介绍页", "https://openai.com/business/guides-and-resources/")], "A",
 "OpenAI 面向企业的 agent 落地指南：何时该用 agent、单智能体优先、三种编排拓扑、分层防护栏。",
 ["Agent 定义三要素：Model（决策大脑）+ Tools（能力）+ Instructions（行为边界与纪律）。",
  "适用判断：只有在'需要持续判断、规则无法穷举、需要自然语言中转'的场景才用 agent；否则用确定性自动化/工作流。",
  "编排三种拓扑：Single Agent（先做这个）、Manager（控制多个工具型子智能体）、Decentralized（多个平级 agent 互相移交）。",
  "防护栏（Guardrails）要分层：内容安全、事实校验、PII 过滤、工具级权限、人工升级（escalation）。"],
 ["指南明确建议'从单智能体 + 好工具开始，跑通再扩展'，与大量企业落地经验一致。",
  "已入选众多企业 AI 转型培训材料，是 2025 年传播最广的 agent 落地文档之一。"],
 ["R1：平台 0→1 时选择'单一平台 + 意图路由'而非多智能体，可用该指南的编排拓扑论证合理性。",
  "R5：防护栏分层思想对应团队工程规范设计（评审分层、发布分层）。"],
 ["场景①被问'从零搭建 agent 的第一步'｜回答：OpenAI 指南第一条就是把 agent 当'带工具和纪律的模型'，先做单智能体把工具质量和指令写透，我 0→1 建平台时同样坚持先单链路后编排。",
  "场景②被问'如何保证线上安全'｜回答：Guardrails 分层清单——输入侧内容过滤、检索侧权限过滤、输出侧事实校验、兜底人工升级，每层可独立开关。"],
 ["把'何时用 agent/何时用工作流'的三条件背下来；对照自己项目写出三层防护栏清单。"]),

("p03", "anthropic-multi-agent-research-system", "How We Built Our Multi-Agent Research System",
 "Anthropic", "2025.06", "工程实战复盘",
 [("原文", "https://www.anthropic.com/engineering/built-multi-agent-research-system")], "A",
 "Anthropic 多智能体研究系统（Research 功能）的完整工程复盘：编排者-执行者架构、并行收益、token 成本与可靠性教训。",
 ["架构：LeadAgent 负责拆解与编排，多个并行 Subagent 各自带独立上下文与工具，最后汇总——适合'广度优先、可并行'的研究型任务。",
  "工程要点：任务描述要显式传递目标/输出格式/工具边界；按问题复杂度分配并行度；LeadAgent 像管理者一样给 subagent 写清楚任务说明书。",
  "可靠性优先：增量保存状态支持断点恢复、渐进式披露降低全量失败率；多智能体的调试难度远高于单链路。"],
 ["内部评测中多智能体系统较单智能体 Opus 提升 90.2%（研究广度任务）。",
  "关键洞察：**token 用量解释了 80% 的性能方差**；多智能体用量约为普通聊天的 15 倍——收益换成本，只在值钱的任务上用。",
  "生产数据：多智能体在代码性、并行性强的任务上优势最大，串行依赖任务上可能为负收益。"],
 ["R1：自己在多轮对话里做摘要压缩控制 token——这篇给了行业级数据（15× token / 80% 方差），可引用说明成本工程是 agent 产品生死线。",
  "R2/R3：多智能体并行 subagent 对基础设施的并发与延迟要求，正好接上你 10× QPS、流量整形的功底。",
  "R5：LeadAgent 写任务说明书 ↔ 你管理 17 人团队的任务分发经验，人机组织同构。"],
 ["场景①'要不要上多智能体'｜回答：用 90.2%/15×token 这组数据说明它是'用成本买广度'，我的场景（知识问答）串行度高，暂不上；若做深度研究类功能则首选该架构。",
  "场景②'多智能体最难的是什么'｜回答：调试与状态管理——Anthropic 也承认失败恢复最难，我的做法对应他们的状态增量保存。"],
 ["记住三个数字：90.2%、15×、80%；把 orchestrator-worker 与你团队的任务拆解方式做一次对照。"]),

("p04", "yao-the-second-half", "The Second Half",
 "Shunyu Yao（OpenAI）", "2025.06", "方向性论文",
 [("原文", "https://ysymyth.github.io/The-Second-Half/"),
  ("中文翻译(社区)", "https://github.com/SLBGAPI/The-Second-Half_cn")], "A",
 "2025 年 agent 方向最有影响力的立场论文：AI 上半场拼方法，下半场拼问题定义与评测。",
 ["上半场（预训练时代）：目标是让模型更强，方法迭代快、但问题固定（benchmark 已定）；下半场：模型能力趋同，价值转向'定义问题 + 构造真实环境 + 可靠度量'。",
  "下半场的关键动作：把模糊的人类需求转成可验证的任务规格（specification）、构建真实环境的 RL 问题、设计能反映真实价值的评测。",
  "对工程师的含义：'知道该测什么、能造出环境'比'知道最新技巧'更稀缺——评测与产品化成为核心竞争力。"],
 ["作者 Shunyu Yao 是 ReAct 论文一作，本文在 agent 圈层被大量引用与讨论，被多家公司内部分享。"],
 ["R1：你的黄金测试集 + 自动评估 + 显著性检验正是'下半场思维'——先有度量再有优化，这是面试里最值钱的自我定位。",
  "R1：意图识别体系=把模糊需求转成规格（specification）的实践。"],
 ["场景①'你怎么看 agent 技术趋势'｜回答：引用下半场论——模型能力趋同后，差异化在环境与评测；我做的评估闭环就是下半场的事。",
  "场景②'为什么你的平台准确率高'｜回答：不归功于某个技巧，归功于先把成功标准定义清楚（分类别 golden set）。"],
 ["把'问题定义 > 方法迭代'内化；每讲一个项目都先讲当时的成功指标是怎么定义的。"]),

("p05", "manus-context-engineering", "Context Engineering for AI Agents: Lessons from Building Manus",
 "Manus（蝴蝶效应团队）", "2025.07", "工程博客",
 [("原文", "https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus")], "B",
 "Manus 通用智能体的一线经验总结：KV-cache 命中率是最重要的产品指标，围绕' append-only 上下文'展开的一整套工程化实践。",
 ["KV-cache 命中率是 Manus 最重要的产品指标：影响成本与延迟的数量级；实现手段——prompt 前缀稳定（不写时间戳等易变内容）、上下文只追加不修改（append-only）、必要时人为打乱 JSON 序列化的键顺序以保持缓存命中。",
  "工具定义的演进：不要把工具从上下文中'删除'（会破坏缓存且造成模型困惑），而是用 **masking（logit 偏置屏蔽）** 控制这一步可用哪些工具。",
  "用文件系统当终极上下文：超长内容放文件、上下文里只留句柄，突破了上下文窗口限制且容量无上限。",
  "通过复述（Todo.md 反复重写）操纵注意力，缓解'目标丢失'；让模型保留过去的错误并从中学习（保持错误在上下文中），避免 few-shot 固化。"],
 ["Manus 是 2025 年现象级通用智能体产品，本文被广泛视为'上下文工程'的代表作，各团队 AI 平台组必读。"],
 ["R1：你在多轮对话里做摘要压缩控 token，与 Manus 的'文件系统当上下文'是同一问题的两种解法——成本视角完全一致。",
  "R3：KV-cache 命中率优化与你做过的缓存与流量整形思想同源——把系统性能思维迁移到 LLM serving。"],
 ["场景①'多轮对话 token 怎么控'｜回答：两层——模型无关的上下文工程（摘要/句柄化/append-only 保 KV-cache）+ 模型侧压缩；引用 Manus 的 KV-cache 指标观。",
  "场景②'你的平台怎么降本'｜回答：先算单次会话成本账（检索+推理+prompt 各占多少），再按 KV-cache 命中率、上下文长度两条线优化，给出你项目的实际降幅。"],
 ["把六条实践（稳定前缀/append-only/mask/文件系统/复述/保留错误）与自己的系统逐条对照，能对上几条。"]),

("p06", "context-engineering-survey", "A Survey of Context Engineering for Large Language Models",
 "多高校联合（含新加坡国立等）", "2025.07", "综述",
 [("arXiv", "https://arxiv.org/abs/2507.13334"),
  ("GitHub 精选", "https://github.com/Meirtz/Awesome-Context-Engineering")], "B",
 "首次把'上下文工程'从经验技巧升格为形式化学科的综述：覆盖检索、处理、生成的全链路上下文组装体系。",
 ["系统化定义：上下文工程 = 为 LLM 组装'正确的信息 + 正确的工具 + 正确的格式'的系统化学科，超越单点 prompt 技巧。",
  "技术全景：长上下文管理、记忆机制（短期/长期）、外部知识检索（RAG 进化形态）、工具集成、多智能体上下文共享，均可纳入同一框架。",
  "给出'上下文不断裂（context coherence）'与'上下文预算分配'两大工程难点的方法学。"],
 ["2025 年被引最快的综述之一，配套 Awesome 清单是社区标准资源库；ACE（Agentic Context Engineering）等后续工作均以此为基础。"],
 ["R1：你的 RAG（分块/混合检索/Query 改写）+ 长对话摘要 + 工具编排，用这篇的框架描述就是'一套完整的上下文工程系统'——让经验获得学科坐标。",
  "R3：上下文预算分配与你做过的资源/流量调度是同构思维。"],
 ["场景①'RAG 怎么优化'｜回答：把 RAG 放进上下文工程的大图——检索只是'取'，还有'选、压、组'三步；我分别在分块粒度、rerank 截断、摘要压缩上做过优化。",
  "场景②'什么是上下文工程'｜回答：引用该综述定义并举例：同一个问题，换上下文组装策略效果天差地别，我项目里 QA 准确率从基线到 90%+ 的过程本质是上下文组装的迭代。"],
 ["用综述的分层（检索/处理/生成）给自己的平台画一张上下文流转图，面试白板上画出来非常加分。"]),

("p07", "mem0-long-term-memory", "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory",
 "Mem0 团队", "2025.04", "论文 + 开源系统",
 [("arXiv", "https://arxiv.org/abs/2504.19413"),
  ("GitHub", "https://github.com/mem0ai/mem0")], "B",
 "生产级 agent 长期记忆系统：两阶段（抽取-更新）记忆管线，以'增量维护'替代'全量塞上下文'。",
 ["核心机制：从对话中抽取候选记忆 → 用 LLM 做增删改决策（ADD/UPDATE/DELETE/NOOP）→ 存入向量存储；对话级与用户级双层记忆。",
  "与全量上下文对比：只携带压缩后的相关记忆，Token 与延迟大幅下降；支持检索时召回相关记忆片段。"],
 ["LOCOMO 基准：较 OpenAI 的记忆方案准确率 +26%；较全量上下文准确率 +2% 的同时 p95 延迟下降 91%；在低于 50ms 的检索延迟下可扩展到百万用户。",
  "2025 年最常被引用的生产级 agent 记忆方案之一，多智能体、客服、伴侣类产品广泛集成。"],
 ["R1：场景模拟培训是多轮长对话——Mem0 的'抽取-更新'管线与你做的'长对话摘要压缩'互为替代方案，面试可对比：摘要保连贯、记忆库保跨会话，两者可叠加。",
  "R3：p95 延迟 91% 的下降来自'少带上下文'，与你 20s→100ms 的优化是同一个'少传数据'的哲学。"],
 ["场景①'跨会话记忆怎么做'｜回答：抽取-更新式记忆库 vs 每次全量上下文，给 Mem0 的 26%/91% 数据，再讲你的摘要方案，最后给组合方案（短期摘要 + 长期记忆库）。",
  "场景②'记忆会不会引入隐私问题'｜回答：DELETE 操作支持遗忘、PII 过滤在抽取层完成——体现工程完整度。"],
 ["记住三个数字：+26%、+2%、-91% p95；想清楚你的场景里'记忆'该记什么（用户偏好？历史结论？未完成事项？）。"]),

("p08", "mast-multi-agent-failure", "Why Do Multi-Agent LLM Systems Fail?（MAST 失败分类法）",
 "UC Berkeley 等（Cemri, Pan 等）", "2025.03", "论文（NeurIPS 2025）",
 [("arXiv", "https://arxiv.org/abs/2503.13657"),
  ("GitHub", "https://github.com/multi-agent-systems-failure-taxonomy/MAST")], "C",
 "首个多智能体系统失败模式的实证分类法（MAST）：14 种失败模式、3 大层级，被引 750+。",
 ["方法：对 LangGraph、AutoGen、CrewAI 三大主流框架的真实运行 trace 做标注与根因分析。",
  "三大失败层级：①规格与系统问题（目标/角色定义不清）②智能体间对齐失败（信息传递丢失/ disagree / 重复工作，占比最高）③任务验证失败（无验证步骤、过早停止、结果错误未被发现）。",
  "给出 MAST-Data 标注数据集与自动标注器（LLM 标注器在无标签数据上达到较高人工一致率）。"],
 ["NeurIPS 2025 接收，被引 750+，是 2025 年多智能体领域引用最高的实证论文之一。"],
 ["R1：你在 0→1 时选择'意图路由的确定性链路'而非多智能体——MAST 说明约四成失败来自智能体间对齐，这正是你当时规避的风险，可反推架构决策的先见性。",
  "R5：三大失败层级与人组织的问题同构（目标不清/信息不同步/验收缺失）——用你带 17 人团队的管理经验类比，极其出彩。"],
 ["场景①'要不要把单 agent 升级成多 agent'｜回答：先引 MAST——失败大头不在单模型能力而在 agent 间对齐与验证缺失；我会先补验证层（评测闭环），再把确有并行收益的环节拆成 subagent，并用 Anthropic 的 15× token 数据算成本账。",
  "场景②'你们怎么排查 agent 链路问题'｜回答：按 MAST 三层级建立检查单——先查任务规格、再查传递信息、最后查验证，一次讲清排障框架。"],
 ["背下 3 层级 14 模式的骨架；准备一个'用 MAST 视角复盘自己系统'的故事（哪怕你的系统是单 agent，验证层缺失同样适用）。"]),

("p09", "agentscope-1.0", "AgentScope 1.0: A Developer-Oriented Technical Report",
 "阿里巴巴（Qwen 团队生态）", "2025.08", "技术报告 + 开源框架",
 [("GitHub", "https://github.com/agentscope-ai/agentscope")], "C",
 "阿里开源的多智能体开发框架 1.0：以'actor 并发 + 显式消息'为核心的开发者向设计。",
 ["设计原则：Agent as Actor——智能体是并发执行的独立单元，通过显式异步消息通信，天然支持并行与分布式部署。",
  "对开发者友好：类 OOP 的消息传递 API、内置 ReAct Agent、直接兼容 DashScope/Qwen 模型、原生 tracing 与 Studio 可视化调试。",
  "支持容错与可观测性：显式消息使失败可定位、可重放——针对 MAST 指出的失败模式提供了工程缓解。"],
 ["AgentScope 是国内使用最广的开源 agent 框架之一，1.0 版与 Qwen3/通义生态深度整合。"],
 ["R1：0→1 时自研编排 vs 采用开源框架（AgentScope/LangGraph）的 tradeoff——自研可控可审计，开源快但黑盒；可用此框架的 actor 模型反观自己的异步路由设计。",
  "R2：AgentScope 的异步消息与你的 Servlet 异步轮询框架思想同源，说明你的高并发功底可直接迁移到 agent 基础设施。"],
 ["场景①'你们为什么自研编排不用开源框架'｜回答：当时的诉求是审计与权限控制（金融场景）+ 链路确定性；开源框架当年代理生态不成熟。今天若新起项目，会评估 AgentScope 这类显式消息框架，因为它把'可观测/可重放'做进了运行时。",
  "场景②'如何做 agent 可观测'｜回答：消息级 tracing + 失败重放，参考 AgentScope 运行时与 MAST 的排障分层。"],
 ["读架构图部分即可，重点理解 'agent as actor + 显式消息' 与你异步框架的对应关系。"]),

("p10", "deepseek-r1", "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning",
 "DeepSeek", "2025.01", "论文 + 开源模型",
 [("arXiv", "https://arxiv.org/abs/2501.12948"),
  ("GitHub", "https://github.com/deepseek-ai/DeepSeek-R1")], "D",
 "开源 RL 推理模型的里程碑：几乎纯强化学习（GRPO）激发出长链推理，开启开源模型'会用脑子'的时代。",
 ["核心方法：跳过 SFT 直接对 base 模型做 GRPO 强化学习（准确奖励 + 格式奖励），推理能力自然涌现；后续加入少量冷启动数据做 R1 正式版。",
  "涌现现象：模型自发学会反思（'wait, wait'时刻）、自我验证、长短推理的自适应切换——'aha moment' 成为经典描述。",
  "蒸馏路线：用 R1 生成的数据蒸馏出 Qwen/Llama 小模型，小模型推理能力大幅超越原版，证明'推理可迁移'。"],
 ["发布后震动全球 AI 圈：以极低成本对齐闭源前沿推理模型；API 价格只有竞品的几十分之一，直接推动 2025 年 agent 推理底座的开源化浪潮。",
  "arXiv 2501.12948 是 2025 年引用量最高的论文之一（数千次引用）。"],
 ["R1：解释你平台'为什么 2023-2024 年要做意图路由和确定性工作流'——当时开源模型推理能力不足，流程确定性要靠工程补；R1 之后规划能力内生化，同样的平台今天可以更简。这体现你对技术演进的判断力。",
  "R1：模型选型故事——你做过 LLM 对比测试，R1 是国产低成本推理底座的分水岭。"],
 ["场景①'模型能力演进对你们架构的影响'｜回答：分两个时代讲——R1 之前工程补能力（意图路由/固定链路），R1 之后模型原生会规划，工程重心转向评测、成本与工具质量。这显示你能随技术演进调整架构。",
  "场景②'GRPO 和 PPO 区别'｜了解即可：去掉价值网络、组内相对优势作 baseline，训练更稳更省。"],
 ["重点读'涌现的推理行为'一节；思考一个面试题：如果今天重做你的平台，哪些工程组件会被模型原生能力替代？"]),

("p11", "qwen3-technical-report", "Qwen3 Technical Report",
 "阿里巴巴 Qwen 团队", "2025.04", "论文 + 开源模型",
 [("arXiv", "https://arxiv.org/abs/2505.09388"),
  ("GitHub", "https://github.com/QwenLM/Qwen3")], "D",
 "全尺寸开源的 hybrid-thinking 模型家族：一个模型内同时支持'深度思考'与'秒回'两种模式，原生强化工具调用。",
 ["核心创新：Thinking / Non-Thinking 混合模式——复杂问题生成完整思考过程，简单问题直接回答，由用户/系统控制，兼顾成本与质量。",
  "全家族开源：0.6B 到 235B-A22B（MoE）共数十款，覆盖端侧到旗舰；预训练 36 万亿 token 多语料。",
  "Agent 能力原生：训练中大幅强化工具调用、MCP 兼容、多轮 agent 场景，开源权重 Apache 2.0 可商用。"],
 ["发布当月成为全球开源模型下载与微调生态的事实底座；Hugging Face 下载量与衍生模型数居 2025 年前列。",
  "Flagship 235B-A22B 在多项 agent/工具调用基准上居开源首位（发布时点）。"],
 ["R1：企业私有化部署（金融数据不出域）最现实的底座选择就是 Qwen3 系——你在平台做过 LLM 对比测试，可把 Qwen3 的 hybrid-thinking 对应到'简单咨询走 non-thinking 省成本、复杂分析走 thinking 保质量'的路由思想。",
  "R1：意图路由 + Qwen3 思考模式开关 = 双层成本控制，讲成本工程时非常好用。"],
 ["场景①'私有化部署怎么选模型'｜回答：给选型框架（任务复杂度分布、显存预算、生态兼容）+ Qwen3 家族的端云协同方案；引用 hybrid thinking 的成本收益。",
  "场景②'思考模式会不会拖慢响应'｜回答：正是 Qwen3 要解决的问题——模式可切换，配合意图路由实现'该快则快'。"],
 ["记住家族规模（0.6B~235B-A22B）与 hybrid thinking 概念；对比 R1 的'always think'与 Qwen3 的'可选 think'。"]),

("p12", "kimi-k2", "Kimi K2: Open Agentic Intelligence",
 "月之暗面 Moonshot AI", "2025.07", "论文 + 开源模型",
 [("arXiv", "https://arxiv.org/abs/2507.20534"),
  ("GitHub", "https://github.com/MoonshotAI/Kimi-K2")], "D",
 "万亿参数开源模型专为 agentic 而生：用数据合成解决'工具调用无真数据'难题，并用自评准则 RL 对齐 agent 行为。",
 ["架构：1T 总参 MoE、32B 激活；自研 MuonClip 优化器（Muon + QK-clip）——15.5T tokens 预训练零 loss spike，大规模训练稳定性的代表作。",
  "关键创新①——Agentic 数据合成：真实场景工具调用数据稀缺，他们搭建大规模工具合成管线，造出覆盖数千工具的可用轨迹数据。",
  "关键创新②——联合 RL：self-critique（模型自评 + rubric 准则奖励）+ 通用可验证奖励 RL，专门对齐'多轮工具交互'行为而非仅刷推理题。"],
 ["发布时 Tau2-Bench 66.1（非思考设置）超越多数开源与闭源基线；开源权重 + 极低 API 价格，被大量 agent 创业团队直接采用。",
  "被视为'agentic model'类别的定义性工作之一。"],
 ["R1：K2 的工具轨迹合成回应了你平台工具质量依赖人工的痛点——工具数据可合成、行为可 RL，未来的意图路由器也可以这样训。",
  "R1：把 K2 的 self-critique 与你的'LLM 自我优化 prompt'机制对照——同一思想（模型评审模型）在数据与 prompt 两层的应用。"],
 ["场景①'agentic 模型和普通对话模型的差别'｜回答：训练目标不同——K2 专门合成多轮工具交互数据并用 RL 对齐，因此'敢用工具、会用工具、用错能反思'；这解释了为什么 2025 年后原生 agent 模型开始替代工作流编排。",
  "场景②'数据不够怎么训 agent'｜回答：合成轨迹 + rubric 奖励的完整路线。"],
 ["记住 1T-32B、工具数据合成、self-critique RL 三个关键词；思考与你 prompt 迭代闭环的共性。"]),

("p13", "glm-4-5", "GLM-4.5: Agentic, Reasoning, Coding (ARC)",
 "智谱 AI / 清华系", "2025.07", "论文 + 开源模型",
 [("arXiv", "https://arxiv.org/abs/2508.06471"),
  ("GitHub", "https://github.com/zai-org/GLM-4.5")], "D",
 "国产'agentic 原生'旗舰：把思考、工具、代码三类能力统一训练，并提出'参数效率'新叙事。",
 ["统一训练目标：Agentic / Reasoning / Coding（ARC）三能力联合——不做只会聊天不会动手的模型。",
  "Hybrid reasoning：与 Qwen3 同期支持 thinking / direct 双模式——混合思考已是 2025 开源旗舰标配，简单请求不付思考成本（TAU-Bench 70.1% 即 direct 模式成绩）。",
  "Agentic-native 设计：从预训练数据配比到 RL 环境都围绕真实工具使用（浏览器、代码解释器、函数调用）构建。",
  "工程贡献：开源 slime 强化学习基础设施（与 K2/GLM 同源理念），推理友好。"],
 ["官方口径：在全部评测模型中综合第 3、agent 基准第 2（发布时点）；TAU-Bench 70.1%、SWE-bench Verified 64.2%；355B 总参/32B 激活（另有 106B 的 Air 版），预训练 23T tokens；MIT 协议全开源，国内私有化部署热门选择。"],
 ["R1：金融私有化场景的候选底座之一；与你做过的模型对比测试呼应——选型维度除了跑分，还有工具调用稳定性与 license。"],
 ["场景①'国产开源 agent 模型怎么选'｜回答：给一张对比卡——Qwen3（全家桶+端侧）、K2（工具交互最强）、GLM-4.5（ARC 均衡+私有化生态），再按客户约束收敛。"],
 ["了解 ARC 命名与'参数效率'叙事；对比三家（K2/GLM/Qwen3）的 RL 策略差异。"]),

("p14", "longcat-flash", "LongCat-Flash Technical Report",
 "美团 LongCat（龙猫）团队", "2025.09", "论文 + 开源模型",
 [("arXiv", "https://arxiv.org/abs/2509.01322"),
  ("GitHub", "https://github.com/meituan-longcat/LongCat-Flash-Chat")], "D",
 "美团 560B MoE 旗舰：以'零计算专家'实现算力按需分配，为 agent 场景把推理成本做到极致，并在 agent 基准上对标前沿。",
 ["ScMoE（Shortcut-connected MoE）：注意力与 FFN 混合连接，吞吐提升近一倍。",
  "Zero-Computation Experts（零计算专家）：动态判断 token 难度，'难 token 多算、简单 token 少算'——每 token 仅激活 27~31B 参数。",
  "面向 agentic 的系统级工程：大规模 RL 稳定性（不稳定 token 摘除、MTP 并行策略）、推理优化，主打'agent 工作负载下的性价比'。"],
 ["τ-bench 等 agentic 基准对标闭源前沿；开源权重 + GitHub 开放，是国内大厂 2025 下半年最受关注的 agent 底座之一。",
  "后续 LongCat-Flash-Thinking（2509.18883）延续强化推理与 agentic 能力。"],
 ["R3：**Zero-Computation Experts 的'按需分配算力'与你自研的'动态负载自适应调度'是同一思想在不同层的实现**——一个是 GPU 算力按 token 难度分配，一个是请求按负载在引擎间分配。这个类比是全篇最出彩的简历关联。",
  "R2：560B 模型可低成本 serve，靠的是系统级优化——与你高并发/流量整形背景天然共鸣，可谈 agent 时代推理服务化。"],
 ["场景①'agent 时代推理成本怎么降'｜回答：模型层（MoE 激活/零计算专家）+ 服务层（缓存/流控）+ 应用层（上下文工程）三层降本，引用 LongCat 与你自己的实践各占一层。",
  "场景②'你怎么看国产大模型'｜回答：以 LongCat 为例——差异点不再是跑分而是'agentic 场景的单位成本'，工程优化成为模型竞争力的一部分。"],
 ["精读 ZCE 机制；把你做过的动态负载自适应算法与之做一张对比小抄（调度对象、信号、粒度）。"]),

("p15", "tongyi-deepresearch", "Tongyi DeepResearch Technical Report",
 "阿里巴巴（通义实验室）", "2025.10", "论文 + 开源模型",
 [("arXiv", "https://arxiv.org/abs/2510.24701")], "E",
 "专为'长周期深度研究'训练的 30B 级 MoE agent 模型：以极少激活参数在 DeepResearch 系基准全面对标甚至超越闭源旗舰。",
 ["定位：deep research agent——多步检索、交叉验证、长程信息综合，而非单轮问答。",
  "训练配方：大规模 agentic 数据合成 + 可扩展的 agentic RL 管线（覆盖检索、浏览、代码等多工具环境）；推理时支持 ReAct 与 heavy speculation 两种模式。",
  "效率叙事：30.5B 总参 / ~3.3B 激活，验证'小激活参数 + 好 RL = 能干研究活'。"],
 ["在 HLE、BrowseComp、GAIA、WebWalker 等 deep research/agent 基准上居开源第一梯队（发布时点），被称为'开源 Deep Research 之王'。"],
 ["R1：**你的 RAG 知识库是'deep research 的单轮退化形态'**——面试可画演化路线：单轮 RAG → 多轮检索问答 → long-horizon deep research，并说明每一步需要的组件（检索质量→任务规划→验证闭环），而你已具备前两段。",
  "R1：BrowseComp 一节与本文呼应，评测先行思想一致。"],
 ["场景①'你的知识库和 deep research 有什么区别、怎么演进'｜回答：用这条演化路线，强调你已经有的检索、评估、prompt 闭环都是 deep research 的子系统，缺的是任务规划器与长程验证——正好接 Agentic RL 的进展。",
  "场景②'小模型能干研究吗'｜回答：Tongyi 证明可以——激活 3.3B 打平闭源，关键是数据合成 + RL 而不是堆参数。"],
 ["记住 30.5B/3.3B、合成数据 + agentic RL 配方；把'单轮 RAG→deep research'演化图讲熟。"]),

("p16", "agentic-rl-survey", "The Landscape of Agentic Reinforcement Learning for LLMs: A Survey",
 "Oxford / 上海 AI Lab 等", "2025.09", "综述",
 [("arXiv", "https://arxiv.org/abs/2509.02547"),
  ("GitHub", "https://github.com/xhyumiracle/Awesome-AgenticLLM-RL-Papers")], "E",
 "第一篇系统化的 Agentic RL 全景综述：把 LLM agent 重新形式化为时序扩展的 POMDP，综合 500+ 篇工作。",
 ["形式化：agent 交互 = 部分可观测马尔可夫决策过程（POMDP）的时间扩展版，观测/动作/奖励的结构都比传统 RL 复杂得多。",
  "六大核心方向：环境与先验知识探索、奖励设计（可验证奖励/ rubric 奖励/过程奖励）、策略优化（GRPO 系/多轮信用分配）、训练范式（SFT→RL 冷启动）、评测、以及工具集成/记忆/多智能体的 RL 化。",
  "整理了开源环境、基准与框架的实用清单（配套 GitHub 持续维护）。"],
 ["发布数月被引 190+，是 2025 年 agent 训练方向引用速度最快的综述；被多个团队用作内部教材。"],
 ["R1：意图识别路由器未来可以 RL 化——用该综述的 POMDP 语言描述你的系统：观测=用户 query+检索结果，动作=路由/改写/拒答，奖励=最终 QA 正确率。这个描述方式能让面试官看到你的理论纵深。",
  "R5：综述里的'奖励设计=目标定义'与你团队 OKR/验收标准的管理思想同构。"],
 ["场景①'RL 和 SFT 对 agent 各解决什么'｜回答：SFT 教模仿、RL 教结果；agent 的多步性导致信用分配难（综述六方向之一），所以工程上常见 SFT 冷启动 + RL 对齐的组合拳。",
  "场景②'怎么给 agent 设计奖励'｜回答：先可验证（正确性/格式）再 rubric（质量准则），必要时 process reward；引用综述的奖励分类体系。"],
 ["只读引言+形式化+奖励设计三章即可（全文 100+ 页）；把你的平台要素翻译成 POMDP 术语练一遍。"]),

("p17", "ui-tars", "UI-TARS: Pioneering Automated GUI Interaction with Native Agents",
 "字节跳动 Seed 团队", "2025.01", "论文 + 开源模型",
 [("arXiv", "https://arxiv.org/abs/2501.12326"),
  ("GitHub", "https://github.com/bytedance/UI-TARS")], "F",
 "原生 GUI 智能体模型：只看屏幕截图就能像人一样操作界面，统一感知-推理-动作循环。",
 ["原生设计：不依赖 HTML/DOM 等平台特定输入，纯视觉感知 + 统一动作空间（键盘/鼠标/系统调用），跨 Web/桌面/手机。",
  "感知-行动迭代：通过持续观察屏幕状态变化进行多步推理与纠错，内置'反思错误并恢复'的训练数据。",
  "数据工程：大规模 GUI 数据采集 + 指令合成 + 面向错误恢复的增强。"],
 ["发布时在多个 GUI agent 基准（Web/OS/Android）居首；已集成进豆包等字节产品服务上亿用户，开源衍生出 Agent TARS 等项目。"],
 ["与 R1 无直接关联，作为'多模态 agent 交互趋势'的谈资：当面试官问'除了 API 还有什么交互形态'时引出 computer use / GUI agent 一族。"],
 ["场景①'agent 的交互边界'｜回答：API 调用（我的平台）→ 计算机使用（截图操作 GUI，如 UI-TARS/Operator）两条线；企业老系统没有 API 时 GUI agent 是兜底方案。"],
 ["了解'原生 agent（视觉驱动）vs 工作流式 RPA'的差别；不需要深读实验细节。"]),

("p18", "browsecomp-benchmark", "BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents",
 "OpenAI", "2025.04", "论文 + 基准",
 [("arXiv", "https://arxiv.org/abs/2504.12516"),
  ("在线", "https://openai.com/index/browsecomp/")], "F",
 "衡量 browsing agent '坚持与交叉验证能力'的基准：1266 道答案极难找到、但验证极易的问题。",
 ["设计哲学：问题对人类检索困难（答案藏在网页深处、需要多跳交叉验证），但标准答案简短易核对——'难找易验'完美适配 RL 训练与客观评估。",
  "发现：单纯推理模型（o1 等）得分很低，说明 browsing 是独立能力维度；结合浏览工具 + 强推理 + 强化学习的 deep research 系统显著领先。",
  "配套发布 BrowseComp-ZH（中文版，后续社区/港中文等扩展）。"],
 ["成为 2025 年 deep research 类产品（OpenAI、Tongyi、Kimi 等）竞相刷的标志性基准，也推动了'检索 agent'评测方法论。"],
 ["R1：与你的评估闭环同思想——**难找易验**是设计评测集的好原则：你可以在 golden set 里加入'需要跨多个知识文档综合'的题目，并用 BrowseComp 的'易验证'标准控制标注成本。"],
 ["场景①'你们怎么评测检索问答'｜回答：分难度分层（单跳/多跳/无答案），引用 BrowseComp 的难找易验原则与你的分类别准确率口径。"],
 ["看懂'难找易验'的设计动机即可；对比 SQuAD 式静态问答集的局限。"]),

("p19", "bfcl-v3", "Berkeley Function Calling Leaderboard V3（BFCL V3）",
 "UC Berkeley（Gorilla 团队）", "2025.05", "基准 + 论文",
 [("排行榜", "https://gorilla.cs.berkeley.edu/leaderboard.html"),
  ("GitHub", "https://github.com/ShishirPatil/gorilla")], "F",
 "UC Berkeley 出品的函数调用/工具使用权威榜单 V3：从单轮调用进化到多轮、状态记忆与'无关性检测'的 agentic 评测。",
 ["V3 关键升级：多轮多步调用（multi-turn & multi-step）、状态/状态性评估（statefulness——多轮间上下文与执行状态保持）、**irrelevance detection（识别不相关请求，判断工具是否适用、该不该调用）**。",
  "评测维度：AST 匹配 + 实际执行（executable check）+ 响应质量；覆盖上千个真实 API。",
  "已成为学术界与工业界（OpenAI/Anthropic/Google/各家国产模型）工具调用能力的标准参照系。"],
 ["榜单被各模型发布会被引用为'工具调用能力'的权威依据；Gorilla 团队相关成果发表于 ICML/ACL 等顶会。"],
 ["R1：**irrelevance detection 与你的意图识别引擎是同一个问题**——判断'该不该调工具/该走哪条链路'，你的拒答与路由策略就是生产环境的 irrelevance 检测；BFCL 说明这是被公认的一级评测维度。",
  "R1：你的黄金测试集方法论可以类比 BFCL 的执行校验（不只看参数对，还要看跑对）。"],
 ["场景①'工具调用质量怎么评'｜回答：四层——参数结构对、执行能跑通、多轮状态保持、无关请求能拒；引用 BFCL V3 维度并映射到你的意图识别+拒答机制。",
  "场景②'怎么避免模型乱调工具'｜回答：irrelevance 检测作为显式能力测试 + 线上 badcase 回流。"],
 ["浏览榜单看主流模型差距；把 irrelevance detection 这个术语记牢（面试直接复用）。"]),

("p20", "mcp-a2a-protocols", "MCP 与 A2A：Agent 互操作协议双雄",
 "Anthropic（MCP）/ Google 发起、Linux 基金会（A2A）", "MCP 2024.11 发布、2025 年生态爆发；A2A 2025.04", "协议标准",
 [("MCP 官网", "https://modelcontextprotocol.io/"),
  ("A2A 项目", "https://github.com/a2aproject/A2A")], "F",
 "Agent 时代的'USB-C'：MCP 统一模型↔工具/数据的接入，A2A 统一智能体↔智能体的协作，共同构成 agent 互操作协议层。",
 ["MCP（Model Context Protocol）：基于 JSON-RPC 的开放协议，三大原语（Tools/Resources/Prompts），把'接 N 个工具写 N 种胶水'变成'一次实现，处处可用'；2025 年 OpenAI、Google 等相继采纳，成为事实标准，服务器生态爆发。",
  "A2A（Agent2Agent Protocol）：异构智能体间的能力发现（Agent Card）与任务生命周期（task 状态机）协议，'不透明协作'——不暴露对方内部思考，只交换任务与产物；2025 年 6 月捐赠给 Linux 基金会中立治理。",
  "分工：MCP 解决'agent 的手和眼'，A2A 解决'agent 之间的外交'；两者互补构成完整互操作栈。"],
 ["MCP 服务器生态数千计；A2A 获 50+ 企业（微软/SAP/ServiceNow 等）支持；两大协议成为企业 agent 架构评审的必答题。"],
 ["R1：平台的工具接入层可迁移到 MCP——知识库/意图识别能力封装为 MCP Server 后，客户侧 Claude/Cursor/自研 agent 都能直接调用，产品化想象空间大；这正是你 0→1 平台的第二曲线。",
  "R4：协议层的数据序列化与你的 Apache Fury 专长直接相关——agent 间高频小消息的序列化效率、schema 演进兼容是 Fury 的用武之地，可作为'开源贡献 × agent 基础设施'的独特故事。",
  "R5：多智能体协作协议与跨团队协作机制的类比。"],
 ["场景①'工具接入多了以后怎么治理'｜回答：协议标准化（MCP）+ 网关治理（鉴权/限流/审计）两层，引用 MCP 原语与生态数据。",
  "场景②'不同团队的 agent 怎么协作'｜回答：MCP 管资源、A2A 管任务委托——给出一套企业级互操作架构。",
  "场景③被问序列化专长怎么用在 AI 上｜回答：Fury 高性能序列化可优化 agent 消息/推理服务 RPC，跨语言（Java/Python 混合栈）正是 agent 系统常态。"],
 ["MCP 读 Quickstart 与三大原语；A2A 读 Agent Card 示例；想清楚'哪些场景该用哪个协议'。"]),
]

def cat_chip(cat):
    name, color = CATS[cat]
    return f'<span class="chip" style="background:{color}">{cat} · {name}</span>'

def detail_page(p):
    pid, slug, title, org, date, form, links, cat, oneline, points, data, resume, interview, deep = p
    name, color = CATS[cat]
    link_html = " · ".join(f'<a href="{u}" target="_blank">{t}</a>' for t, u in links)
    points_html = "".join(f"<li>{md(x)}</li>" for x in points)
    data_html = "".join(f"<li>{md(x)}</li>" for x in data) if data else "<li>—</li>"
    resume_html = "".join(f"<li><b>{x.split('：')[0]}：</b>{md(x.split('：', 1)[1] if '：' in x else x)}</li>" for x in resume)
    iv_html = "".join(f'<div class="iv">{md(x)}</div>' for x in interview)
    deep_html = "".join(f"<li>{x}</li>" for x in deep)
    resume_tags = " ".join(f'<span class="rtag">{rtag(x)}</span>' for x in resume)
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - Agent 论文深度笔记</title><link rel="stylesheet" href="../assets/style.css"></head>
<body>
<div class="wrap">
<a class="back" href="../index.html">← 返回总览</a>
<div class="catline">{cat_chip(cat)}</div>
<h1>{title}</h1>
<table class="meta">
<tr><th>机构 / 作者</th><td>{org}</td></tr>
<tr><th>时间</th><td>{date}</td></tr>
<tr><th>形式</th><td>{form}</td></tr>
<tr><th>链接</th><td>{link_html}</td></tr>
<tr><th>简历关联</th><td>{resume_tags}</td></tr>
</table>
<div class="oneline">{md(oneline)}</div>

<h2>核心内容</h2>
<ul class="pts">{points_html}</ul>

<h2>关键数据与影响力</h2>
<ul class="pts data">{data_html}</ul>

<h2>与简历项目的关联</h2>
<ul class="pts resume">{resume_html}</ul>

<h2>面试引用场景（场景｜话术）</h2>
<div class="ivs">{iv_html}</div>

<h2>深度学习指引</h2>
<ul class="pts deep">{deep_html}</ul>

<div class="foot">Agent 论文知识库 · 分类 {cat} {name} · 生成于 2026-09</div>
</div></body></html>"""

def paper_card(p):
    pid, slug, title, org, date, form, links, cat, oneline, points, data, resume, interview, deep = p
    name, color = CATS[cat]
    tags = " ".join(f'<span class="rtag">{rtag(x)}</span>' for x in resume)
    return f"""<a class="card" href="papers/{slug}.html">
<div class="card-top"><span class="chip" style="background:{color}">{cat} · {name}</span><span class="date">{date}</span></div>
<h3>{title}</h3>
<div class="org">{org} · {form}</div>
<p>{md(oneline)}</p>
<div class="tags">{tags}</div></a>"""

CSS = """:root{--ink:#111827;--sub:#6b7280;--line:#e5e7eb;--bg:#f8fafc}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;color:var(--ink);background:var(--bg);line-height:1.65;font-size:14.5px}
.wrap{max-width:1080px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:30px;letter-spacing:.5px;margin:6px 0 4px}
h2{font-size:18px;margin:26px 0 10px;padding-bottom:6px;border-bottom:2px solid var(--ink)}
h3{font-size:17px;margin:4px 0 6px}
p{margin:6px 0}
a{color:#2563eb;text-decoration:none}a:hover{text-decoration:underline}
.sub{color:var(--sub);font-size:14px}
.chip{display:inline-block;color:#fff;font-size:11.5px;font-weight:600;padding:2px 9px;border-radius:99px;white-space:nowrap}
.date{color:var(--sub);font-size:12px}
.catline{margin-top:10px}
.back{font-size:13px;color:var(--sub)}
table.meta{width:100%;border-collapse:collapse;margin:14px 0;font-size:13.5px}
table.meta th{width:96px;text-align:left;color:var(--sub);font-weight:600;padding:6px 8px;vertical-align:top;background:#f1f5f9}
table.meta td{padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.oneline{background:#eef2ff;border-left:4px solid #2563eb;padding:10px 14px;border-radius:6px;margin:14px 0;font-size:14.5px}
ul.pts{list-style:none}
ul.pts li{padding:4px 0 4px 18px;position:relative}
ul.pts li::before{content:"▸";position:absolute;left:2px;color:#2563eb}
ul.pts.data li::before{content:"◆";color:#059669}
ul.pts.resume li::before{content:"★";color:#d97706}
ul.pts.deep li::before{content:"›";color:#7c3aed}
.iv{background:#fff;border:1px solid var(--line);border-left:4px solid #d97706;border-radius:6px;padding:9px 12px;margin:8px 0;font-size:13.5px}
.foot{margin-top:34px;color:#9ca3af;font-size:12px;border-top:1px solid var(--line);padding-top:10px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin:14px 0 30px}
.card{display:block;background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;color:inherit;transition:.15s}
.card:hover{border-color:#2563eb;box-shadow:0 2px 10px rgba(37,99,235,.10);text-decoration:none}
.card-top{display:flex;justify-content:space-between;align-items:center;gap:8px;margin-bottom:6px}
.card h3{font-size:15.5px}
.card .org{color:var(--sub);font-size:12.5px;margin-bottom:4px}
.card p{font-size:13px;color:#374151}
.rtag{display:inline-block;background:#f1f5f9;border:1px solid var(--line);border-radius:4px;font-size:11px;padding:1px 6px;margin:2px 3px 0 0;color:#334155}
.hero{background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#fff;border-radius:14px;padding:26px 28px;margin-bottom:24px}
.hero h1{color:#fff}
.hero .sub{color:#cbd5e1}
.stats{display:flex;gap:26px;margin-top:14px;flex-wrap:wrap}
.stats b{font-size:22px;display:block}
.stats span{font-size:12.5px;color:#cbd5e1}
table.tbl{width:100%;border-collapse:collapse;background:#fff;font-size:13px}
table.tbl th{background:#1f4e79;color:#fff;padding:8px 10px;text-align:left;white-space:nowrap}
table.tbl td{padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
table.tbl tr:hover td{background:#f0f6ff}
.sect{display:flex;gap:8px;align-items:center;margin:26px 0 10px}
.sect h2{margin:0;border:none;padding:0}
.callout{background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:10px 14px;font-size:13.5px;margin:10px 0}
"""

def index():
    cats_html = ""
    for c, (name, color) in CATS.items():
        items = [p for p in PAPERS if p[7] == c]
        lis = "".join(f'<li><a href="papers/{p[1]}.html">{p[2]}</a> <span class="sub">— {p[3]}</span></li>' for p in items)
        cats_html += f'<div class="card"><div class="card-top"><span class="chip" style="background:{color}">{c} · {name}</span></div><ul class="pts" style="margin-top:8px">{lis}</ul></div>'
    cards_html = "".join(paper_card(p) for p in PAPERS)
    rows = ""
    for i, p in enumerate(PAPERS, 1):
        pid, slug, title, org, date, form, links, cat, oneline, points, data, resume, interview, deep = p
        name, color = CATS[cat]
        lurl = links[0][1]
        rtags = "、".join(x.split("（")[0].split("：")[0] for x in resume)
        rows += (f'<tr><td>{i}</td><td><a href="papers/{slug}.html">{title}</a></td><td>{org}</td>'
                 f'<td>{date}</td><td><span class="chip" style="background:{color}">{name}</span></td>'
                 f'<td>{rtags}</td><td><a href="{lurl}" target="_blank">链接</a></td></tr>')
    matrix_rows = ""
    keys = list(RESUME.keys())
    for p in PAPERS:
        slug, title = p[1], p[2]
        marks = []
        for k in keys:
            hit = any(k in r for r in p[11])
            marks.append('<td style="text-align:center;color:#2563eb;font-weight:700">●</td>' if hit else '<td style="text-align:center;color:#d1d5db">·</td>')
        matrix_rows += f'<tr><td><a href="papers/{slug}.html">{title}</a></td>' + "".join(marks) + "</tr>"
    matrix_head = "".join(f'<th style="text-align:center">{k}<br><span style="font-weight:400;font-size:10.5px">{RESUME[k][:12]}…</span></th>' for k in keys)
    legend = "".join(f'<div><b>{k}</b> — {v}</div>' for k, v in RESUME.items())
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent 论文知识库（2025–2026.09）· Steven Li</title><link rel="stylesheet" href="assets/style.css"></head>
<body><div class="wrap">
<div class="hero">
<h1>Agent 论文知识库</h1>
<div class="sub">2025 – 2026.09 · 面向面试的系统性梳理 · 为 Steven Li（AI 应用技术负责人 / 软件架构师）定制</div>
<div class="stats">
<div><b>20</b><span>篇典型高引论文</span></div>
<div><b>6</b><span>大分类</span></div>
<div><b>8</b><span>类面试场景话术</span></div>
<div><b>5</b><span>个简历关联项目</span></div>
</div>
</div>

<div class="callout"><b>使用方法：</b>① 面试前 30 分钟只看本页的「面试场景速查表」；② 抽查某篇细节点进 papers/ 深度页（每篇含核心内容 / 关键数据 / 简历关联 / 引用话术 / 深度学习指引）；③ 投递不同岗位时，按「简历关联矩阵」优先准备重合度高的论文。</div>

<h2>六大分类导航</h2>
<div class="grid">{cats_html}</div>

<h2>论文总表（20 篇）</h2>
<table class="tbl">
<tr><th>#</th><th>标题（点击看深度笔记）</th><th>机构</th><th>时间</th><th>分类</th><th>简历关联</th><th>原文</th></tr>
{rows}
</table>

<h2>简历关联矩阵</h2>
<p class="sub">● = 强关联。面试该岗位/话题前，优先准备与目标岗位 JD 重合的行。</p>
<table class="tbl">
<tr><th>论文</th>{matrix_head}</tr>
{matrix_rows}
</table>
<div style="font-size:12px;color:var(--sub);margin-top:8px">{legend}</div>

<h2>面试场景速查表</h2>
<table class="tbl">
<tr><th style="width:180px">面试场景</th><th style="width:210px">引用论文</th><th>30 秒话术要点</th></tr>
<tr><td>RAG / 检索质量优化</td><td>⑤上下文工程综述 ⑥Manus ⑮Tongyi DeepResearch</td><td>检索只是上下文工程的"取"环节，我在分块/重排/摘要压缩三层都做过迭代（QA 90%+）；下一站是 long-horizon 检索（Tongyi 路线）。</td></tr>
<tr><td>多轮对话 / Token 成本</td><td>③多智能体复盘 ⑤Manus ⑦Mem0</td><td>Anthropic：token 用量解释 80% 方差、多智能体 15× 成本；Manus：KV-cache 命中率优先；Mem0：抽取-更新记忆 p95 −91%。我做过摘要压缩，思路同源。</td></tr>
<tr><td>工具调用 / 意图识别</td><td>①Building Effective Agents ⑱BFCL V3 ⑲MCP/A2A</td><td>我的意图识别 = Routing 模式 + BFCL 的 irrelevance detection；工具接入正走向 MCP 标准化。</td></tr>
<tr><td>质量评估与回归</td><td>④The Second Half ⑰BrowseComp ⑱BFCL V3</td><td>下半场拼评测：我建了分类别黄金测试集 + 自动评估 + 显著性检验；评测集设计参考"难找易验"原则。</td></tr>
<tr><td>要不要上多智能体</td><td>③多智能体复盘 ⑧MAST ⑳MCP/A2A</td><td>MAST：约四成失败在 agent 间对齐；Anthropic：15× token 买广度。我的场景串行度高故未上，但具备并行 subagent 的基础设施经验。</td></tr>
<tr><td>模型选型与能力演进</td><td>⑨R1 ⑩Qwen3 ⑪K2 ⑫GLM-4.5 ⑬LongCat</td><td>两时代论：R1 前工程补能力（我做意图路由），R1 后模型原生会规划；选型看任务分布 + 部署约束（私有化→Qwen3/GLM，工具交互→K2）。</td></tr>
<tr><td>高并发 / 性能 / 降本</td><td>⑬LongCat-Flash ⑤Manus ⑥Mem0</td><td>LongCat 零计算专家=算力按需分配，与我自研的动态负载自适应调度同构；加上 KV-cache 与记忆压缩，三层降本。</td></tr>
<tr><td>学习能力 / 技术跟进</td><td>④The Second Half ⑯Agentic RL 综述 ⑯UI-TARS</td><td>用下半场论 + Agentic RL POMDP 框架展示体系化跟进；从 API agent 到 GUI agent 的交互边界扩展。</td></tr>
</table>

<h2>延伸关注（不在 20 篇内，面试加分项）</h2>
<ul class="pts">
<li><a href="https://arxiv.org/abs/2506.06941" target="_blank">The Illusion of Thinking（Apple, 2025.06）</a> — 推理模型在复杂度阈值后的"思考崩塌"，用于回答"推理模型的局限"类批判性问题。</li>
<li><a href="https://arxiv.org/abs/2503.21460" target="_blank">LLM Agent: A Survey on Methodology, Applications and Challenges（2025.03）</a> — 方法论视角的 agent 标准综述。</li>
<li><a href="https://arxiv.org/abs/2510.04618" target="_blank">ACE: Agentic Context Engineering（2025.10）</a> — 把上下文当"可演化 playbook"的自改进方向。</li>
<li>AGENTS.md 仓库规范（OpenAI 等, 2025.08）与 Claude Skills（Anthropic, 2025.10）— agent 工程规范化的最新实践。</li>
<li>Terminal-Bench / SWE-bench Pro（2025）— 端到端任务型基准的下一代。</li>
</ul>

<div class="foot">数据来源：arXiv / 各公司官方博客（2025–2026.09 检索核实）· 引用数随时间变化，面试表述建议用"被引数百次/数千次"量级 · 生成：Steven Li 面试准备知识库</div>
</div></body></html>"""

def main():
    os.makedirs(os.path.join(BASE, "papers"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "assets"), exist_ok=True)
    with open(os.path.join(BASE, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(CSS)
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(index())
    for p in PAPERS:
        with open(os.path.join(BASE, "papers", f"{p[1]}.html"), "w", encoding="utf-8") as f:
            f.write(detail_page(p))
    with open(os.path.join(BASE, "README.md"), "w", encoding="utf-8") as f:
        f.write("# Agent 论文知识库（2025–2026.09）\n\n- index.html 总览（分类 / 总表 / 简历关联矩阵 / 面试场景速查）\n- papers/ 每篇深度笔记\n- 面试前 30 分钟：只看 index 的「面试场景速查表」\n")
    print("pages:", 2 + len(PAPERS))

if __name__ == "__main__":
    main()
