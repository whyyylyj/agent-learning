# -*- coding: utf-8 -*-
"""Agent 论文知识库 v2：章节式多页站点（循序渐进）"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_papers import PAPERS, CATS, RESUME, BASE  # noqa
from figs import FIGS
from struggle import STRUGGLE
from framework_chapter import build as build_framework_chapter
from dimensions import DIM1, DIM1_EXC, DIM2, DIM2_EXC, dim_card
from jd_interviews import build as build_jd_chapter

SHORT = {"R1": "AI 应用平台", "R2": "轮询框架", "R3": "性能优化", "R4": "Apache Fury", "R5": "团队管理"}

def md(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)

def rtag(item):
    key = item.split("：")[0].strip()
    return SHORT.get(key, key)

BY_SLUG = {p[1]: p for p in PAPERS}
BY_ID = {p[0]: p for p in PAPERS}

# ============ 章节（循序渐进学习路径）============
CHAPTERS = [
    dict(no=1, slug="ch1", name="Agent 设计范式与方向",
         why="先建立判断力：什么是 agent、什么时候不用 agent、行业的方向感。这一章不写代码，但决定你后面所有技术叙述的'站位'。",
         papers=["p01", "p02", "p04"],
         goal=["能说出 workflow 与 agent 的区别及五种种基础模式", "能讲'先单智能体后编排'的落地路径", "能用'上下半场论'表达对技术趋势的判断"],
         resume="开场介绍 AI 平台时用 Routing/Evaluator-Optimizer 模式描述自己的意图识别与 Prompt 迭代闭环。"),
    dict(no=2, slug="ch2", name="上下文工程与记忆",
         why="单智能体能不能做好，八成取决于上下文工程。这是你 RAG/多轮对话经验最直接的学科化表达。",
         papers=["p05", "p06", "p07"],
         goal=["掌握 KV-cache / append-only / 记忆库三类工程手段", "能把'摘要压缩 token'讲成上下文工程学科问题", "记住 Mem0 三个数字：+26%、+2%、−91% p95"],
         resume="你的'长对话摘要压缩控 token'对应 Manus 的文件系统与 Mem0 的记忆库——同题不同解，面试对比着讲。"),
    dict(no=3, slug="ch3", name="多智能体：模式、失败与框架",
         why="从单 agent 到多 agent 是 2025 年最大的架构跃迁，但失败率极高——先学失败分类再学框架，避免'为了多智能体而多智能体'。",
         papers=["p03", "p08", "p09"],
         goal=["掌握 orchestrator-worker 拓扑与 15× token 成本账", "记住 MAST 三层级 14 种失败模式", "能给出自研编排 vs 开源框架的选型论证"],
         resume="你 0→1 时选择意图路由的确定性链路而非多智能体——用 MAST 的失败数据反推这个决策的先见性。"),
    dict(no=4, slug="ch4", name="Agentic 底座模型",
         why="模型原生能力（规划/工具/反思）在 2025 年快速内生化，直接改变 agent 架构的分工。理解训练配方，才能做好选型与成本预估。",
         papers=["p10", "p11", "p12", "p13", "p14"],
         goal=["讲清 R1 的 GRPO 与'推理涌现'", "对比 Qwen3/K2/GLM-4.5/LongCat 的定位与适用场景", "把 LongCat 零计算专家与自己动态负载调度类比"],
         resume="你做过 LLM 对比测试——用本章给选型框架：任务分布 × 部署约束 × 单位成本，私有化看 Qwen3/GLM，工具交互看 K2。"),
    dict(no=5, slug="ch5", name="Agent RL 与深度研究",
         why="deep research 是 RAG 的长程演进形态，RL 是它的训练引擎。这一章回答'你的知识库下一步怎么走'。",
         papers=["p16", "p15"],
         goal=["能用 POMDP 语言描述自己的 agent 系统", "掌握 Search-R1→DeepResearcher→Tongyi 的演进线", "设计 deep research 的评测集（难找易验）"],
         resume="你的知识库是 deep research 的单轮退化形态——画出'单轮 RAG → 多轮检索 → 长程研究'的演化路线图。"),
    dict(no=6, slug="ch6", name="交互、评测与协议",
         why="生态与规尺：评测决定你能不能度量，协议决定你的系统能不能被生态调用。",
         papers=["p17", "p18", "p19", "p20"],
         goal=["掌握 BFCL V3 四层工具评测（含 irrelevance 检测）", "能讲 MCP/A2A 的分工与企业级互操作架构", "了解 GUI agent 的交互边界"],
         resume="BFCL 的 irrelevance detection 与你的意图匹配/拒答是同一个问题；MCP 是你平台工具层的标准化出口。"),
    dict(no=7, slug="ch7", name="实战案例一：民生保险知识库平台", case="cases/case-minsheng-insurance.html",
         why="把前六章的范式/上下文/失败分析/评测全部落到保险垂直场景：三条链路、三层意图路由、规则引擎校验。"),
    dict(no=8, slug="ch8", name="实战案例二：基金组合绩效评价（金融 DeepResearch）", case="cases/case-finance-deepresearch.html",
         why="服务银行/保险/券商的基金组合资产配置绩效评价：复用原系统数据层、能力组件封装为工具 API、skill 适配 + Plan/ReAct 混合推理、数字勾稽红线——异步并发功底的迁移。"),
    dict(no=10, slug="ch10", kind="jd", name="面经与 JD 分析：考察重点 · 短板 · 针对性准备",
         why="把知识库对准真实市场：归纳字节 / 阿里 / 腾讯 / 小红书 / 微软 / NVIDIA / OpenAI / Anthropic / Shopee / 宇树等公司 JD 与面经的考察重点，基于简历做短板分析，并用两个实战案例做针对性扩展。",
         companies=["字节系（抖音/豆包/火山）", "阿里系（千问/夸克/百炼）", "百度", "腾讯", "小红书", "微软", "Shopee 虾皮", "NVIDIA", "宇树科技", "OpenAI / Anthropic"],
    ),
    dict(no=9, slug="ch9", kind="fw", name="典型 Agent 开源框架：实现与落地",
         frameworks=["Claude Code", "OpenAI Codex", "LangChain · LangGraph", "LlamaIndex · LlamaParse", "AutoGen · CrewAI", "Dify · Coze"],
         why="框架是论文思想的工业落地。面试必问'用过什么框架、为什么选'——这一章把 Claude Code / Codex / LangChain·LangGraph / LlamaIndex 的定位、核心概念、八股问答与工程取舍一次讲透。"),

]

# ============ 每篇论文的 总分总 enrich ============
E = {
"p01": dict(problem="agent 概念爆火但缺乏统一设计语言，团队容易过度设计、为 agent 而 agent，项目烂尾率高。",
    idea="原则主义：先工作流后智能体；把复杂系统拆成五种可组合的基础模式（Routing/Chaining/Parallel/Orchestrator/Evaluator）；工具接口（ACI）质量决定 agent 上限。",
    summary="它给的不是框架而是判断力——什么时候不该用 agent。后续所有 agent 工程文献都在与它对话。",
    rel=[("related", "p02", "OpenAI 视角的同题指南"), ("next", "p03", "确需多智能体时的模式与成本")]),
"p02": dict(problem="企业知道要落地 agent，但不知道从哪开始、风险怎么控、边界在哪。",
    idea="单智能体优先；编排拓扑三分（Single/Manager/Decentralized）；Guardrails 分层 + 人工升级。",
    summary="把 agent 落地拆成模型/工具/指令/防护栏四件套的工程题。",
    rel=[("pre", "p01", "范式基础"), ("related", "p08", "失败分析反推防护栏设计"), ("next", "p03", "编排的进阶形态")]),
"p04": dict(problem="AI 从业者普遍焦虑：方法迭代太快追不完，不知道该投入哪一侧。",
    idea="上半场（预训练时代）拼方法，下半场拼问题定义、真实环境与可靠度量；'把模糊需求转成可验证规格'是稀缺能力。",
    summary="为'评测先行'提供世界观——这是面试里讲评估闭环时的理论锚点。",
    rel=[("related", "p18", "评测设计的实践样例"), ("related", "p17", "同属评测方法"), ("next", "p16", "下半场的训练侧展开")]),
"p05": dict(problem="长周期 agent 的上下文爆炸与注意力漂移：成本数量级上升、目标丢失、任务失败。",
    idea="KV-cache 命中率是最重要产品指标；append-only 上下文；文件系统当外部记忆；todo 复述操纵注意力；保留错误供学习。",
    summary="上下文工程的第一手实战手册，六条实践可直接移植。",
    rel=[("pre", "p01", "单 agent 设计原则"), ("related", "p07", "记忆的另一种解法（抽取-更新）"), ("next", "p06", "实战的学科化")]),
"p06": dict(problem="上下文相关技巧散落各处（检索/压缩/记忆/工具），缺乏统一学科体系。",
    idea="形式化'上下文工程'：为 LLM 系统化组装正确的信息、工具与格式；覆盖长上下文管理、记忆、检索与工具集成全链路。",
    summary="给自己项目的实践找到学科坐标与共同语言。",
    rel=[("related", "p05", "工业实战印证"), ("related", "p07", "记忆子领域"), ("next", "p15", "长程上下文的前沿应用")]),
"p07": dict(problem="跨会话记忆：全量上下文传递不可扩展（成本/延迟/窗口上限），删减又丢关键信息。",
    idea="两阶段记忆管线（抽取→增删改决策），增量维护替代全量传递；对话级+用户级双层记忆。",
    summary="记忆是上下文工程的专门子问题，生产级数据完备（+26% / +2% / −91% p95）。",
    rel=[("pre", "p05", "上下文工程总纲"), ("related", "p15", "deep research 也依赖记忆"), ("apply", "case1", "多轮场景培训的跨会话记忆")]),
"p03": dict(problem="研究型任务串行执行慢、覆盖窄；单 agent 上下文装不下多源信息。",
    idea="orchestrator-worker：LeadAgent 拆解并行分派 subagent；状态增量保存；用 token 买广度。",
    summary="多智能体的工业级样板，附完整成本账（90.2% 提升 / 15× token / 80% 方差）。",
    rel=[("pre", "p01", "单 agent 与编排模式"), ("related", "p08", "先看失败分类再动手"), ("related", "p09", "框架工程化"), ("apply", "case2", "组件编排的拓扑来源")]),
"p08": dict(problem="多智能体系统经常不如单 agent，失败原因从未被体系化归因。",
    idea="对 LangGraph/AutoGen/CrewAI 真实 trace 实证标注：14 种失败模式、三大层级（规格/智能体间对齐/任务验证），失败大头在 agent 间对齐与验证缺失。",
    summary="给'要不要上多智能体'提供风险清单与排障检查单。",
    rel=[("pre", "p03", "多智能体实现"), ("related", "p02", "防护栏缓解"), ("related", "p09", "运行时缓解"), ("apply", "case1", "验证层实践")]),
"p09": dict(problem="主流 agent 框架黑盒程度高：失败难定位、状态难重放、并发难控。",
    idea="agent as actor + 显式异步消息：并发天然、失败可定位、可重放；配套 Studio 可视化。",
    summary="框架层面系统性回应 MAST 的失败模式。",
    rel=[("pre", "p08", "失败分析"), ("related", "p03", "编排形态对照"), ("apply", "case2", "并行组件编排运行时")]),
"p10": dict(problem="推理能力被闭源模型垄断：开源模型'不会思考'，规划要靠工程流程硬补。",
    idea="纯 RL（GRPO）激发推理涌现（反思/自验证/aha moment）；蒸馏把推理能力迁移给小模型。",
    summary="开源 agent 时代的起点：规划能力开始内生化，工程分工随之改变。",
    rel=[("next", "p11", "hybrid thinking 演进"), ("related", "p12", "RL 训练配方延续"), ("next", "p16", "RL 方法体系化")]),
"p11": dict(problem="企业私有化 agent 部署需要端云协同、成本可控、可商用的模型家族。",
    idea="hybrid thinking/non-thinking 模式可切换 + 0.6B~235B-A22B 全家族开源（Apache 2.0），原生强化工具调用。",
    summary="私有化 agent 部署的事实标准底座。",
    rel=[("pre", "p10", "RL 推理路线"), ("related", "p13", "同为国产私有化热门"), ("apply", "case1", "保险私有化部署选型")]),
"p12": dict(problem="真实工具调用数据稀缺，开源模型'不敢调、不会调'工具。",
    idea="大规模 agentic 数据合成（数千工具轨迹）+ 联合 RL（self-critique rubric 奖励 + 通用可验证奖励）。",
    summary="把'会用工具'变成可训练目标，定义 agentic model 类别。",
    rel=[("pre", "p10", "RL 训练路线"), ("related", "p13", "同代 agentic 旗舰"), ("apply", "case1", "意图路由器 RL 化参考")]),
"p13": dict(problem="agent 同时需要思考、工具、代码三种能力，多数模型只偏其一。",
    idea="ARC 统一训练（Agentic/Reasoning/Coding）+ slime RL 基建 + MIT 全开源。",
    summary="国产 agentic 原生均衡旗舰，私有化生态热门。",
    rel=[("related", "p12", "同代对照"), ("related", "p11", "私有化选型对照")]),
"p14": dict(problem="大参数 MoE 推理成本高，而 agent 工作负载波动大、预算敏感。",
    idea="ScMoE 混合连接 + 零计算专家：按 token 难度自适应分配算力（560B 总参、27~31B 激活）。",
    summary="把'动态负载调度'思想做进模型架构——与你自研的动态负载自适应调度同构。",
    rel=[("related", "p11", "MoE 效率对照"), ("apply", "case2", "推理服务成本规划")]),
"p16": dict(problem="agentic RL 论文爆炸式增长，缺乏统一体系与术语。",
    idea="POMDP 形式化 + 六大研究方向 + 奖励设计分类（可验证/rubric/过程奖励），综合 500+ 工作。",
    summary="agent 训练方向的总地图与共同语言。",
    rel=[("pre", "p10", "R1 的方法学延伸"), ("related", "p15", "训练配方实例"), ("apply", "case2", "取数-校验行为的形式化")]),
"p15": dict(problem="deep research 能力被闭源产品垄断，开源缺乏专门优化的小巧模型。",
    idea="30.5B（激活 3.3B）MoE + 大规模合成数据 + 可扩展 agentic RL，专攻长程信息检索与交叉验证。",
    summary="开源 deep research 的完整训练配方，'小激活参数也能干研究活'。",
    rel=[("pre", "p16", "RL 方法体系"), ("related", "p18", "核心评测基准"), ("related", "p05", "长程上下文工程")]),
"p17": dict(problem="企业大量存量系统没有 API，agent 只能调结构化接口，覆盖受限。",
    idea="纯视觉原生 GUI agent：统一动作空间（键鼠/系统调用），感知-行动迭代，含错误恢复训练数据。",
    summary="交互形态从 API 扩展到'像人一样操作界面'。",
    rel=[("related", "p20", "协议之外的最后一步交互"), ("related", "p18", "GUI 评测生态")]),
"p18": dict(problem="browsing/deep research 缺乏'难且可客观验证'的评测基准。",
    idea="难找易验：1266 道需多跳检索与交叉验证的问题，答案简短易核对，完美适配 RL 与评估。",
    summary="评测设计的方法论样板——可直接迁移到自建评估集。",
    rel=[("related", "p15", "该基准的头部玩家"), ("related", "p16", "评测在 RL 中的角色"), ("apply", "case2", "报告类评测集设计")]),
"p19": dict(problem="工具调用评测停留在单轮参数匹配，无法反映多轮、状态与'该不该调'的判断。",
    idea="V3 升级：multi-turn & multi-step、状态性评估、irrelevance detection（识别不相关请求）。",
    summary="工具调用质量的标准规尺——irrelevance detection 与意图识别/拒答同构。",
    rel=[("related", "p20", "被评测对象通过 MCP 接入"), ("apply", "case1", "意图匹配评测维度")]),
"p20": dict(problem="工具接入 N×M 胶水代码、agent 之间无法互操作，生态碎片化。",
    idea="MCP（agent↔工具，JSON-RPC，Tools/Resources/Prompts）+ A2A（agent↔agent，Agent Card 与任务生命周期，不透明协作）。",
    summary="互操作标准层：MCP 管'手和眼'，A2A 管'外交'。",
    rel=[("related", "p19", "接入后的质量评测"), ("apply", "case2", "数据源封装为 MCP 工具"), ("related", "p17", "GUI 是无 API 时的兜底交互")]),
}

CHAPTER_OF = {}
for ch in CHAPTERS:
    for s in ch.get("papers", []):
        CHAPTER_OF[s] = ch["no"]

def paper_path(slug): return f"papers/{slug}.html"
def chapter_path(no): return f"chapters/ch{no}.html"

def chip(cat): 
    n, c = CATS[cat]
    return f'<span class="chip" style="background:{c}">{cat} · {n}</span>'

def crumb(ch_no, title):
    ch = next(c for c in CHAPTERS if c["no"] == ch_no)
    return f'<div class="crumbs"><a href="../index.html">首页</a> / <a href="../{chapter_path(ch_no)}">第 {ch_no} 章 · {ch["name"]}</a> / {title}</div>'

def rel_html(rel):
    out = ""
    labels = {"pre": ("前置阅读", "#7c3aed"), "related": ("相关论文", "#2563eb"), "next": ("进阶 / 应用", "#059669"), "apply": ("案例应用", "#d97706")}
    for typ, slug, note in rel:
        if typ == "apply":
            out += f'<div class="relitem"><span class="reltag" style="background:#fbebcf;color:#92400e">案例应用</span><a href="../cases/{("case-minsheng-insurance" if slug == "case1" else "case-finance-deepresearch")}.html">{note}</a></div>'
            continue
        lab, col = labels[typ]
        p = BY_ID.get(slug)
        if not p: continue
        out += f'<div class="relitem"><span class="reltag" style="background:{col}1a;color:{col}">{lab}</span><a href="{paper_path(BY_ID[slug][1]).split("/")[-1]}">{p[2]}</a><span class="relnote"> — {note}</span></div>'
    return out or '<div class="relitem sub">—</div>'

def detail_page(p):
    pid, slug, title, org, date, form, links, cat, oneline, points, data, resume, interview, deep = p
    e = E[pid]
    e2 = STRUGGLE[pid]
    ch_no = CHAPTER_OF[pid]
    ch = next(c for c in CHAPTERS if c["no"] == ch_no)
    idx_in_ch = ch["papers"].index(pid)
    name, color = CATS[cat]
    link_html = " · ".join(f'<a href="{u}" target="_blank">{t}</a>' for t, u in links)
    points_html = "".join(f"<li>{md(x)}</li>" for x in points)
    data_html = "".join(f"<li>{md(x)}</li>" for x in data) if data else "<li>—</li>"
    resume_html = "".join(f"<li><b>{rtag(x)}：</b>{md(x.split('：', 1)[1] if '：' in x else x)}</li>" for x in resume)
    iv_html = "".join(f'<div class="iv">{md(x)}</div>' for x in interview)
    deep_html = "".join(f"<li>{x}</li>" for x in deep)
    resume_tags = " ".join(f'<span class="rtag">{rtag(x)}</span>' for x in resume)
    # 章内导航
    prev_s = ch["papers"][idx_in_ch - 1] if idx_in_ch > 0 else None
    next_s = ch["papers"][idx_in_ch + 1] if idx_in_ch + 1 < len(ch["papers"]) else None
    nav_p = f'<a class="pn" href="{paper_path(BY_ID[prev_s][1]).split("/")[-1]}">← 上一篇：{BY_ID[prev_s][2]}</a>' if prev_s else '<span class="pn sub">本篇是本章第一篇</span>'
    nav_n = f'<a class="pn" href="{paper_path(BY_ID[next_s][1]).split("/")[-1]}">下一篇：{BY_ID[next_s][2]} →</a>' if next_s else (f'<a class="pn" href="../cases/case-minsheng-insurance.html">进入下一章：实战案例一 →</a>' if ch_no == 6 else (f'<a class="pn" href="../cases/case-finance-deepresearch.html">进入下一章：实战案例二 →</a>' if ch_no == 7 else '<span class="pn sub">全站完</span>'))
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 第 {ch_no} 章 - Agent 论文知识库</title><link rel="stylesheet" href="../assets/style.css"></head>
<body><div class="wrap">
{crumb(ch_no, title)}
<div class="catline">{chip(cat)}<span class="chip" style="background:#334155">第 {ch_no} 章</span></div>
<h1>{title}</h1>
<table class="meta">
<tr><th>机构 / 作者</th><td>{org}</td></tr>
<tr><th>时间 / 形式</th><td>{date} · {form}</td></tr>
<tr><th>链接</th><td>{link_html}</td></tr>
<tr><th>简历关联</th><td>{resume_tags}</td></tr>
</table>

<h2>总 · 解决什么问题</h2>
<div class="box problem">{md(e["problem"])}</div>
<h2>总 · 主旨思路与设计理念</h2>
<div class="box idea">{md(e["idea"])}</div>

<h2>一图看懂 · 核心机制</h2>
<div class="figcard">{FIGS[pid]}</div>

<h2>分 · 核心要点</h2>
<ul class="pts">{points_html}</ul>

<h2>分 · 关键数据与影响力</h2>
<ul class="pts data">{data_html}</ul>

<h2>总 · 一句话总结</h2>
<div class="box summ">{md(e["summary"])}</div>

<h2>与简历项目的关联</h2>
<ul class="pts resume">{resume_html}</ul>

<h2>面试怎么结合</h2>
<div class="ivs">{iv_html}</div>

<h2>实战复盘 · {e2[0]}</h2>
<div class="strug">{"".join(f'<div class="sstep"><span class="stag">{lab}</span><div>{md(txt)}</div></div>' for lab, txt in e2[1])}</div>

<h2>关联关系</h2>
<div class="relbox">{rel_html(e["rel"])}</div>

<h2>深度学习指引</h2>
<ul class="pts deep">{deep_html}</ul>

<div class="chapnav">{nav_p}<a class="pn" href="../{chapter_path(ch_no)}">↩ 回到本章</a>{nav_n}</div>
<div class="foot">Agent 论文知识库 · 第 {ch_no} 章 · {name} · 生成于 2026-09</div>
</div></body></html>"""

