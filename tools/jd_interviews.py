# -*- coding: utf-8 -*-
"""第 10 章 · 面经与 JD 分析：考察重点 · 短板 · 针对性准备"""
from figs import svg, R, T, badge, INK, SUB, BLUE

def build(ch, by_id):
    # 框架版图式 SVG：考察重点雷达/分布
    i = svg(740, 210, (
        T(370, 24, "大厂 AI Agent 岗考察重点分布（据面经归纳）", 13.5, INK, "middle", "600")
        + badge(40, 46, "项目深挖（决策理由）", "#1f4e79", 210)
        + badge(270, 46, "RAG 全链路", "#2563eb", 130)
        + badge(420, 46, "框架选型", "#059669", 110)
        + badge(560, 46, "工具调用/MCP", "#7c3aed", 140)
        + badge(40, 84, "Agent 设计（状态/循环）", "#d97706", 210)
        + badge(270, 84, "评测体系", "#dc2626", 110)
        + badge(400, 84, "高并发/服务端", "#0891b2", 150)
        + badge(570, 84, "多智能体", "#65a30d", 110)
        + badge(150, 122, "Transformer 八股", "#64748b", 160)
        + badge(330, 122, "RL/Post-Training", "#64748b", 160)
        + badge(510, 122, "多模态", "#64748b", 100)
        + T(370, 180, "面积越大考察越频；灰色为'非 agent 岗也会问'的工程与理论基本盘", 12, SUB, "middle")
    ))
    # 共性 JD 要求
    jd_rows = "".join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in [
        ("语言", "精通 Python（AI 岗默认）；Java/Go 至少一门（后端岗）"),
        ("大模型原理", "Transformer 架构、Post-Training、RL/多模态、部署流程"),
        ("Agent 能力", "任务规划、多步推理（CoT）、工具调用、框架与架构设计"),
        ("服务端基础", "数据库、消息队列、ES、缓存；亿级用户性能优化优先"),
        ("评测与数据", "评测体系、数据合成、badcase 归因（新趋势）"),
        ("标准化", "MCP / Coze / Dify 等平台与协议经验加分"),
    ])
    # 公司 cluster 分析
    clusters = [
    ("字节系（抖音 / 豆包 / 火山引擎）", "Agent 架构设计与效果优化、RL 与 Post-Training、Python/Go、服务端基础（MQ/ES/Ray）",
     "✅ 强项：Java 高并发功底（10× QPS）、RAG 全链路、意图路由、评测闭环", "⚠ Go 语言需补；训练侧（RL/Post-Training）无生产经验",
     "第 4 章底座模型 + 案例 DeepResearch 的成本工程；准备'从零设计对话 Agent（会话/任务/工具三状态）'场景题"),
    ("阿里系（千问 / 夸克 / 百炼）", "Agent 全栈、任务规划/多步推理（CoT）/工具调用、Coze 经验加分、亿级用户性能优化优先",
     "✅ 强项：RAG 平台 0→1、意图路由、Milvus 选型、性能优化（20s→100ms）", "⚠ 亿级 C 端用户经验弱；Qwen 生态细节",
     "第 1/2 章范式与上下文工程 + Qwen3 选型（第 4 章）；强调与开源模型生态的实操"),
    ("百度（千帆 / 文心）", "LLM 应用工程、基础算法与工程结合", "✅ 强项：RAG 工程、金融 16+ 机构交付", "⚠ 生态细节",
     "速查工具页八股 + 案例 1 的合规与权限治理"),
    ("腾讯（AI Agent 开发）", "从零设计对话 Agent：会话状态 / 任务状态 / 工具状态三状态管理",
     "✅ 强项：多轮对话状态管理实战、意图路由", "⚠ 对话平台通用设计题需演练",
     "案例 1 多轮对话 + 第 2 章上下文工程 + 第 3 章失败分析"),
    ("小红书", "偏算法研究：论文讲解、RAG 短板、DPO、多模态检索（CLIP）",
     "✅ 强项：RAG 工程与评测体系可讲深", "⚠ 训练细节（DPO/LoRA）与论文讲解需补",
     "第 5 章 RL 综述 + 论文精读（挑 1 篇练 20 分钟讲解，推荐 MAST 或 LongCat）"),
    ("微软", "AutoGen / Semantic Kernel 生态、系统设计、工程规范、英文",
     "✅ 强项：多智能体失败分析（MAST 理解深）、Java/Python 双栈", "⚠ 英文面试表达",
     "第 3 章 + 第 6 章协议；准备英文版项目 3 分钟介绍"),
    ("Shopee 虾皮", "Java 后端高并发、MySQL/缓存、AI 应用（客服/搜索）",
     "✅ 强项：Java 高并发 + RAG 双修，匹配度最高", "⚠ 东南亚业务语境",
     "R2 轮询框架 + R3 性能优化为主叙事；案例 1 补 AI 差异点"),
    ("NVIDIA（NIM / 推理）", "推理性能优化、RAG 部署、底层系统", "✅ 强项：性能优化与序列化（Fury）叙事契合",
     "⚠ CUDA/算子层经验缺失", "R3 性能优化 + R4 Fury + 第 4 章 serving 成本；诚实说明 CUDA 边界"),
    ("宇树科技（具身智能）", "机器人 RL、实时控制、嵌入式", "✅ 可迁移：高可靠系统的性能与稳定性思维",
     "⚠ 具身智能/机器人 RL 无经验（关联最弱）", "诚实定位：后端/仿真数据管线方向；补具身智能通识即可"),
    ("OpenAI / Anthropic", "Applied AI：agent 设计哲学、评测驱动、系统与提示工程、英文沟通",
     "✅ 强项：评测驱动开发、上下文工程、agent 失败分析的实战叙事", "⚠ 英文工作语言；开源贡献活跃度",
     "第 1 章范式 + 第 2 章上下文 + 案例双案例；英文简历与 3 分钟英文项目介绍"),
    ]
    crows = ""
    for name, jd, strong, weak, prep in clusters:
        crows += (f'<tr><td><b>{name}</b></td><td>{jd}</td>'
                  f'<td style="color:#047857">{strong}</td><td style="color:#92400e">{weak}</td><td>{prep}</td></tr>')
    sources = "".join(f'<li><a href="{u}" target="_blank">{t}</a></li>' for t, u in [
        ("字节跳动招聘官网：大模型应用后端工程师（Agent 方向）", "https://jobs.bytedance.com/experienced/position/7536149766817138951/detail"),
        ("阿里云：AI Agent 全栈开发工程师", "https://careers.aliyun.com/off-campus/position-detail?positionId=100015503004"),
        ("牛客：AI Agent 面试高频 100 问", "https://www.nowcoder.com/discuss/922460251717128192"),
        ("腾讯 AI Agent 一面面经（三状态设计）", "https://www.nowcoder.com/discuss/873917052023492608"),
        ("字节飞连二面真题与解答（腾讯云社区）", "https://developer.cloud.tencent.com/article/2673729"),
        ("65 题 AI Agent 全栈面试宝典（阿里云社区）", "https://developer.aliyun.com/article/1739618"),
        ("AgentGuide：大厂面经整合（GitHub）", "https://github.com/adongwanai/AgentGuide"),
        ("nageoffer：Agent/RAG/MCP Top50 题库", "https://nageoffer.com/ai/interview/home/"),
        ("JavaGuide：AI 应用开发知识体系", "https://javaguide.cn/ai/"),
        ("小林面试笔记：Agent 框架选型高频题", "https://xiaolinnote.com/ai/langchain/agent_frameworks.html"),
    ])
    gaps = "".join(f'<li><b>{t}</b> — {d}</li>' for t, d in [
        ("训练侧细节（RLHF/DPO/LoRA）", "无生产经验。补法：理论梳理 + 开源小模型跑一次 LoRA 微调 demo，话术定界'工程侧理解训练，用于选型与协作，不做训练本身'。"),
        ("多模态（CLIP/VLM）", "无。补法：概念 + 多模态检索面经题（图文混检）准备一轮即可，不深追。"),
        ("Transformer 八股细节", "注意力公式/位置编码/归因需要手推。补法：按 JavaGuide AI 篇过一遍，面试前一晚复习。"),
        ("英文面试", "OpenAI/Anthropic/微软/NVIDIA 需要。补法：英文简历已完成；练 3 分钟英文项目介绍 + 20 个高频问答英文版。"),
        ("Go 语言", "字节后端岗常见。补法：强调 Java/Python 深度 + 语言迁移案例（PHP→Java 的重构经历证明迁移能力）。"),
        ("亿级 C 端用户经验", "阿里系 JD 提及。补法：用 50W+ 用户 + 16+ 机构多租户的复杂度叙事对冲（多租户隔离与权限复杂度不低于 C 端规模）。"),
    ])
    map_rows = ""
    for name, chs in [
        ("字节系 / 豆包 / 抖音", "第 3 章失败分析 · 第 4 章底座 · 案例 2 成本工程 · 八股 Top10"),
        ("阿里系 / 千问 / 夸克", "第 1 章范式 · 第 2 章上下文 · Qwen3 选型 · 案例 1 意图路由"),
        ("腾讯", "案例 1 多轮对话 · 第 2 章 · 三状态设计场景题演练"),
        ("小红书", "第 5 章RL 综述 · MAST 精读 · 第 6 章评测"),
        ("微软", "第 3 章 AgentScope/AutoGen · 第 6 章 MCP/A2A · 英文项目介绍"),
        ("Shopee 虾皮", "R2 轮询框架 · R3 性能优化 · 案例 1 AI 差异点"),
        ("NVIDIA", "R3/R4 性能与序列化 · 第 4 章 serving 成本"),
        ("OpenAI / Anthropic", "第 1 章范式 · 评测驱动叙事 · 两个案例的合规与治理"),
    ]:
        map_rows += f'<tr><td><b>{name}</b></td><td>{chs}</td></tr>'
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>第 10 章 面经与 JD 分析 - Agent 论文知识库</title><link rel="stylesheet" href="../assets/style.css"><style>
table.sel{{width:100%;border-collapse:collapse;background:#fff;font-size:13px;margin:10px 0}}
table.sel th{{background:#1f4e79;color:#fff;padding:7px 10px;text-align:left}}
table.sel td{{padding:7px 10px;border-bottom:1px solid #e5e7eb;vertical-align:top}}
</style></head>
<body><div class="wrap">
<div class="crumbs"><a href="../index.html">首页</a> / 第 10 章</div>
<div class="catline"><span class="chip" style="background:#334155">第 10 章 / 共 10 章</span></div>
<h1>{ch["name"]}</h1>
<div class="box why"><b>本章定位：</b>{ch["why"]}</div>

<h2>一图看懂 · 考察重点分布</h2>
<div class="figcard">{i}</div>

<h2>JD 共性要求（字节 / 阿里公开招聘信息归纳）</h2>
<table class="sel"><tr><th style="width:130px">维度</th><th>典型要求</th></tr>{jd_rows}</table>
<p class="case-src">来源：<a target="_blank" href="https://jobs.bytedance.com/experienced/position/7536149766817138951/detail">字节·巨量星图 Agent 后端</a> · <a target="_blank" href="https://careers.aliyun.com/off-campus/position-detail?positionId=100015503004">阿里云 AI Agent 全栈</a> 等（见文末）</p>

<h2>分公司考察分析与匹配度</h2>
<table class="sel"><tr><th style="width:150px">公司</th><th style="width:24%">考察重点（JD+面经）</th><th style="width:22%">匹配强项 ✅</th><th style="width:20%">短板 ⚠</th><th>针对性准备</th></tr>{crows}</table>

<h2>面经考点归纳（高频主题）</h2>
<ul class="pts">
<li>框架选型与状态机设计：LangGraph 为什么用图、会话/任务/工具三状态管理（腾讯一面真题）</li>
<li>RAG 全链路：切分、多路召回、rerank、评测、幻觉治理</li>
<li>Agent 设计：ReAct/CoT/ToT、工具调用与 MCP、死循环防护</li>
<li>项目深挖：技术决策的理由与取舍（"你做过吗"类追问必须能落地）</li>
<li>工程基本盘：Transformer 八股、Redis/缓存、系统设计</li>
</ul>

<h2>短板分析与补齐计划（基于简历的诚实自评）</h2>
<ul class="pts">{gaps}</ul>

<h2>公司 × 知识库针对性扩展映射</h2>
<table class="sel"><tr><th style="width:200px">目标公司</th><th>优先准备的章节 / 案例 / 话术</th></tr>{map_rows}</table>

<h2>面经与 JD 来源</h2>
<ul class="case-src">{sources}</ul>

<div class="chapnav"><a class="pn" href="ch9.html">← 第 9 章：典型 Agent 开源框架</a><a class="pn" href="../cheatsheet.html">速查工具页 →</a></div>
<div class="foot">Agent 论文知识库 · 第 10 章 / 共 10 章 · JD 与面经为 2025–2026.09 公开信息归纳</div>
</div></body></html>"""

def md2(s): return s
