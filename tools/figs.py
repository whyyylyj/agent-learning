# -*- coding: utf-8 -*-
"""20 张论文核心机制图（inline SVG，一图看懂）"""

INK = "#1f2937"; SUB = "#64748b"; BLUE = "#2563eb"; GREEN = "#059669"
AMBER = "#d97706"; RED = "#dc2626"; PURPLE = "#7c3aed"; GRAY = "#64748b"

def svg(w, h, inner):
    return (f'<svg viewBox="0 0 {w} {h}" style="width:100%;height:auto;font-family:inherit" '
            f'xmlns="http://www.w3.org/2000/svg">{inner}</svg>')

def R(x, y, w, h, fill, stroke, rx=9, sw=1.6, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'

def T(x, y, t, size=12.5, fill=INK, anchor="middle", w="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'font-weight="{w}">{t}</text>')

def AR(x1, y1, x2, y2, color="#94a3b8", sw=1.8):
    import math
    ang = math.atan2(y2 - y1, x2 - x1); L = 8
    xa = x2 - L * math.cos(ang - 0.42); ya = y2 - L * math.sin(ang - 0.42)
    xb = x2 - L * math.cos(ang + 0.42); yb = y2 - L * math.sin(ang + 0.42)
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"/>'
            f'<polygon points="{x2},{y2} {xa},{ya} {xb},{yb}" fill="{color}"/>')

def badge(x, y, t, color, w=None):
    w = w or (len(t) * 12 + 26)
    return (R(x, y, w, 26, color, color, rx=13) +
            T(x + w / 2, y + 17.5, t, 12, "#ffffff", "middle", "600"))

def FIG_p01():
    i = R(300, 16, 140, 34, "#eef2ff", BLUE) + T(370, 38, "拿到一个任务", 13)
    i += AR(370, 50, 370, 74)
    i += R(255, 76, 230, 40, "#fffbeb", AMBER) + T(370, 101, "步骤能否预先穷举？", 13, AMBER, "middle", "600")
    i += AR(280, 116, 190, 152, GREEN) + T(205, 140, "能 → Workflow", 12, GREEN)
    i += AR(460, 116, 550, 152, RED) + T(535, 140, "不能 → Agent", 12, RED)
    i += R(40, 154, 300, 96, "#ecfdf5", GREEN)
    i += T(190, 176, "五种可组合模式", 12.5, GREEN, "middle", "600")
    chips = ["链式", "路由", "并行", "编排者", "评审循环"]
    for k, cname in enumerate(chips):
        cx = 58 + (k % 3) * 96; cy = 188 + (k // 3) * 30
        i += R(cx, cy, 86, 24, "#ffffff", GREEN, rx=12) + T(cx + 43, cy + 16.5, cname, 11.5)
    i += R(400, 154, 300, 96, "#fef2f2", RED)
    i += T(550, 180, "Agent：LLM + 工具 循环", 12.5, RED, "middle", "600")
    i += T(550, 202, "自己决定下一步，直到完成", 11.5, SUB)
    i += T(550, 222, "过程开放 · 需强验证", 11.5, SUB)
    i += T(370, 276, "复杂度开关只有一个：ACI（工具接口）质量", 12.5, INK, "middle", "600")
    return svg(740, 292, i)

def FIG_p02():
    i = T(128, 24, "Agent = 三要素", 13, INK, "start", "600")
    i += R(20, 78, 460, 54, "#f8fafc", "#cbd5e1")
    i += T(80, 100, "Model", 13, BLUE, "middle", "600") + T(80, 118, "决策大脑", 11, SUB)
    i += T(240, 100, "Tools", 13, GREEN, "middle", "600") + T(240, 118, "能力边界", 11, SUB)
    i += T(400, 100, "Instructions", 13, AMBER, "middle", "600") + T(400, 118, "行为纪律", 11, SUB)
    i += AR(490, 105, 520, 105)
    i += T(560, 24, "编排拓扑（复杂度从上到下）", 13, INK, "start", "600")
    for k, (t, c) in enumerate([("Single 单智能体", BLUE), ("Manager 管理者", AMBER), ("Decentralized 去中心", RED)]):
        y = 40 + k * 44
        i += R(540, y, 180, 34, "#fff", c) + T(630, y + 21.5, t, 12)
        if k < 2: i += AR(630, y + 34, 630, y + 44, "#cbd5e1")
    i += R(20, 158, 700, 56, "#fffbeb", AMBER)
    i += T(370, 178, "Guardrails 防护栏分层（每层独立开关）", 12.5, "#92400e", "middle", "600")
    for k, t in enumerate(["输入过滤", "工具权限", "事实校验", "人工升级"]):
        x = 60 + k * 168
        i += R(x, 188, 150, 20, "#fff", AMBER, rx=10) + T(x + 75, 202, t, 11.5, "#92400e")
    i += T(370, 244, "先单智能体跑通 → 再考虑编排升级；规则能解决的不用 agent", 12.5, SUB)
    return svg(740, 258, i)

def FIG_p03():
    i = R(24, 96, 170, 64, "#eff6ff", BLUE)
    i += T(109, 122, "LeadAgent", 13, BLUE, "middle", "600")
    i += T(109, 141, "拆解 · 分派 · 汇总", 11, SUB)
    for k in range(3):
        y = 28 + k * 84
        i += AR(194, 128, 268, y + 32, BLUE)
        i += R(270, y, 220, 64, "#fff", GREEN)
        i += T(380, y + 26, f"Subagent {k+1}", 12.5, GREEN, "middle", "600")
        i += T(380, y + 46, "独立上下文 · 独立工具", 11, SUB)
        i += AR(490, y + 32, 560, 128, GREEN)
    i += R(562, 96, 156, 64, "#f0fdf4", "#059669")
    i += T(640, 122, "汇总", 13, GREEN, "middle", "600")
    i += T(640, 141, "带引用的报告", 11, SUB)
    i += badge(250, 218, "研究广度任务 +90.2%", GREEN, 190)
    i += badge(460, 218, "token ≈ 15× 聊天", RED, 165)
    i += badge(240, 252, "token 用量解释 80% 性能方差", AMBER, 250)
    i += T(370, 300, "适用：广度优先、可并行的任务；串行依赖任务可能负收益", 12, SUB)
    return svg(740, 312, i)

def FIG_p04():
    i = R(20, 40, 330, 130, "#f1f5f9", "#94a3b8")
    i += T(185, 68, "上半场 · 预训练时代", 14, INK, "middle", "600")
    for k, t in enumerate(["问题是固定的（benchmark 已定）", "拼方法：更大的模型", "评测是静态的附属品"]):
        i += T(185, 96 + k * 24, t, 12, SUB)
    i += R(390, 40, 330, 130, "#eff6ff", BLUE)
    i += T(555, 68, "下半场 · 现在", 14, BLUE, "middle", "600")
    for k, t in enumerate(["定义问题：把需求变成规格", "构造真实环境 + RL", "可靠度量成为稀缺能力"]):
        i += T(555, 96 + k * 24, t, 12, "#1e40af")
    i += AR(352, 105, 386, 105)
    i += T(370, 205, "模型能力趋同之后，价值转向：会问什么问题、能造什么环境、能不能度量", 13, INK, "middle", "600")
    i += T(370, 228, "agent 是下半场的载体；评测与产品化 = 工程师的核心竞争力", 12, SUB)
    return svg(740, 244, i)

def FIG_p05():
    i = R(60, 34, 620, 44, "#eff6ff", BLUE)
    i += T(370, 61, "上下文（只追加 · append-only）", 12.5, BLUE, "middle", "600")
    segs = [("系统提示（稳定前缀）", 150), ("历史轨迹", 150), ("todo.md 复述", 130), ("文件句柄", 100)]
    x = 70
    for t, w in segs:
        i += R(x, 40, w - 6, 32, "#fff", "#93c5fd", rx=6) + T(x + (w - 6) / 2, 60, t, 10.5, "#1e40af")
        x += w
    i += badge(60, 8, "KV-cache 命中率 = 第一产品指标", BLUE, 240)
    six = ["prompt 前缀稳定", "只追加不修改", "mask 而非删工具", "文件系统当上下文", "todo 反复复述", "保留过去错误"]
    for k, t in enumerate(six):
        x = 40 + (k % 3) * 232; y = 118 + (k // 3) * 56
        i += R(x, y, 210, 40, "#fff", "#cbd5e1") + T(x + 105, y + 25, t, 12.5)
    i += T(370, 240, "六条实践共同服务一个目标：让模型在长任务里不丢目标、不丢缓存、不被误导", 12, SUB)
    return svg(740, 256, i)

def FIG_p06():
    i = T(370, 26, "上下文工程 = 系统化地组装：正确的信息 + 工具 + 格式", 13, INK, "middle", "600")
    steps = [("原始信息", "#f1f5f9", "#94a3b8"), ("取 · 检索", "#eff6ff", BLUE), ("选 · 过滤", "#fef3c7", AMBER),
             ("压 · 摘要", "#f5f3ff", PURPLE), ("组 · 格式", "#ecfdf5", GREEN), ("LLM", "#1f4e79", "#1f4e79")]
    x = 30
    for k, (t, f, c) in enumerate(steps):
        i += R(x, 56, 96, 44, f, c)
        i += T(x + 48, 83, t, 12.5, "#111827" if t == "LLM" else c, "middle", "600")
        if k < 5: i += AR(x + 96, 78, x + 112, 78)
        x += 112
    i += T(370, 150, "三条支撑轨道", 12.5, INK, "middle", "600")
    for k, t in enumerate(["记忆：短期摘要 + 长期记忆库", "工具：统一接口（MCP 方向）", "格式：结构化 / 引用溯源"]):
        i += R(70 + k * 210, 166, 190, 36, "#fff", "#cbd5e1") + T(165 + k * 210, 189, t, 11)
    i += T(370, 238, "你做的分块、混合检索、rerank 截断、摘要压缩——都能放进这张图", 12, SUB)
    return svg(740, 252, i)

def FIG_p07():
    i = R(20, 70, 120, 44, "#f1f5f9", "#94a3b8") + T(80, 96, "对话流", 12.5)
    i += AR(140, 92, 172, 92)
    i += R(174, 70, 110, 44, "#eff6ff", BLUE) + T(229, 96, "抽取 LLM", 12.5, BLUE)
    i += AR(284, 92, 316, 92)
    i += R(318, 70, 150, 44, "#fffbeb", AMBER)
    i += T(393, 90, "更新决策", 12.5, AMBER, "middle", "600")
    for k, t in enumerate(["ADD", "UPDATE", "DELETE", "NOOP"]):
        i += T(328 + k * 38, 106, t, 9.5, SUB)
    i += AR(468, 92, 500, 92)
    i += R(502, 70, 110, 44, "#ecfdf5", GREEN) + T(557, 96, "记忆库", 12.5, GREEN)
    i += AR(612, 92, 644, 92)
    i += R(646, 70, 76, 44, "#f5f3ff", PURPLE) + T(684, 96, "召回", 12.5, PURPLE)
    i += T(370, 34, "两阶段记忆管线：不是把历史全塞进上下文，而是增量维护一个记忆库", 13, INK, "middle", "600")
    i += badge(150, 158, "准确率 +26%（vs OpenAI 记忆）", GREEN, 260)
    i += badge(430, 158, "p95 延迟 −91%（vs 全量上下文）", BLUE, 260)
    i += T(370, 216, "双层记忆：对话级（本话题）+ 用户级（跨会话偏好与事实）", 12, SUB)
    return svg(740, 232, i)

def FIG_p08():
    i = T(370, 26, "MAST：多智能体失败三大层级（14 种失败模式）", 13.5, INK, "middle", "600")
    bands = [
        ("① 规格与系统问题", "目标不清 · 角色重叠 · 任务说明书缺失", "#fef2f2", RED),
        ("② 智能体间对齐失败（占比最高）", "信息传递丢失 · 互相抬杠 · 重复工作", "#fffbeb", AMBER),
        ("③ 任务验证失败", "没有验证步骤 · 过早停止 · 错误未被发现", "#eff6ff", BLUE),
    ]
    for k, (t, d, f, c) in enumerate(bands):
        y = 48 + k * 62
        i += R(60, y, 480, 50, f, c)
        i += T(80, y + 22, t, 13, c, "start", "600")
        i += T(80, y + 41, d, 11.5, SUB, "start")
    i += R(570, 48, 150, 162, "#f8fafc", "#cbd5e1")
    i += T(645, 76, "标注来源", 12, SUB, "middle", "600")
    for k, t in enumerate(["LangGraph", "AutoGen", "CrewAI", "真实 trace"]):
        i += T(645, 104 + k * 26, t, 12, INK)
    i += T(370, 242, "用法：给'要不要上多智能体'建立风险清单——失败大头不在模型，在协同与验证", 12.5, INK, "middle", "600")
    return svg(740, 258, i)

def FIG_p09():
    i = R(14, 22, 712, 150, "#fff", "#cbd5e1", rx=12, dash="7 5")
    i += T(370, 44, "Runtime（并发 · tracing · 失败重放）", 12, SUB, "middle", "600")
    for k, t in enumerate(["Agent A", "Agent B", "Agent C"]):
        x = 90 + k * 220
        i += R(x, 66, 150, 52, "#eff6ff", BLUE)
        i += T(x + 75, 88, t, 13, BLUE, "middle", "600")
        i += T(x + 75, 106, "独立上下文", 10.5, SUB)
    i += AR(240, 92, 310, 92, AMBER) + T(275, 84, "msg", 11, AMBER)
    i += AR(310, 112, 240, 112, AMBER) + T(275, 130, "msg", 11, AMBER)
    i += AR(460, 92, 530, 92, AMBER) + T(495, 84, "msg", 11, AMBER)
    i += AR(530, 112, 460, 112, AMBER) + T(495, 130, "msg", 11, AMBER)
    i += T(370, 206, "Agent = Actor：显式消息通信 → 并行天然、失败可定位、过程可重放", 12.5, INK, "middle", "600")
    i += T(370, 228, "对 MAST 失败分类的工程回应：消息级 tracing + 重放 = 排障框架", 12, SUB)
    return svg(740, 244, i)

def FIG_p10():
    i = R(30, 40, 150, 52, "#f1f5f9", "#94a3b8") + T(105, 70, "Base 模型", 13)
    i += AR(180, 66, 220, 66, GREEN)
    i += R(222, 34, 200, 64, "#ecfdf5", GREEN)
    i += T(322, 58, "GRPO 强化学习", 13, GREEN, "middle", "600")
    i += T(322, 78, "准确奖励 + 格式奖励", 11, SUB)
    i += T(322, 92, "无人工标注思维链", 11, SUB)
    i += AR(422, 66, 462, 66, GREEN)
    i += R(464, 34, 254, 64, "#fff", GREEN)
    i += T(590, 56, "推理行为自发涌现", 12.5, GREEN, "middle", "600")
    i += T(590, 76, "反思 · 自验证 · 'aha moment'", 11.5, SUB)
    i += AR(590, 98, 590, 120, "#94a3b8")
    i += R(464, 122, 254, 44, "#fff", "#94a3b8")
    i += T(590, 148, "蒸馏 → 1.5B~70B 小模型也能推理", 11.5)
    i += T(370, 206, "意义：开源模型第一次'学会思考'——工程上很多确定流程开始可以被模型原生规划替代", 12, SUB)
    return svg(740, 222, i)

def FIG_p11():
    i = R(310, 20, 120, 36, "#f1f5f9", "#94a3b8") + T(370, 43, "用户问题", 12.5)
    i += AR(370, 56, 370, 74)
    i += R(270, 76, 200, 40, "#fffbeb", AMBER) + T(370, 101, "模式开关", 12.5, AMBER, "middle", "600")
    i += AR(300, 116, 200, 140, BLUE)
    i += AR(440, 116, 540, 140, GREEN)
    i += R(60, 142, 260, 56, "#eff6ff", BLUE)
    i += T(190, 166, "Thinking 深度思考", 12.5, BLUE, "middle", "600")
    i += T(190, 186, "复杂分析 · 生成完整推理过程", 11, SUB)
    i += R(430, 142, 260, 56, "#ecfdf5", GREEN)
    i += T(560, 166, "Non-thinking 秒回", 12.5, GREEN, "middle", "600")
    i += T(560, 186, "简单咨询 · 省成本", 11, SUB)
    i += R(60, 216, 680, 30, "#f1f5f9", "#cbd5e1")
    i += T(370, 236, "家族谱：0.6B · 1.7B · 4B · 8B · 14B · 32B · 30B-A3B · 235B-A22B（全开源 Apache 2.0）", 11.5)
    return svg(740, 262, i)

def FIG_p12():
    i = T(370, 26, "K2 训练管线：为 agentic 而生", 13.5, INK, "middle", "600")
    steps = [("工具轨迹合成", "数千工具 · 造出稀缺数据"), ("继续预训练", "agentic 语料配比"),
             ("Self-critique RL", "模型自评 + rubric 准则奖励"), ("通用可验证 RL", "真实任务结果奖励")]
    x = 24
    for k, (t, d) in enumerate(steps):
        i += R(x, 52, 158, 64, "#eff6ff" if k % 2 == 0 else "#fffbeb", BLUE if k % 2 == 0 else AMBER)
        i += T(x + 79, 78, t, 12, BLUE if k % 2 == 0 else AMBER, "middle", "600")
        for j, dd in enumerate(d.split(" · ")):
            i += T(x + 79, 96 + j * 13, dd, 10, SUB)
        if k < 3: i += AR(x + 158, 84, x + 178, 84)
        x += 178
    i += badge(240, 150, "K2：1T 总参 / 32B 激活（MoE）", PURPLE, 250)
    i += badge(330, 184, "τ²-bench 工具交互：开源第一", GREEN, 240)
    i += T(370, 226, "洞察：工具调用数据可以合成、agent 行为可以 RL——'会用工具'是训练出来的", 12, SUB)
    return svg(740, 242, i)

def FIG_p13():
    i = ""
    boxes = [("Agentic 智能体", "工具使用 · 浏览器 · 函数调用", "#eff6ff", BLUE),
             ("Reasoning 推理", "长链思考 · 数学 · 代码", "#fef3c7", AMBER),
             ("Coding 编码", "真实仓库 · 端到端修复", "#ecfdf5", GREEN)]
    for k, (t, d, f, c) in enumerate(boxes):
        x = 30 + k * 240
        i += R(x, 46, 220, 64, f, c)
        i += T(x + 110, 72, t, 13, c, "middle", "600")
        i += T(x + 110, 94, d, 10.5, SUB)
    i += AR(140, 114, 300, 158, "#94a3b8")
    i += AR(370, 114, 370, 158, "#94a3b8")
    i += AR(600, 114, 440, 158, "#94a3b8")
    i += R(240, 160, 260, 46, "#1f4e79", "#1f4e79", rx=10)
    i += T(370, 189, "ARC 统一训练", 13.5, "#ffffff", "middle", "700")
    i += T(370, 232, "ARC 三能力联合 + hybrid reasoning → 综合第 3 / agent 基准第 2（官方口径，发布时点）", 12, SUB)
    i += R(580, 200, 140, 92, "#f8fafc", "#cbd5e1")
    i += T(650, 226, "355B-A32B", 12, INK, "middle", "600")
    i += T(650, 246, "MoE", 10.5, SUB)
    i += T(650, 264, "slime RL 基建", 10.5, SUB)
    i += T(650, 282, "MIT 开源", 10.5, SUB)
    return svg(740, 300, i)

def FIG_p14():
    i = T(370, 26, "零计算专家：算力按 token 难度自适应分配", 13.5, INK, "middle", "600")
    i += R(60, 56, 150, 48, "#f1f5f9", "#94a3b8") + T(135, 84, "输入 token", 12.5)
    i += AR(210, 80, 260, 80, AMBER)
    i += R(262, 56, 190, 48, "#fffbeb", AMBER)
    i += T(357, 76, "零计算专家", 13, AMBER, "middle", "600")
    i += T(357, 95, "这个 token 难不难？", 11, SUB)
    i += AR(452, 68, 502, 58, GREEN)
    i += AR(452, 92, 502, 104, RED)
    i += R(504, 36, 216, 44, "#ecfdf5", GREEN)
    i += T(612, 54, "简单 token → 少激活", 12, GREEN, "middle", "600")
    i += T(612, 72, "快 · 省", 11, SUB)
    i += R(504, 100, 216, 44, "#fef2f2", RED)
    i += T(612, 118, "复杂 token → 多激活", 12, RED, "middle", "600")
    i += T(612, 136, "强 · 准", 11, SUB)
    i += badge(150, 170, "560B 总参", BLUE, 120)
    i += badge(290, 170, "仅 27~31B 激活", GREEN, 150)
    i += badge(460, 170, "ScMoE：吞吐 ≈ ×2", PURPLE, 180)
    i += badge(210, 206, "τ-bench（agentic 基准）对标闭源前沿", AMBER, 320)
    i += T(370, 246, "与你自研的'动态负载自适应调度'同构：调度对象从请求变成 token", 12.5, INK, "middle", "600")
    return svg(740, 262, i)

def FIG_p15():
    i = T(370, 26, "Tongyi DeepResearch 训练配方", 13.5, INK, "middle", "600")
    i += R(40, 52, 200, 60, "#f1f5f9", "#94a3b8")
    i += T(140, 76, "底座", 12, SUB, "middle", "600")
    i += T(140, 96, "Qwen3-30.5B-A3B", 12, INK, "middle", "600")
    i += AR(240, 82, 272, 82)
    i += R(274, 52, 200, 60, "#fffbeb", AMBER)
    i += T(374, 76, "大规模合成数据", 12, AMBER, "middle", "600")
    i += T(374, 96, "多源多任务轨迹", 11, SUB)
    i += AR(474, 82, 506, 82)
    i += R(508, 52, 200, 60, "#eff6ff", BLUE)
    i += T(608, 76, "Agentic RL", 12, BLUE, "middle", "600")
    i += T(608, 96, "检索 · 浏览 · 代码环境", 11, SUB)
    i += AR(608, 112, 608, 138, "#94a3b8")
    i += R(430, 140, 278, 44, "#ecfdf5", GREEN)
    i += T(569, 158, "DeepResearch 基准开源第一梯队", 12, GREEN, "middle", "600")
    i += T(569, 176, "HLE · BrowseComp · GAIA · WebWalker", 10.5, SUB)
    i += R(40, 140, 330, 44, "#f5f3ff", PURPLE)
    i += T(205, 158, "30.5B 总参 / 3.3B 激活", 12.5, PURPLE, "middle", "600")
    i += T(205, 176, "'小激活参数也能干研究活'", 11, SUB)
    i += T(370, 226, "对你是演化路线图：单轮 RAG（已具备）→ 多轮检索 → 长程研究（本章方向）", 12, SUB)
    return svg(740, 242, i)

def FIG_p16():
    i = f'<circle cx="370" cy="105" r="62" fill="#eff6ff" stroke="{BLUE}" stroke-width="2"/>'
    i += T(370, 100, "Agent = POMDP", 13, BLUE, "middle", "700")
    i += T(370, 120, "部分可观测 · 多步决策", 10.5, SUB)
    six = [("环境构建", "#2563eb"), ("奖励设计", "#dc2626"), ("策略优化", "#059669"),
           ("训练范式", "#d97706"), ("评测体系", "#7c3aed"), ("工具·记忆·多智能体", "#0891b2")]
    for k, (t, c) in enumerate(six):
        x = 60 + (k % 3) * 232; y = 30 + (k // 3) * 60
        i += R(x, y, 210, 40, "#fff", c) + T(x + 105, y + 25, t, 12.5, c, "middle", "600")
    i += T(370, 210, "奖励设计是灵魂：先可验证（对/错），再 rubric（质量准则），必要时过程奖励", 12, SUB)
    i += T(370, 234, "用法：把你的系统翻译成这套语言——观测 = query + 检索结果，动作 = 路由/改写/拒答，奖励 = QA 正确率", 12, SUB)
    return svg(740, 250, i)

def FIG_p17():
    i = R(70, 46, 170, 52, "#eff6ff", BLUE) + T(155, 68, "感知：屏幕截图", 12.5, BLUE, "middle", "600") + T(155, 87, "不依赖 HTML/DOM", 10.5, SUB)
    i += AR(240, 72, 288, 72)
    i += R(290, 46, 170, 52, "#f5f3ff", PURPLE) + T(375, 68, "推理：规划 + 反思", 12.5, PURPLE, "middle", "600") + T(375, 87, "错误恢复训练", 10.5, SUB)
    i += AR(460, 72, 508, 72)
    i += R(510, 46, 170, 52, "#ecfdf5", GREEN) + T(595, 68, "动作：键鼠统一", 12.5, GREEN, "middle", "600") + T(595, 87, "跨 Web/桌面/移动", 10.5, SUB)
    i += AR(595, 98, 595, 128, "#94a3b8") + T(640, 118, "屏幕变化", 11, SUB)
    i += AR(595, 132, 595, 152, "#94a3b8")
    i += AR(510, 160, 250, 132, "#94a3b8")
    i += R(40, 190, 700, 34, "#f8fafc", "#cbd5e1")
    i += T(370, 212, "适用边界：没有 API 的老系统、跨平台 GUI 自动化；有 API 时仍优先结构化调用", 12, SUB)
    return svg(740, 240, i)

def FIG_p18():
    i = R(50, 50, 280, 90, "#fef2f2", RED)
    i += T(190, 78, "难找", 14, RED, "middle", "600")
    for k, t in enumerate(["多跳推理", "藏在网页深处", "需交叉验证多个来源"]):
        i += T(190, 102 + k * 18, t, 11.5, SUB)
    i += T(355, 100, "+", 24, INK, "middle", "600")
    i += R(400, 50, 280, 90, "#ecfdf5", GREEN)
    i += T(540, 78, "易验", 14, GREEN, "middle", "600")
    for k, t in enumerate(["答案短小", "事实明确", "可程序化核对"]):
        i += T(540, 102 + k * 18, t, 11.5, SUB)
    i += AR(370, 160, 370, 186, BLUE)
    i += badge(210, 196, "1266 道题：推理模型直接答崩", BLUE, 270)
    i += badge(500, 196, "deep research 系统显著领先", GREEN, 250)
    i += T(370, 246, "迁移价值：你的评测集也可以按'难找易验'设计——多跳题 + 客观核对", 12.5, INK, "middle", "600")
    return svg(740, 262, i)

def FIG_p19():
    i = T(370, 26, "BFCL V3：工具调用能力的四层评测阶梯", 13.5, INK, "middle", "600")
    layers = [
        ("单轮 AST 匹配", "参数结构对不对", "#f1f5f9", "#64748b"),
        ("实际执行", "跑得通、结果对", "#eff6ff", BLUE),
        ("多轮状态性", "跨轮上下文与执行状态保持", "#fffbeb", AMBER),
        ("irrelevance 检测", "不相关请求敢拒绝（= 意图识别/拒答）", "#ecfdf5", GREEN),
    ]
    for k, (t, d, f, c) in enumerate(layers):
        y = 48 + k * 58
        w = 320 + k * 90
        x = 370 - w / 2
        i += R(x, y, w, 46, f, c)
        i += T(x + 18, y + 21, f"L{k+1} · {t}", 12.5, c, "start", "600")
        i += T(x + 18, y + 38, d, 11, SUB, "start")
    i += T(370, 300, "覆盖上千真实 API · 各家模型发布会的标准引用源", 12, SUB)
    return svg(740, 314, i)

def FIG_p20():
    i = R(30, 40, 190, 52, "#eff6ff", BLUE) + T(125, 62, "Agent A", 13, BLUE, "middle", "600") + T(125, 81, "你的平台 / 知识库", 10.5, SUB)
    i += R(30, 190, 190, 52, "#f5f3ff", PURPLE) + T(125, 212, "Agent B", 13, PURPLE, "middle", "600") + T(125, 231, "其他团队的智能体", 10.5, SUB)
    i += R(520, 40, 200, 60, "#ecfdf5", GREEN)
    i += T(620, 62, "工具 / 数据", 12.5, GREEN, "middle", "600")
    i += T(620, 82, "数据库 · API · 文档", 10.5, SUB)
    i += AR(220, 66, 518, 66, GREEN)
    i += R(300, 48, 150, 36, "#fff", GREEN, rx=18) + T(375, 71, "MCP", 14, GREEN, "middle", "700")
    i += T(375, 122, "Tools · Resources · Prompts 三原语", 11, SUB)
    i += T(375, 140, "'Agent 的手和眼'", 11, SUB)
    i += AR(125, 150, 125, 188, PURPLE)
    i += R(40, 152, 170, 32, "#fff", PURPLE, rx=16) + T(125, 173, "A2A 任务委托", 12, PURPLE, "middle", "600")
    i += T(370, 268, "MCP = 手和眼（调工具）· A2A = 外交（agent 间委托）· 互补构成互操作栈", 12.5, INK, "middle", "600")
    i += T(370, 292, "企业化落点：条款库/佣金接口封装为 MCP Server → 生态内所有 agent 可调用", 12, SUB)
    return svg(740, 308, i)

FIGS = {
    "p01": FIG_p01(), "p02": FIG_p02(), "p03": FIG_p03(), "p04": FIG_p04(), "p05": FIG_p05(),
    "p06": FIG_p06(), "p07": FIG_p07(), "p08": FIG_p08(), "p09": FIG_p09(), "p10": FIG_p10(),
    "p11": FIG_p11(), "p12": FIG_p12(), "p13": FIG_p13(), "p14": FIG_p14(), "p15": FIG_p15(),
    "p16": FIG_p16(), "p17": FIG_p17(), "p18": FIG_p18(), "p19": FIG_p19(), "p20": FIG_p20(),
}