def chapter_page(ch):
    no, name, why = ch["no"], ch["name"], ch["why"]
    blocks = ""
    for s in ch.get("papers", []):
        p = BY_ID[s]
        e = E[s]
        tags = " ".join(f'<span class="rtag">{rtag(x)}</span>' for x in p[11])
        blocks += f"""<div class="tot">
<div class="tot-head"><a href="../{paper_path(BY_ID[s][1])}"><h3>{p[2]}</h3></a><span class="sub">{p[3]} · {p[5]}</span></div>
<div class="tot-grid">
<div class="tot-cell"><b>问题</b>{md(e["problem"])}</div>
<div class="tot-cell"><b>理念</b>{md(e["idea"])}</div>
<div class="tot-cell"><b>总结</b>{md(e["summary"])}</div>
</div>
<div>{tags}</div>
</div>"""
    goals = "".join(f"<li>{g}</li>" for g in ch.get("goal", []))
    resume_line = ch.get("resume", "")
    prev_ch = next((c for c in reversed(CHAPTERS) if c["no"] < no), None)
    next_ch = next((c for c in CHAPTERS if c["no"] > no), None)
    pn = ""
    if prev_ch: pn += f'<a class="pn" href="../{chapter_path(prev_ch["no"])}">← 第 {prev_ch["no"]} 章：{prev_ch["name"]}</a>'
    pn += '<a class="pn" href="../index.html">目录</a>'
    if next_ch: pn += f'<a class="pn" href="../{next_ch.get("case", chapter_path(next_ch["no"]))}">第 {next_ch["no"]} 章：{next_ch["name"]} →</a>'
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第 {no} 章 {name} - Agent 论文知识库</title><link rel="stylesheet" href="../assets/style.css"></head>
<body><div class="wrap">
<div class="crumbs"><a href="../index.html">首页</a> / 第 {no} 章</div>
<div class="catline"><span class="chip" style="background:#334155">第 {no} 章 / 共 10 章</span></div>
<h1>{name}</h1>
<div class="box why"><b>本章定位（循序渐进）：</b>{why}</div>

