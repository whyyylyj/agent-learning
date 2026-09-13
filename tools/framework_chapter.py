# -*- coding: utf-8 -*-
"""第 9 章 · 典型 Agent 开源框架：实现与落地"""
from figs import svg, R, T, AR, badge, INK, SUB, BLUE, GREEN, AMBER, RED, PURPLE

FIG_FW_MAP = svg(740, 300, (
    T(370, 24, "Agent 框架版图：按'主要解决的问题'分层", 13.5, INK, "middle", "600")
    + R(20, 44, 700, 46, "#eff6ff", BLUE)
    + T(370, 72, "编码智能体（写代码 / 改代码 / 评审）", 12.5, BLUE, "middle", "600")
    + R(20, 98, 700, 46, "#ecfdf5", GREEN)
    + T(370, 126, "通用编排（状态机 / 循环 / 人工介入 / 生态集成）", 12.5, GREEN, "middle", "600")
    + R(20, 152, 700, 46, "#f5f3ff", PURPLE)
    + T(370, 180, "数据与 RAG（接入 · 解析 · 索引 · 查询）", 12.5, PURPLE, "middle", "600")
    + R(20, 206, 700, 46, "#fffbeb", AMBER)
    + T(370, 234, "低代码平台（可视化工作流 · 面向非程序员）", 12.5, AMBER, "middle", "600")
    + T(105, 60, "Claude Code", 12, INK, "middle", "600") + T(255, 60, "OpenAI Codex", 12, INK, "middle", "600")
    + T(95, 114, "LangChain · LangGraph", 12, INK) + T(400, 114, "OpenAI Agents SDK", 12, INK)
    + T(620, 114, "AutoGen · AgentScope", 12, INK)
    + T(105, 166, "LlamaIndex · LlamaParse", 12, INK)
    + T(105, 220, "Dify · Coze（扣子）", 12, INK)
    + T(370, 282, "共同底座：模型原生能力（第 4 章）+ 协议标准化 MCP/A2A（第 6 章）", 12, SUB, "middle", "600")
))

