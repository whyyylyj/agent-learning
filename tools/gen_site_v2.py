# -*- coding: utf-8 -*-
"""Agent 论文知识库 v2：章节式多页站点（循序渐进）"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_papers import PAPERS, CATS, RESUME, BASE  # noqa
from figs import FIGS

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
         papers=["p17", "p18", "p20", "p19"],
         goal=["掌握 BFCL V3 四层工具评测（含 irrelevance 检测）", "能讲 MCP/A2A 的分工与企业级互操作架构", "了解 GUI agent 的交互边界"],
         resume="BFCL 的 irrelevance detection 与你的意图匹配/拒答是同一个问题；MCP 是你平台工具层的标准化出口。"),
    dict(no=7, slug="ch7", name="实战案例一：民生保险知识库平台", case="cases/case-minsheng-insurance.html",
         why="把前六章的范式/上下文/失败分析/评测全部落到保险垂直场景：三条链路、三层意图路由、规则引擎校验。"),
    dict(no=8, slug="ch8", name="实战案例二：金融 DeepResearch", case="cases/case-finance-deepresearch.html",
         why="把并行取数、证据治理、交叉校验组装成长程研究链路——RAG 2.0 的完整骨架，也是异步并发功底的迁移。"),
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
    rel=[("pre", "p01", "单 agent 与编排模式"), ("related", "p08", "先看失败分类再动手"), ("related", "p09", "框架工程化"), ("apply", "case2", "并行取数的拓扑来源")]),
"p08": dict(problem="多智能体系统经常不如单 agent，失败原因从未被体系化归因。",
    idea="对 LangGraph/AutoGen/CrewAI 真实 trace 实证标注：14 种失败模式、三大层级（规格/智能体间对齐/任务验证），失败大头在 agent 间对齐与验证缺失。",
    summary="给'要不要上多智能体'提供风险清单与排障检查单。",
    rel=[("pre", "p03", "多智能体实现"), ("related", "p02", "防护栏缓解"), ("related", "p09", "运行时缓解"), ("apply", "case1", "验证层实践")]),
"p09": dict(problem="主流 agent 框架黑盒程度高：失败难定位、状态难重放、并发难控。",
    idea="agent as actor + 显式异步消息：并发天然、失败可定位、可重放；配套 Studio 可视化。",
    summary="框架层面系统性回应 MAST 的失败模式。",
    rel=[("pre", "p08", "失败分析"), ("related", "p03", "编排形态对照"), ("apply", "case2", "并行取数运行时")]),
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
<div class="catline"><span class="chip" style="background:#334155">第 {no} 章 / 共 8 章</span></div>
<h1>{name}</h1>
<div class="box why"><b>本章定位（循序渐进）：</b>{why}</div>

<h2>本章论文（总分总速览，点击进入深度笔记）</h2>
{blocks}

{f'<h2>本章学习目标</h2><ul class="pts deep">{goals}</ul>' if goals else ''}
{f'<div class="box ideab"><b>与简历项目的关联：</b>{resume_line}</div>' if resume_line else ''}

<div class="chapnav">{pn}</div>
<div class="foot">Agent 论文知识库 · 第 {no} 章 / 共 8 章</div>
</div></body></html>"""

def case_page_patch():
    """给已生成的案例页加章节导航"""
    mapping = [
        ("cases/case-minsheng-insurance.html", 7, "第 7 章 · 实战案例一", "cases/case-finance-deepresearch.html", "下一章：金融 DeepResearch →"),
        ("cases/case-finance-deepresearch.html", 8, "第 8 章 · 实战案例二", "cases/case-minsheng-insurance.html", "← 上一章：民生保险知识库平台"),
    ]
    for rel, no, label, other, other_label in mapping:
        path = os.path.join(BASE, rel)
        html = open(path, encoding="utf-8").read()
        if "章节导航" not in html:
            html = html.replace('<a class="back" href="../index.html">← 返回总览</a>',
                f'<a class="back" href="../index.html">← 返回总览</a><div class="crumbs"><span class="chip" style="background:#334155">{label}</span></div>')
            html = html.replace('<div class="foot">',
                f'<div class="chapnav"><a class="pn" href="../index.html">目录</a><a class="pn" href="../{other}">{other_label}</a></div><div class="foot">', 1)
        open(path, "w", encoding="utf-8").write(html)