<h2>本章论文（总分总速览，点击进入深度笔记）</h2>
{blocks}

{f'<h2>本章学习目标</h2><ul class="pts deep">{goals}</ul>' if goals else ''}
{f'<div class="box ideab"><b>与简历项目的关联：</b>{resume_line}</div>' if resume_line else ''}

<div class="chapnav">{pn}</div>
<div class="foot">Agent 论文知识库 · 第 {no} 章 / 共 10 章</div>
</div></body></html>"""

def case_page_patch():
    """幂等：清理历史导航后重建案例页章节导航"""
    import re as _re
    NAV = {
        "cases/case-minsheng-insurance.html": dict(label="第 7 章 · 实战案例一", prev=None,
            next=("cases/case-finance-deepresearch.html", "下一章：金融 DeepResearch →"),
            deep=("cases/case1-deepdive.html", "🔍 深挖 10 维度")),
        "cases/case-finance-deepresearch.html": dict(label="第 8 章 · 实战案例二",
            prev=("cases/case-minsheng-insurance.html", "← 上一章：民生保险知识库平台"),
            next=("cases/case-billing-platform.html", "实战案例三：平台计费系统 →"),
            deep=("cases/case2-deepdive.html", "🔍 深挖 10 维度")),
    }
    for rel, cfg in NAV.items():
        path = os.path.join(BASE, rel)
        html = open(path, encoding="utf-8").read()
        html = _re.sub(r'<div class="chapnav">.*?</div>\s*', "", html, flags=_re.S)
        html = _re.sub(r'<div class="crumbs"><span class="chip" style="background:#334155">[^<]*</span></div>', "", html)
        chip = f'<div class="crumbs"><span class="chip" style="background:#334155">{cfg["label"]}</span></div>'
        html = html.replace('<a class="back" href="../index.html">← 返回总览</a>',
            '<a class="back" href="../index.html">← 返回总览</a>' + chip, 1)
        navlinks = '<a class="pn" href="../index.html">目录</a>'
        if cfg.get("prev"):
            navlinks += f'<a class="pn" href="../{cfg["prev"][0]}">{cfg["prev"][1]}</a>'
        if cfg.get("next"):
            navlinks += f'<a class="pn" href="../{cfg["next"][0]}">{cfg["next"][1]}</a>'
        if cfg.get("deep"):
            navlinks += f'<a class="pn" href="../{cfg["deep"][0]}">{cfg["deep"][1]}</a>'
        html = html.replace('<div class="foot">', f'<div class="chapnav">{navlinks}</div><div class="foot">', 1)
        open(path, "w", encoding="utf-8").write(html)

def portal():
    ch_cards = ""
    for ch in CHAPTERS:
        if ch.get("kind") == "fw":
            inner = "".join(f'<li>{x}</li>' for x in ch["frameworks"])
            ch_cards += f"""<a class="card" href="{chapter_path(ch["no"])}">