FRAMEWORKS = [
dict(key="cc", name="Claude Code", org="Anthropic",
     pos="终端里的 agentic 编码工具，已泛化为通用 agent 运行时（Agent SDK）",
     focus="极简主循环 + 按需检索（agentic search）+ 权限确认 + 项目记忆",
     concepts=["主循环：LLM + 工具循环", "工具集：Bash/Read/Write/Edit/Grep/Glob", "CLAUDE.md 项目记忆",
               "权限模式（allowlist 确认）", "Hooks 生命周期钩子", "Subagents 子智能体", "MCP 客户端", "Agent SDK"],
     how=["不建代码索引，用 agentic search（grep/glob 即时检索）按需看代码——任何仓库即开即用，无索引过期问题",
          "CLAUDE.md 把项目约定/规范/口径写进上下文——项目记忆工程化",
          "权限模式 + Hooks：危险操作需确认，生命周期可注入审计与自动化",
          "Subagents 隔离上下文处理子任务，主循环不被污染"],
     bagu=[("为什么 Claude Code 不建代码索引（RAG）？", "代码库持续演化，索引天然滞后；grep/glob 即时精确检索 + 语义导航的组合更稳，还省掉索引维护。这是 agentic search 与传统 RAG 的路线之争。"),
           ("CLAUDE.md 是什么？", "项目记忆文件：构建命令、代码规范、拒答口径等约定，自动加载注入上下文——上下文工程（第 2 章）的落地形态。"),
           ("Hooks 用来干什么？", "在工具调用前后注入校验/审计/自动化，比如提交前强制跑 lint、操作后写审计日志。")],
     papers=[("p01", "agent 主循环 = BEA 的 Agent 定义"), ("p05", "CLAUDE.md / 上下文管理 = 上下文工程实践"), ("p20", "MCP 客户端接入生态")],
     tradeoff="每次 agentic search 耗 token 与延迟，换取零索引维护；权限确认换安全，牺牲部分自动化。",
     borrow="R1：把意图规范/拒答口径写成 CLAUDE.md 式项目记忆注入系统上下文；Hooks 思路迁移到平台审计与发布卡点。"),
dict(key="codex", name="OpenAI Codex（CLI + 云端 Agent）", org="OpenAI",
     pos="沙箱优先的编码 agent：本地 CLI + 云端隔离容器并行执行，内置 code review",
     focus="OS 级沙箱（默认断网）+ 审批模式 + AGENTS.md 标准 + 真实 SWE 任务 RL 训练的模型",
     concepts=["沙箱执行：macOS Seatbelt / 容器，网络默认禁用", "审批模式：suggest / auto-edit / full-auto",
               "AGENTS.md 仓库说明标准", "云端隔离容器并行多任务", "Code Review Agent", "codex 系模型：真实 SWE 任务上 RL 训练"],
     how=["沙箱 + 默认断网：让 full-auto 全自动模式的风险可控——跑飞了也出不了沙箱",
          "云端并行：多个任务在隔离容器各自执行，互不干扰",
          "AGENTS.md：一个文件约定各编码 agent 的行为（多家已采纳）——规范化降低协作成本",
          "模型在真实软件工程任务上 RL：补齐'长任务、要验证'的能力"],
     bagu=[("Codex 和 Claude Code 的安全模型差异？", "Codex 是沙箱优先（OS 级隔离 + 默认断网，适合全自动），Claude Code 是权限确认优先（灵活，可叠 devcontainer 沙箱）。选型看自动化程度需求。"),
           ("AGENTS.md 解决什么？", "每个编码 agent 各有一套配置文件 → 统一成一个 Markdown 约定，降低多工具协作成本。")],
     papers=[("p02", "Guardrails 分层的极端实现：沙箱即最强防护栏"), ("p18", "真实 SWE 任务上的验证思路")],
     tradeoff="沙箱限制 vs 能力上限（断网装不了依赖）；云端并行 vs 代码出境顾虑（企业需私有化部署时受限）。",
     borrow="R1：佣金/变更等敏感工具链的执行沙箱化——默认最小权限，白名单放开。"),
dict(key="lang", name="LangChain / LangGraph（+ LangSmith）", org="LangChain Inc.",
     pos="LangChain = LLM 应用通用库（生态最全）；LangGraph = 图/状态机式底层编排，做可控的多步 agent",
     focus="StateGraph（节点/条件边/reducer）+ Checkpoints 持久化（断点恢复 / 时间旅行 / 人工介入）+ LangSmith 可观测与评测",
     concepts=["LCEL 链式组合", "StateGraph：节点 · 边 · 条件边 · reducer", "Checkpoints：持久化状态",
               "Human-in-the-loop 中断", "Subgraphs 子图", "LangSmith：tracing + 评测"],
     how=["复杂 agent 的循环/分支/人工介入用'图'表达：链是单向 DAG，画不出循环与中断",
          "Checkpoint 把每步状态落库：长任务可断点恢复、可时间旅行回滚重放——生产可用性的关键",
          "LangSmith 把 tracing 与评测标准化：每个节点输入输出可查，对应 MAST 的排障需求"],
     bagu=[("为什么 LangGraph 用图而不用链？", "链是单向流水线；agent 需要循环、条件分支、人工中断、失败回滚——图 + checkpoint 原生表达这四件事。"),
           ("LangChain 常被诟病什么？", "抽象层过多导致调试困难、版本变动快——所以重控制场景可退到 LangGraph 或薄抽象自研。")],
     papers=[("p03", "orchestrator-worker ↔ supervisor 图"), ("p08", "tracing/checkpoint 回应 MAST 排障"), ("p16", "环境与评测的工程位")],
     tradeoff="框架生态速度 vs 抽象税与调试黑盒；通用能力 vs 业务深度。",
     borrow="R2：LangGraph checkpoint 与异步轮询框架的断点续跑同源——可讲'我早已手写实现过图框架解决的核心问题'。"),
dict(key="llamaindex", name="LlamaIndex（+ LlamaParse / LlamaCloud）", org="LlamaIndex Inc.",
     pos="数据框架：把'接入 → 解析 → 索引 → 查询'做成一等公民；后扩展事件驱动 Workflows 与 Agents",
     focus="Data connectors（LlamaHub 数百个）· LlamaParse 复杂文档解析 · 多种 Index · Query/Chat Engine · 事件驱动 Workflows",
     concepts=["Data connectors", "LlamaParse（PDF/表格解析）", "VectorStoreIndex / SummaryIndex 等",
               "Query Engine / Chat Engine", "Workflows：事件驱动 @step、支持循环与流式", "FunctionAgent / ReActAgent"],
     how=["复杂文档（PDF 表格/扫描件）解析开箱即用——RAG 质量的天花板往往由解析决定",
          "索引抽象多样：按数据形态选索引，而不是一把向量索引打天下",
          "Workflows 事件驱动：步骤解耦、可流式、可循环——比链更接近 agent 形态"],
     bagu=[("LlamaIndex 和 LangChain 怎么选？", "数据接入与解析复杂度高（PDF/表格/多源）优先 LlamaIndex；多源工具编排、人工介入、状态管理优先 LangGraph；两者可组合使用。"),
           ("为什么解析这么重要？", "RAG 质量天花板 = 解析质量 × 检索质量 × 生成质量；表格切断/漏行是幻觉的重要来源（TAT-QA 类问题的核心难点）。")],
     papers=[("p06", "取/选/压/组 = LlamaIndex pipeline 的学术表达"), ("p07", "记忆组件化"), ("apply", "条款 PDF 表格解析的选型论证")],
     tradeoff="LlamaParse 解析质量 vs 成本（收费）；组件化灵活 vs 集成开箱度。",
     borrow="R1：条款 PDF 表格解析的'采购 LlamaParse vs 自研'论证——直接引用其公开能力与定价做 ROI 分析。"),
]