def portal():
    ch_cards = ""
    for ch in CHAPTERS:
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
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent 论文知识库 · Steven Li</title><link rel="stylesheet" href="assets/style.css"></head>
<body><div class="wrap">
<div class="hero">
<h1>Agent 论文知识库</h1>
<div class="sub">2025 – 2026.09 · 章节式 · 循序渐进 · 为 Steven Li（AI 应用技术负责人 / 软件架构师）定制</div>
<div class="stats">
<div><b>20</b><span>篇典型高引论文</span></div><div><b>8</b><span>章学习路径</span></div><div><b>2</b><span>个实战案例</span></div><div><b>8</b><span>类面试场景话术</span></div>
</div>
</div>

<div class="callout"><b>使用方法：</b>按第 1→6 章顺序精读（每章 30~60 分钟），第 7/8 章是两个实战案例（你的简历项目），面试前 30 分钟只看<a href="cheatsheet.html">速查工具页</a>。每篇论文都按「总分总」组织：解决什么问题 → 主旨与设计理念 → 分要点 → 一句话总结。</div>

<h2>学习路径 · 共 8 章</h2>
<p class="sub">顺序即依赖：范式 → 单智能体工程 → 多智能体 → 底座模型 → RL 与深度研究 → 评测与协议 → 两个实战案例收束。</p>
<div class="grid">{ch_cards}</div>

<h2>快速入口</h2>
<div class="grid">
<a class="card" href="cheatsheet.html"><div class="card-top"><span class="chip" style="background:#b91c1c">面试前 30 分钟</span></div><h3>速查工具页</h3><p>面试场景速查表（8 类话术）/ 论文总表 / 简历关联矩阵 / 延伸阅读。</p></a>
</div>

<div class="foot">数据来源：arXiv / 各公司官方博客（2025–2026.09 检索核实）· 引用数表述建议用量级 · Steven Li 面试准备知识库</div>
</div></body></html>"""

def cheatsheet():
    # 从旧 index 中提取场景速查表与总表逻辑（直接重建内容）
    scenario_rows = [
    ("RAG / 检索质量优化", "⑤上下文工程综述 ⑥Manus ⑮Tongyi DeepResearch", "检索只是上下文工程的“取”环节，我在分块/重排/摘要压缩三层都做过迭代（QA 90%+）；下一站是 long-horizon 检索（Tongyi 路线）。"),
    ("多轮对话 / Token 成本", "③多智能体复盘 ⑤Manus ⑦Mem0", "Anthropic：token 用量解释 80% 方差、多智能体 15× 成本；Manus：KV-cache 命中率优先；Mem0：抽取-更新记忆 p95 −91%。我做过摘要压缩，思路同源。"),
    ("工具调用 / 意图识别", "①Building Effective Agents ⑱BFCL V3 ⑲MCP/A2A", "我的意图识别 = Routing 模式 + BFCL 的 irrelevance detection；工具接入正走向 MCP 标准化。"),
    ("质量评估与回归", "④The Second Half ⑰BrowseComp ⑱BFCL V3", "下半场拼评测：我建了分类别黄金测试集 + 自动评估 + 显著性检验；评测集设计参考“难找易验”原则。"),
    ("要不要上多智能体", "③多智能体复盘 ⑧MAST ⑳MCP/A2A", "MAST：约四成失败在 agent 间对齐；Anthropic：15× token 买广度。我的场景串行度高故未上，但具备并行 subagent 的基础设施经验。"),
    ("模型选型与能力演进", "⑨R1 ⑩Qwen3 ⑪K2 ⑫GLM-4.5 ⑬LongCat", "两时代论：R1 前工程补能力（我做意图路由），R1 后模型原生会规划；选型看任务分布 + 部署约束（私有化→Qwen3/GLM，工具交互→K2）。"),
    ("高并发 / 性能 / 降本", "⑬LongCat-Flash ⑤Manus ⑥Mem0", "LongCat 零计算专家=算力按需分配，与我自研的动态负载自适应调度同构；加上 KV-cache 与记忆压缩，三层降本。"),
    ("学习能力 / 技术跟进", "④The Second Half ⑯Agentic RL 综述 ⑰UI-TARS", "用下半场论 + Agentic RL POMDP 框架展示体系化跟进；从 API agent 到 GUI agent 的交互边界扩展。"),
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

<h2>面试场景速查表（8 类话术）</h2>
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
    for p in PAPERS:
        with open(os.path.join(BASE, "papers", f"{p[1]}.html"), "w", encoding="utf-8") as f:
            f.write(detail_page(p))
    for ch in CHAPTERS:
        if "case" in ch:
            continue  # 案例页独立存在
        with open(os.path.join(BASE, chapter_path(ch["no"])), "w", encoding="utf-8") as f:
            f.write(chapter_page(ch))
    case_page_patch()
    print("v2 built:", len(PAPERS), "papers,", len(CHAPTERS), "chapters + portal + cheatsheet")

if __name__ == "__main__":
    main()