<div class="card-top"><span class="chip" style="background:#334155">第 {ch["no"]} 章</span><span class="date">框架对比</span></div>
<h3>{ch["name"]}</h3>
<p>{ch["why"]}</p><ul class="mini">{inner}</ul></a>"""
            continue
        if ch.get("kind") == "jd":
            inner = "".join(f'<li>{x}</li>' for x in ch["companies"])
            ch_cards += f"""<a class="card" href="{chapter_path(ch["no"])}">
<div class="card-top"><span class="chip" style="background:#334155">第 {ch["no"]} 章</span><span class="date">面经 · JD</span></div>
<h3>{ch["name"]}</h3>
<p>{ch["why"]}</p><ul class="mini">{inner}</ul></a>"""
            continue
        if ch["no"] <= 6:
            inner = "".join(f'<li>{BY_ID[s][2]}</li>' for s in ch["papers"])
            ch_cards += f"""<a class="card" href="{chapter_path(ch["no"])}">
<div class="card-top"><span class="chip" style="background:#334155">第 {ch["no"]} 章</span><span class="date">{len(ch["papers"])} 篇</span></div>
<h3>{ch["name"]}</h3>
<p>{ch["why"]}</p><ul class="mini">{inner}</ul></a>"""
        else:
            inner = ch.get("why", "")
            ch_cards += f"""<a class="card case" href="{ch["case"]}" style="background:#fffdf5">