FW_OTHERS = [
    ("AutoGen（Microsoft）", "对话驱动多智能体；v0.4 重写为事件驱动 actor 模型；已并入 Microsoft Agent Framework（与 Semantic Kernel 合流）"),
    ("CrewAI", "角色化团队（role/goal/backstory + tasks），上手快，适合线性协作流"),
    ("OpenAI Agents SDK（2025.03）", "Agents / Handoffs（移交）/ Guardrails / Sessions / Tracing——Swarm 的生产化"),
    ("Google ADK", "与 Gemini / Vertex 生态绑定，A2A 原生支持"),
    ("Dify / Coze（扣子）", "低代码 LLM 应用平台：可视化工作流 + RAG，适合非程序员快速搭建"),
]

FW_QA = [
    ("LangChain 和 LlamaIndex 的区别？", "通用编排生态 vs 数据/RAG 优先。数据接入与解析复杂选 LlamaIndex；多源工具编排与人工介入选 LangGraph；可组合。"),
    ("LangGraph 为什么用图而不用链？", "链是单向 DAG；agent 需要循环、条件分支、人工中断、失败回滚——图 + checkpoint 原生支持这四件事。"),
    ("Claude Code 为什么不建代码索引？", "agentic search：代码库持续变化索引易过期；即时 grep/glob 精确检索 + 语义导航更稳且免维护。"),
    ("MCP 是什么、解决什么？", "agent↔工具的开放协议（Tools/Resources/Prompts），把 N×M 胶水变成一次实现处处可用。"),
    ("ReAct 和 Plan-and-Execute 的区别？", "ReAct 边想边做（灵活但 token 贵）；Plan-and-Execute 先规划后执行（稳定但适应性差）；复杂任务常先规划后 ReAct。"),
    ("Function calling 的原理？", "schema 约束下模型生成结构化参数 → 运行时执行真实函数 → 结果回填上下文继续推理。"),
    ("agent 死循环/跑飞怎么防？", "步数与预算上限、状态快照回滚、重复动作检测、人工中断——四道保险。"),
    ("多智能体什么时候值得上？", "任务可并行且广度优先 + 验证闭环完备 + 预算可承受 15× token（引 MAST 与 Anthropic 数据）。"),
    ("RAG 到 Agentic RAG 的演进？", "Naive RAG → 检索决策（要不要查/查几路）→ 自反思与改写 → 多跳工具化检索（Search-R1 路线）。"),
    ("怎么避免被框架锁死？", "薄抽象自研核心循环 + 协议标准化（MCP/A2A）+ 把评测当成自己的护城河。"),
]