<div class="card-top"><span class="chip" style="background:#92400e">第 {ch["no"]} 章 · 实战案例</span></div>
<h3>{ch["name"]}</h3><p>{inner}</p></a>"""
    ch_cards += """<a class="card case" href="cases/case-billing-platform.html" style="background:#f5f8ff">
<div class="card-top"><span class="chip" style="background:#1e3a8a">实战案例 3 · 平台商业化</span></div>
<h3>Agent 平台计费系统：预付费点数 × 次数+流量 × API 倍数</h3>
<p>充值点数预付费；扣点 = API 倍数 ×（调用基础点 + token 流量点）；两阶段冻结-结算、Redis 原子扣减防超卖、幂等与对账——支付级工程问题域在 AI 平台的落地。</p></a>"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent 论文知识库 · Steven Li</title><link rel="stylesheet" href="assets/style.css"></head>
<body><div class="wrap">
<div class="hero">
<h1>Agent 论文知识库</h1>
<div class="sub">2025 – 2026.09 · 章节式 · 循序渐进 · 为 Steven Li（AI 应用技术负责人 / 软件架构师）定制</div>
<div class="stats">
<div><b>20</b><span>篇典型高引论文</span></div><div><b>10</b><span>章学习路径</span></div><div><b>3</b><span>个实战案例</span></div><div><b>10</b><span>类面试场景话术</span></div>
</div>
</div>

<div class="callout"><b>使用方法：</b>按第 1→6 章顺序精读（每章 30~60 分钟），第 7/8 章是两个实战案例（你的简历项目），面试前 30 分钟只看<a href="cheatsheet.html">速查工具页</a>。每篇论文都按「总分总」组织：解决什么问题 → 主旨与设计理念 → 分要点 → 一句话总结。</div>

<h2>学习路径 · 共 8 章</h2>
<p class="sub">顺序即依赖：范式 → 单智能体工程 → 多智能体 → 底座模型 → RL 与深度研究 → 评测与协议 → 两个实战案例收束。</p>
<div class="grid">{ch_cards}</div>

<h2>快速入口</h2>
<div class="grid">
<a class="card" href="cheatsheet.html"><div class="card-top"><span class="chip" style="background:#b91c1c">面试前 30 分钟</span></div><h3>速查工具页</h3><p>面试场景速查表（10 类话术）/ 论文总表 / 简历关联矩阵 / 面试前夜清单。</p></a>
<a class="card" href="checklist.html"><div class="card-top"><span class="chip" style="background:#b45309">数据收尾</span></div><h3>待填真实数据清单</h3><p>38 个效果数字占位：按维度列出要填什么、去哪里找——填完即为最终版。</p></a>
<a class="card" href="edd-learning.html"><div class="card-top"><span class="chip" style="background:#059669">方法论专题</span></div><h3>EDD 评估驱动开发学习目录</h3><p>博客 / 书籍 / 论文 / 工具四层资料 + 5 天学习路径 + 与两个实战案例的勾连复用。</p></a>
</div>

<h2>七天冲刺计划（每天 60–90 分钟）</h2>
<table class="tbl">
<tr><th style="width:70px">天</th><th style="width:280px">内容</th><th>当天产出（自测标准）</th></tr>
<tr><td><b>D1</b></td><td>第 1 章范式五模式 + 第 9 章框架版图（上半）</td><td>能脱口说出五种模式与适用信号；能画框架分层版图</td></tr>
<tr><td><b>D2</b></td><td>第 2 章上下文工程（Manus/CE 综述/Mem0）+ 案例一主页</td><td>能讲"上下文是操作系统"的比喻与三层降本</td></tr>
<tr><td><b>D3</b></td><td>第 3 章 MAST 失败分析 + 案例一 deep-dive 10 维</td><td>10 个维度各能展开 1 分钟；异常 case 能举 3 个</td></tr>
<tr><td><b>D4</b></td><td>第 4 章评测 + 第 5 章模型演进（R1→Qwen3→K2/GLM/LongCat 对比卡）</td><td>能背"两时代论"与国产四模型一句话定位</td></tr>
<tr><td><b>D5</b></td><td>案例二主页 + deep-dive + Tongyi DeepResearch</td><td>能白板画 skill→Plan DAG→组件编排链路；讲清数字不过 LLM 与数据层复用决策</td></tr>
<tr><td><b>D6</b></td><td>第 6 章协议（BFCL/MCP/A2A）+ 第 9 章下半（归纳与反哺）</td><td>能讲四条设计原则各自的实战出处</td></tr>
<tr><td><b>D7</b></td><td>第 10 章面经对照 + 速查页 + 填完 <a href="checklist.html">数据清单</a> + 口述模拟 3 遍</td><td>三个开场故事录音回听各 60 秒无卡顿</td></tr>
</table>
<div style="font-size:12.5px;color:var(--sub);margin:6px 0 18px">顺序设计原则：先范式（词汇表）→ 再上下文/失败（深挖弹药）→ 后模型/协议（选型视野）→ 案例贯穿每天复盘。面试提前到来时：只走 D1→D3→D5→速查页。</div>