FW_TRADE = [
    ("自研 vs 框架", "控制/审计/可解释 vs 交付速度", "金融审计场景自研核心循环；MVP 与内部工具用框架"),
    ("图编排 vs 代码编排", "人工介入/断点恢复 vs 轻量直接", "需要 HITL 与长任务恢复用图；简单循环直接代码"),
    ("索引 vs agentic search", "确定性低延迟 vs 零维护不过期", "文档知识库索引；代码/工单类即时检索"),
    ("沙箱 vs 权限确认", "全自动可控 vs 灵活低摩擦", "全自动必须沙箱；半自动确认更灵活"),
    ("多 agent vs 单 agent + 子任务", "广度并行 vs 成本可控", "验证闭环完备且确有并行收益才上多 agent"),
]

FW_FUTURE = [
    "上下文管理成为一等公民：自动压缩 / 分层记忆 / 缓存感知（Manus 路线标准化）",
    "Durable execution 成为标配：断点恢复、时间旅行、人工介入是长任务 agent 的生产门槛",
    "协议生态统一：MCP/A2A 吸收后，框架趋同为'薄运行时 + 模型原生能力'",
    "RL 训练的原生 agent 模型削弱脚手架：规划与工具使用内生化（K2 / codex / LongCat-Thinking 路线）",
    "垂直 agent（金融 / 保险 / 医疗）+ evals 驱动开发：评测集成为公司资产",
]

# ============ 第一人称：设计巧思的观察 → 归纳 → 融会贯通 ============
FW_INSIGHT_OBSERVE = [
    ("Claude Code 最反直觉的巧思：不做索引",
     "我最初默认'用代码库就得先建向量索引'，但 Claude Code 用 grep/glob 即时检索 + 语义导航，完全不建索引。深想一层：代码库是高频变更数据，索引必然滞后；而'精确符号检索 + LLM 语义理解'的组合恰好不需要向量索引。这直接修正了我对知识库检索的选型直觉。"),
    ("Codex 的巧思：把安全做成出厂状态，而不是使用守则",
     "默认断网沙箱，full-auto 全自动也跑不飞。对比不少工具把安全写进文档让用户自觉——安全应该是架构属性，不是纪律要求。"),
    ("LangGraph 的巧思：checkpoint 是 agent 的存档点",
     "状态每步落库，才有时间旅行、人工介入、失败重放。我立刻想到自己的异步轮询框架：断点续跑与状态重放是同一件事，只是发生在请求层而不是 agent 层。"),
    ("LlamaIndex 的巧思：把'解析'当一等公民",
     "RAG 的上限由解析质量决定（金融表格是 TAT-QA 的核心难题），它直接做 LlamaParse 攻最难的一环——在产业链最疼的点上下重手，而不是全面铺开。"),
    ("CLAUDE.md / AGENTS.md 的巧思：用 Markdown 约定代替代码逻辑",
     "把项目规范注入上下文，成本几乎为零；且这是多家工具自发采纳的事实标准——协议标准化也可以自下而上。"),
]

FW_INSIGHT_PRINCIPLES = [
    ("上下文是唯一真相源", "能写成约定/记忆的，不要散落在代码逻辑里——CLAUDE.md、AGENTS.md、系统前缀注入都是同一思想的落地。"),
    ("状态可持久化、过程可重放，agent 才能走向生产", "checkpoint / 显式消息 / 审计日志是分水岭，demo 与产品的差距就在这里。"),
    ("检索策略跟着数据变化频率走", "稳定数据建索引，高频变更数据用即时 agentic search——不存在普适最优，只存在匹配场景。"),
    ("安全边界是一等开关", "沙箱 / 权限 / 确认 / HITL 内建于运行时模式，而不是上线前的补丁。"),
]

FW_INSIGHT_FUSE = [
    ("R1 · AI 应用平台", "意图规范与拒答口径按 CLAUDE.md 思想注入系统前缀（约定即上下文）；评测四维（含误答率）按 BrowseComp/BFCL 原则设计——框架的巧思反哺了平台的一致性与安全性。"),
    ("R2 · 异步轮询框架", "LangGraph checkpoint 的断点恢复 = 我在请求层手写过的状态重放。两个不同层的实现互为印证——面试讲这个类比最能体现融会贯通。"),
    ("实战案例一（保险）", "条款库是低频变更数据 → 建索引；无 API 的老核心系统 → GUI agent 兜底方向（UI-TARS 类）。检索策略跟着数据变化频率走的原则直接落地。"),
    ("实战案例二（DeepResearch）", "多源证据句柄化（文件系统当上下文）控制长报告上下文预算；数据源封装为 MCP 工具复用生态——把巧思迁移进了自己的方案。"),
    ("面试话术", "'我调研框架不看跑分，看它怎么解决我最疼的三个问题：上下文失控、状态丢失、安全边界。Claude Code 教我上下文工程、LangGraph 教我状态持久化、Codex 教我沙箱设计——然后我把这三课搬回了自己的平台。'"),
]