<div class="foot">数据来源：arXiv / 各公司官方博客（2025–2026.09 检索核实）· 引用数表述建议用量级 · Steven Li 面试准备知识库</div>
</div></body></html>"""

def cheatsheet():
    # 从旧 index 中提取场景速查表与总表逻辑（直接重建内容）
    scenario_rows = [
    ("RAG / 检索质量优化", "⑤Manus ⑥上下文工程综述 ⑮Tongyi DeepResearch", "检索只是上下文工程的“取”环节，我在分块/重排/摘要压缩三层都做过迭代（QA 90%+）；下一站是 long-horizon 检索（Tongyi 路线）。"),
    ("多轮对话 / Token 成本", "③多智能体复盘 ⑤Manus ⑦Mem0", "Anthropic：token 用量解释 80% 方差、多智能体 15× 成本；Manus：KV-cache 命中率优先；Mem0：抽取-更新记忆 p95 −91%。我做过摘要压缩，思路同源。"),
    ("工具调用 / 意图识别", "①Building Effective Agents ⑲BFCL V3 ⑳MCP/A2A", "我的意图识别 = Routing 模式 + BFCL 的 irrelevance detection；工具接入正走向 MCP 标准化。"),
    ("质量评估与回归", "④The Second Half ⑱BrowseComp ⑲BFCL V3", "下半场拼评测：我建了分类别黄金测试集 + 自动评估 + 显著性检验；评测集设计参考“难找易验”原则。"),
    ("要不要上多智能体", "③多智能体复盘 ⑧MAST ⑳MCP/A2A", "MAST：约四成失败在 agent 间对齐；Anthropic：15× token 买广度。我的场景串行度高故未上，但具备并行 subagent 的基础设施经验。"),
    ("模型选型与能力演进", "⑩R1 ⑪Qwen3 ⑫K2 ⑬GLM-4.5 ⑭LongCat", "两时代论：R1 前工程补能力（我做意图路由），R1 后模型原生会规划；选型看任务分布 + 部署约束（私有化→Qwen3/GLM，工具交互→K2）。"),
    ("高并发 / 性能 / 降本", "⑭LongCat-Flash ⑤Manus ⑦Mem0", "LongCat 零计算专家=算力按需分配，与我自研的动态负载自适应调度同构；加上 KV-cache 与记忆压缩，三层降本。"),
    ("学习能力 / 技术跟进", "④The Second Half ⑯Agentic RL 综述 ⑰UI-TARS", "用下半场论 + Agentic RL POMDP 框架展示体系化跟进；从 API agent 到 GUI agent 的交互边界扩展。"),
    ("框架选型（LangChain/LlamaIndex/自研）", "第 9 章 · 典型 Agent 开源框架", "版图分层定位（编码/编排/数据/低代码）+ 五大取舍（自研vs框架、图vs代码、索引vs agentic search、沙箱vs确认、多vs单 agent）+ 我提炼的四条设计原则。"),
    ("求职针对性准备", "第 10 章 · 面经与 JD 分析", "按目标公司（字节/阿里/腾讯/微软/NVIDIA…）对照强项短板，用两个实战案例做针对性扩展；短板补齐计划（训练侧/多模态/英文/Go）。"),
    ("计费 / 商业化 / 配额", "实战案例三 · 平台计费系统", "预付费点数 + 次数/流量双维 + API 倍数；两阶段冻结-结算、Redis 原子扣减防超卖、幂等与对账——把'成本工程'讲到商业闭环。"),
    ]
    srows = "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>' for a, b, c in scenario_rows)
    trows = ""
    for i, p in enumerate(PAPERS, 1):
        pid, slug, title, org, date, form, links, cat, oneline, points, data, resume, interview, deep = p
        n, c = CATS[cat]
        rtags = "、".join(rtag(x) for x in resume)
        trows += (f'<tr><td>{i}</td><td><a href="{paper_path(slug)}">{title}</a></td><td>{org}</td><td>{date}</td>'
                  f'<td><span class="chip" style="background:{c}">{n}</span></td><td>{rtags}</td></tr>')
    mrows = ""
    keys = list(RESUME.keys())
    for p in PAPERS:
        marks = "".join('<td style="text-align:center;color:#2563eb;font-weight:700">●</td>' if any(k in r for r in p[11]) else '<td style="text-align:center;color:#d1d5db">·</td>' for k in keys)
        mrows += f'<tr><td><a href="{paper_path(p[1])}">{p[2]}</a></td>{marks}</tr>'
    mhead = "".join(f'<th style="text-align:center">{k}</th>' for k in keys)
    legend = "".join(f'<div><b>{k}</b> — {v}</div>' for k, v in RESUME.items())
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>速查工具页 - Agent 论文知识库</title><link rel="stylesheet" href="assets/style.css"></head>
<body><div class="wrap">
<div class="crumbs"><a href="index.html">首页</a> / 速查工具页</div>
<h1>速查工具页（面试前 30 分钟）</h1>

<h2>面试场景速查表（11 类话术）</h2>
<table class="tbl"><tr><th style="width:170px">面试场景</th><th style="width:220px">引用论文</th><th>30 秒话术要点</th></tr>{srows}</table>

<h2>论文总表（20 篇）</h2>
<table class="tbl"><tr><th>#</th><th>标题</th><th>机构</th><th>时间</th><th>分类</th><th>简历关联</th></tr>{trows}</table>

<h2>简历关联矩阵</h2>
<table class="tbl"><tr><th>论文</th>{mhead}</tr>{mrows}</table>
<div style="font-size:12px;color:var(--sub);margin:8px 0 20px">{legend}</div>

<h2>延伸阅读</h2>
<ul class="pts">
<li><a href="https://arxiv.org/abs/2506.06941" target="_blank">The Illusion of Thinking（Apple, 2025.06）</a> — 推理模型复杂度阈值后的"思考崩塌"，回答"推理模型的局限"类问题。</li>
<li><a href="https://arxiv.org/abs/2503.21460" target="_blank">LLM Agent: A Survey on Methodology, Applications and Challenges（2025.03）</a> — 方法论视角标准综述。</li>
<li><a href="https://arxiv.org/abs/2510.04618" target="_blank">ACE: Agentic Context Engineering（2025.10）</a> — 上下文当"可演化 playbook"。</li>
<li>AGENTS.md（OpenAI 等, 2025.08）· Claude Skills（Anthropic, 2025.10）· Terminal-Bench / SWE-bench Pro（2025）。</li>
</ul>

<h2>面试前夜清单（10 分钟过一遍）</h2>
<ul class="pts">
<li><b>三个开场故事各 60 秒：</b>①保险三链路（条款 RAG / 佣金数字不过 LLM / 变更规则引擎）②基金组合绩效评价（数据层复用 + 组件 API + skill×Plan/ReAct + 数字勾稽）③异步轮询 10× QPS 迁移。</li>
<li><b>三组硬数字：</b>90%+ QA 准确率 / +35% 满意度 / +25% 响应准确率；20s→100ms、O(nlogn)→O(1)；Anthropic 90.2%·15×·80% 方差。</li>
<li><b>三个"我做的决策"：</b>不上多智能体（MAST 依据）· 三层意图路由（否掉"换更大模型"）· 评测先行（下半场论）。</li>
<li><b>两个诚实边界预答：</b>训练侧无生产经验（定界话术：我负责推理侧工程与评测，训练侧了解原理与数据配方）· GUI agent 无实战（风险+沙箱观点）。</li>
<li><b>一个反问准备：</b>"贵团队 agent 的评测体系现在怎么建设？"（体现 Second Half 思维）</li>
<li><b><a href="checklist.html">待填真实数据清单</a></b>——把 34 个占位数字换成真实值，所有话术即为最终版。</li>
</ul>
<div class="chapnav"><a class="pn" href="index.html">← 回到目录</a></div>
<div class="foot">Agent 论文知识库 · 速查工具页</div>
</div></body></html>"""