def build(ch, by_id):
    i = FIG_FW_MAP
    rows = ""
    for fw in FRAMEWORKS:
        rows += (f'<tr><td><b>{fw["name"]}</b></td><td>{fw["org"]}</td><td>{fw["pos"]}</td>'
                 f'<td>{fw["focus"]}</td></tr>')
    fw_blocks = ""
    for fw in FRAMEWORKS:
        concepts = "".join(f'<span class="rtag">{c}</span>' for c in fw["concepts"])
        how = "".join(f"<li>{md2(x)}</li>" for x in fw["how"])
        bagu = "".join(f'<div class="iv"><b>Q：{q}</b><br>A：{a}</div>' for q, a in fw["bagu"])
        papers_li = ""
        for p, note in fw["papers"]:
            if p == "apply":
                papers_li += f'<li><a href="../cases/case-minsheng-insurance.html">{note}</a></li>'
                continue
            if p.startswith("case"):
                papers_li += f'<li><a href="../{ch["case"] if False else p + ".html"}">{note}</a></li>' if False else f'<li>{note}</li>'
            else:
                papers_li += f'<li>《{by_id[p][2]}》—— {note}</li>'
        fw_blocks += f"""
<h3>{fw["name"]} <span class="sub">（{fw["org"]}）</span></h3>
<div class="box idea"><b>定位与侧重：</b>{fw["pos"]}。侧重：{fw["focus"]}。</div>
<p><b>核心概念：</b>{concepts}</p>
<p><b>它是如何实现的 / 优势怎么来的：</b></p>
<ul class="pts">{how}</ul>
<p><b>八股问答：</b></p>
{bagu}
<p><b>论文关联：</b></p>
<ul class="pts deep">{papers_li}</ul>
<p><b>工程取舍：</b>{fw["tradeoff"]}</p>
<p><b>实战借鉴：</b>{fw["borrow"]}</p>
<hr style="border:none;border-top:1px dashed #e5e7eb;margin:14px 0">"""
    others = "".join(f'<li><b>{n}</b> — {d}</li>' for n, d in FW_OTHERS)
    qa_rows = "".join(f'<tr><td style="width:46%"><b>{q}</b></td><td>{a}</td></tr>' for q, a in FW_QA)
    trade_rows = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in FW_TRADE)
    future = "".join(f"<li>{x}</li>" for x in FW_FUTURE)
    obs = "".join(f'<div class="iv"><b>{t}</b><br>{d}</div>' for t, d in FW_INSIGHT_OBSERVE)
    prin = "".join(f'<li><b>{t}：</b>{d}</li>' for t, d in FW_INSIGHT_PRINCIPLES)
    fuse = "".join(f'<li><b>{t}：</b>{d}</li>' for t, d in FW_INSIGHT_FUSE)
    borrow = f"""<ul class="pts resume">
<li><b>R1 AI 应用平台：</b>CLAUDE.md 式项目记忆（意图规范/拒答口径注入上下文）；agentic search vs 索引的知识库选型论证；条款表格解析的采购 vs 自研 ROI。</li>
<li><b>R2 异步轮询框架：</b>LangGraph checkpoint 的断点恢复与多路并行取数的并发控制——我早已手写实现过框架解决的核心问题。</li>
<li><b>R3 性能优化：</b>LongCat 零计算专家 / KV-cache / LlamaParse 成本——性能与成本工程在 agent 时代同样稀缺。</li>
<li><b>R4 Apache Fury：</b>agent 消息与推理服务 RPC 的高性能序列化（Java/Python 混合栈常态）。</li>
<li><b>R5 团队管理：</b>用 LangSmith 式 tracing 与评测清单沉淀团队 QA 规范。</li>
</ul>"""
    prev = '<a class="pn" href="../cases/case-finance-deepresearch.html">← 第 8 章：金融 DeepResearch</a>'
    nxt = '<a class="pn" href="ch10.html">下一章：面经与 JD 分析 →</a>'
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第 9 章 {ch["name"]} - Agent 论文知识库</title><link rel="stylesheet" href="../assets/style.css"><style>
table.sel{{width:100%;border-collapse:collapse;background:#fff;font-size:13px;margin:10px 0}}
table.sel th{{background:#1f4e79;color:#fff;padding:7px 10px;text-align:left}}
table.sel td{{padding:7px 10px;border-bottom:1px solid #e5e7eb;vertical-align:top}}
.insight{{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:6px 14px}}
</style></head>
<body><div class="wrap">
<div class="crumbs"><a href="../index.html">首页</a> / 第 9 章</div>
<div class="catline"><span class="chip" style="background:#334155">第 9 章 / 共 10 章</span></div>
<h1>{ch["name"]}</h1>
<div class="box why"><b>本章定位：</b>{ch["why"]}</div>

<h2>一图看懂 · 框架版图</h2>
<div class="figcard">{i}</div>

<h2>总览对比</h2>
<table class="sel"><tr><th>框架</th><th>出品方</th><th>一句话定位</th><th>侧重</th></tr>{rows}</table>

<h2>四大框架深潜</h2>
{fw_blocks}

<h2>归纳总结 · 我观察到的设计巧思</h2>
<div class="insight">{obs}</div>

<h2>融会贯通 · 四条通用设计原则（我的提炼）</h2>
<ul class="pts">{prin}</ul>

<h2>反哺项目实践</h2>
<ul class="pts resume">{fuse}</ul>

<h2>其他框架速览</h2>
<ul class="case-src">{others}</ul>

<h2>工程上的五大取舍</h2>
<table class="sel"><tr><th>取舍</th><th>两端</th><th>判断依据</th></tr>{trade_rows}</table>

<h2>面试八股 Top 10（含一句话答案）</h2>
<table class="sel"><tr><th style="width:42%">问题</th><th>一句话答案</th></tr>{qa_rows}</table>

<h2>未来发展方向</h2>
<ul class="pts">{future}</ul>

<h2>实战项目如何借鉴</h2>
{borrow}

<div class="chapnav">{prev}<a class="pn" href="../cheatsheet.html">速查工具页 →</a>{nxt}</div>
<div class="foot">Agent 论文知识库 · 第 9 章 / 共 10 章 · 框架信息以 2025–2026.09 公开资料为准</div>
</div></body></html>"""

def md2(s):
    return s