CSS_ADD = """
.crumbs{font-size:12.5px;color:#6b7280;margin-bottom:10px}
.crumbs a{color:#2563eb}
.box{border-radius:10px;padding:12px 16px;margin:10px 0;font-size:14px;line-height:1.7}
.box.problem{background:#fef2f2;border-left:4px solid #dc2626}
.box.idea{background:#eff6ff;border-left:4px solid #2563eb}
.box.summ{background:#ecfdf5;border-left:4px solid #059669}
.box.why{background:#f8fafc;border-left:4px solid #334155}
.box.ideab{background:#fffbeb;border-left:4px solid #d97706}
.figcard{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:12px 14px;margin:10px 0}
.strug{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:6px 14px}
.sstep{display:flex;gap:12px;padding:9px 0;border-bottom:1px dashed #eef2f7;font-size:13.5px;line-height:1.65}
.sstep:last-child{border-bottom:none}
.stag{flex:0 0 96px;text-align:center;font-weight:700;font-size:12px;color:#1f4e79;background:#eef2ff;border-radius:6px;padding:3px 0;height:fit-content;margin-top:2px}
.figcard svg{display:block;width:100%;height:auto}
.tot{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px 16px;margin:12px 0}
.tot-head{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap}
.tot-head h3{margin:0;font-size:15.5px}
.tot-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:10px 0 8px}
.tot-cell{background:#f8fafc;border:1px solid #eef2f7;border-radius:8px;padding:8px 10px;font-size:12.5px;line-height:1.6}
.tot-cell b{display:block;color:#1f4e79;margin-bottom:3px;font-size:12px}
.relbox{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:10px 14px}
.relitem{padding:5px 0;font-size:13.5px}
.reltag{display:inline-block;font-size:11px;font-weight:600;padding:1px 7px;border-radius:4px;margin-right:8px}
.relnote{color:#6b7280;font-size:12.5px}
.chapnav{display:flex;gap:10px;flex-wrap:wrap;margin:26px 0 6px;border-top:1px solid #e5e7eb;padding-top:14px}
.pn{background:#fff;border:1px solid #cbd5e1;border-radius:8px;padding:7px 13px;font-size:13px;color:#1f4e79}
.pn:hover{background:#eff6ff;text-decoration:none}
ul.mini{margin-top:6px;font-size:12.5px;color:#374151;list-style:none}
ul.mini li::before{content:"· ";color:#2563eb}
.card.case{border-color:#fde68a}
"""

# ============ 待填真实数据清单 ============
def build_checklist():
    G1 = [
        ("多知识库切分", "跨库污染导致的错答基本清零", "清零前后的错答计数或比例", "错答案例库 / QA 回归记录"),
        ("权限管控", "越权用例通过率 100%", "安全用例集规模（多少条越权用例）", "安全测试清单"),
        ("数据正确性校验", "解析类坏例下降 __%；口径投诉清零", "坏例下降比例", "解析失败日志抽样"),
        ("意图路由", "Top1 __%；首响 2s→__ms；token −__%", "三个数：准确率 / 延迟 / 成本", "网关埋点 + LLM 用量账单"),
        ("抽检成本", "抽检成本降约七成", "确认或修正实际比例", "抽检工时前后对比"),
        ("佣金链路", "纠纷相关工单下降 __%", "工单降幅", "客服工单系统"),
        ("保单变更识别", "抽取准确率 __%", "字段抽取准确率", "标注评测集"),
        ("幻觉治理", "分类别幻觉率 __%，压至门槛以下", "门槛值与实测值", "幻觉抽检报表"),
        ("埋点冷启动", "一个月 __ 条 query、__ 类系统性问题", "query 量级 / 问题类别数", "日志平台"),
        ("上下文压缩", "多轮约束保持率 __%；输入 token −__%", "两个百分比", "AB 对照实验"),
    ]
    G2 = [
        ("skill 适配", "场景-技能匹配率 __%；框架完整执行率 __%", "两个比率", "标注评测集 / 探针"),
        ("组件封装", "工具调用一次成功率 __%", "成功率", "网关调用日志"),
        ("Plan+ReAct", "任务完成率 / 循环发生率", "两个指标", "任务黑板监控"),
        ("并行编排", "单次评价 __分钟 → __秒", "前后时延", "调度看板"),
        ("勾稽校验", "数字勾稽一致率 100%（硬门槛）", "实际值与口径标签覆盖率", "勾稽回归"),
        ("结果交叉校验", "数字类结论双源一致率 __%", "一致率阈值", "校验批跑结果"),
        ("推断标记", "数字错误率降至 __", "错误率数值", "人工复核抽样"),
        ("分段生成", "节间矛盾率下降 __%", "矛盾率降幅", "一致性检查脚本"),
        ("上下文预算", "保留 __% 关键信息，质量无感损失", "信息保留率", "压缩前后评测对比"),
        ("成本工程", "单次任务成本下降 __%", "成本降幅", "token 账单对比"),
        ("评测体系", "每次改进可量化 __", "黄金集规模 / 门禁指标", "评测平台"),
        ("RL 演进", "完成 RL 化的数据与奖励准备【进展】", "一句话进度（诚实即可）", "—"),
    ]
    G3 = [
        ("p01", "Anthropic·工作流", "意图 Top1 __%"),
        ("p02", "OpenAI·实践指南", "无依据输出降至 __%"),
        ("p03", "Anthropic·多智能体", "报告分钟级【实测数据】"),
        ("p05", "Manus·上下文工程", "输入 token −__%"),
        ("p10", "混合智能体架构", "单次成本可控 __%"),
        ("p11", "Qwen3 私有化选型", "分类别得分"),
        ("p14", "LongCat·降本", "单位成本 −__%"),
        ("p15", "Tongyi DeepResearch", "原型指标"),
        ("p19", "BFCL·误答门禁", "红线阈值"),
        ("p20", "MCP 接入", "进度（规划/推进中）"),
    ]
    G4 = [
        ("API 倍数表", "倍数按链路复杂度 × 模型档位 × SLA 设计", "各 API 真实倍数值（1.0/2.0/8.0…按项目校准）", "定价文档 / 配置中心"),
        ("费率口径", "流量点 = 输入 token×输入费率 + 输出 token×输出费率", "输入/输出费率、点数-人民币换算", "商务定价表"),
        ("非 LLM 折算", "字节 / 页数折算等价点", "折算系数", "成本观测"),
        ("计费准确率", "幂等 + 对账兜底", "对账 diff 零差异持续天数 / 影子验证结果", "对账任务报表"),
        ("悬挂冻结治理", "TTL + 补偿任务自动解冻", "解冻时效（如 P99 &lt; 5 分钟）", "补偿任务监控"),
        ("并发防超卖", "Redis Lua 原子扣减", "负余额穿透次数（目标 0）/ 峰值扣减 QPS", "风控告警记录"),
    ]
    def rows(items):
        return "".join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>'
                       for a, b, c, d in items)
    g3rows = "".join(
        f'<tr><td><a href="papers/{BY_ID[s][1]}.html">{t}</a></td><td>{n}</td></tr>' for s, t, n in G3)
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>待填真实数据清单 - Agent 论文知识库</title><link rel="stylesheet" href="assets/style.css"></head>
<body><div class="wrap">
<div class="crumbs"><a href="index.html">首页</a> / 待填真实数据清单</div>
<h1>待填真实数据清单（38 项）</h1>
<div class="box why"><b>为什么有这张表：</b>知识库的话术骨架已完整，但深挖页与复盘里的效果数字还留着【占位】。这 34 个数字只有你能填——填完后所有页面的黄色占位即为最终版，面试时每个数字都有出处、经得起追问。</div>
<div class="box idea"><b>怎么诚实地填：</b>① 记不清就用区间或量级（"约三成""下降 40% 左右"），不要编精确值；② 区分灰度与全量口径；③ 填完同步改对应页面源码（tools/dimensions.py、tools/struggle.py）后重建。</div>

<h2>一、案例一：民生保险 deep-dive（10 项）</h2>
<table class="tbl"><tr><th style="width:130px">维度</th><th>当前话术</th><th style="width:200px">要填什么</th><th style="width:160px">建议来源</th></tr>{rows(G1)}</table>

<h2>二、案例二：基金组合绩效评价 deep-dive（12 项）</h2>
<table class="tbl"><tr><th style="width:130px">维度</th><th>当前话术</th><th style="width:200px">要填什么</th><th style="width:160px">建议来源</th></tr>{rows(G2)}</table>

<h2>三、论文页实战复盘（10 项）</h2>
<table class="tbl"><tr><th style="width:220px">论文页</th><th>待填数字</th></tr>{g3rows}</table>

<h2>四、实战案例三：平台计费系统（6 项）</h2>
<table class="tbl"><tr><th style="width:130px">维度</th><th>当前话术</th><th style="width:220px">要填什么</th><th style="width:160px">建议来源</th></tr>{rows(G4)}</table>

<div class="chapnav"><a class="pn" href="index.html">← 回到目录</a><a class="pn" href="cheatsheet.html">速查工具页 →</a></div>
<div class="foot">Agent 论文知识库 · 数据完整性工具页</div>
</div></body></html>"""


def main():
    os.makedirs(os.path.join(BASE, "chapters"), exist_ok=True)
    os.makedirs(os.path.join(BASE, "papers"), exist_ok=True)
    css_old = open(os.path.join(BASE, "assets", "style.css"), encoding="utf-8").read()
    with open(os.path.join(BASE, "assets", "style.css"), "w", encoding="utf-8") as f:
        f.write(css_old + CSS_ADD)
    with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
        f.write(portal())
    with open(os.path.join(BASE, "cheatsheet.html"), "w", encoding="utf-8") as f:
        f.write(cheatsheet())
    with open(os.path.join(BASE, "checklist.html"), "w", encoding="utf-8") as f:
        f.write(build_checklist())
    for p in PAPERS:
        with open(os.path.join(BASE, "papers", f"{p[1]}.html"), "w", encoding="utf-8") as f:
            f.write(detail_page(p))
    for ch in CHAPTERS:
        if "case" in ch:
            continue
        if ch.get("kind") == "fw":
            with open(os.path.join(BASE, chapter_path(ch["no"])), "w", encoding="utf-8") as f:
                f.write(build_framework_chapter(ch, BY_ID))
            continue  # 框架章独立构建
        if ch.get("kind") == "jd":
            with open(os.path.join(BASE, chapter_path(ch["no"])), "w", encoding="utf-8") as f:
                f.write(build_jd_chapter(ch, BY_ID))
            continue  # 面经章独立构建
        with open(os.path.join(BASE, chapter_path(ch["no"])), "w", encoding="utf-8") as f:
            f.write(chapter_page(ch))
    with open(os.path.join(BASE, "cases", "case1-deepdive.html"), "w", encoding="utf-8") as f:
        f.write(build_dim_page(7, "民生保险知识库平台", "保险垂直场景", DIM1, DIM1_EXC,
                               "case-minsheng-insurance.html", "返回案例主页"))
    with open(os.path.join(BASE, "cases", "case2-deepdive.html"), "w", encoding="utf-8") as f:
        f.write(build_dim_page(8, "基金组合绩效评价（金融 DeepResearch）", "基金组合绩效评价", DIM2, DIM2_EXC,
                               "case-finance-deepresearch.html", "返回案例主页"))
    import billing_page
    with open(os.path.join(BASE, "cases", "case-billing-platform.html"), "w", encoding="utf-8") as f:
        f.write(billing_page.build())
    import edd_page
    with open(os.path.join(BASE, "edd-learning.html"), "w", encoding="utf-8") as f:
        f.write(edd_page.build())
    case_page_patch()
    print("v2 built:", len(PAPERS), "papers,", len(CHAPTERS), "chapters + portal + cheatsheet")


def build_dim_page(ch_no, case_title, chip_label, dims, exc, prev_href, prev_label):
    cards = "".join(dim_card(d, "深挖维度") for d in dims)
    exc_html = "".join(f'<div class="iv"><b>异常 case：{t}</b><br>{h}</div>' for t, h in exc)
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{case_title} · 深挖维度 - Agent 论文知识库</title><link rel="stylesheet" href="../assets/style.css"></head>
<body><div class="wrap">
<div class="crumbs"><a href="../index.html">首页</a> / <a href="{prev_href}">{case_title}</a> / 深挖维度</div>
<div class="catline"><span class="chip" style="background:#334155">第 {ch_no} 章 · 深挖 10 维</span></div>
<h1>{case_title}：10 个可以深挖的维度</h1>
<div class="box why"><b>怎么用：</b>面试官追问"再深入一点"时，每个维度都是一条完整的防线，按六步方法论展开——<b>① 问题定义</b>（把症状翻译成可度量的工程问题）→ <b>② 问题分析</b>（根因链 + 排除的假设与证据）→ <b>③ 问题场景</b>（具体现场与复现方式）→ <b>④ 方案对比</b>（三个候选的优劣与结论）→ <b>⑤ 采用与踩坑</b>（第一版怎么翻车、怎么改）→ <b>⑥ 验证与迭代</b>（指标、回归、后续演进）。红色"面试官深挖预演"是站在面试官视角的追问与亮点回答。黄色高亮为待填真实数据。</div>
{cards}
<h2>异常处理 Case 集（高频拷打）</h2>
{exc_html}
<div class="chapnav"><a class="pn" href="../cases/{prev_href}">← 返回案例主页</a><a class="pn" href="../cheatsheet.html">速查工具页 →</a></div>
<div class="foot">实战案例深挖 · Steven Li 面试准备知识库 · 黄色占位请替换真实数据</div>
</div></body></html>"""

if __name__ == "__main__":
    main()
