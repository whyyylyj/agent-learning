# -*- coding: utf-8 -*-
"""生成两个实战案例深度页，并把案例挂进 index.html"""
import os, re

import os
BASE = os.environ.get("KB_SITE") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

CSS_LINK = "../assets/style.css"

CASE_CSS = """
<h2>占位</h2>
"""
EXTRA = """
.arch{background:#fff;border:1px solid #e5e7eb;border-radius:10px;padding:14px 16px;margin:12px 0}
.arch .layer{border-radius:8px;padding:9px 14px;margin:6px 0;font-size:13.5px}
.arch .l1{background:#eff6ff;border:1.5px solid #2563eb}
.arch .l2{background:#fef3c7;border:1.5px solid #d97706}
.arch .l3a{background:#ecfdf5;border:1.5px solid #059669}
.arch .l3b{background:#f5f3ff;border:1.5px solid #7c3aed}
.arch .l3c{background:#fff1f2;border:1.5px solid #dc2626}
.arch .l4{background:#f1f5f9;border:1.5px solid #64748b}
.arch .arrow{color:#94a3b8;text-align:center;font-size:14px;margin:-2px 0}
.arch .layer b{font-size:13.5px}
.arch .layer small{color:#64748b}
table.sel{width:100%;border-collapse:collapse;background:#fff;font-size:13px;margin:10px 0}
table.sel th{background:#1f4e79;color:#fff;padding:7px 10px;text-align:left}
table.sel td{padding:7px 10px;border-bottom:1px solid #e5e7eb;vertical-align:top}
.ph{background:#fef9c3;border-bottom:1px dashed #ca8a04;padding:0 3px}
.case-src{font-size:12.5px;color:#475569}
.case-src li{margin:3px 0}
"""

def md(s):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)

def page(title, body):
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - 实战案例</title><link rel="stylesheet" href="../assets/style.css"><style>{EXTRA}</style></head>
<body><div class="wrap">
<a class="back" href="../index.html">← 返回总览</a>
{body}
<div class="foot">实战案例深度笔记 · Steven Li 面试准备知识库 · 黄色高亮处请按真实项目数据替换后使用</div>
</div></body></html>"""

# ============ CASE 1 ============
case1_body = f"""
<div class="catline"><span class="chip" style="background:#0f766e">实战案例 1 · 保险垂直场景</span></div>
<h1>民生保险：知识库问答 + 佣金问答 + 场景识别 / 意图匹配（保单变更识别 + 规则校验）</h1>

<h2>一、明确场景：用户是谁、问什么、痛点在哪</h2>
<p><b>服务对象：</b>内部代理人 / 运营坐席为主（企微侧 / 坐席工作台），覆盖售前咨询与售后办理两类动作。</p>
<p><b>三个问题域（对应三条链路）：</b></p>
<ul class="pts">
<li><b>条款知识问答：</b>"这款产品的等待期多久？宽限期之后合同什么状态？"——考的是保险条款 PDF 的准确理解与引用；条款长、表格多、术语密（现金价值 / 宽限期 / 减额交清），且同一段话在不同产品里含义不同。</li>
<li><b>佣金问答：</b>"我这个月的首年佣金是多少？续期佣金比例怎么算？"——涉及<b>个人数据 + 计算规则</b>，要求一分钱不能错，且不能把 A 业务员的数据混给 B。</li>
<li><b>保单变更办理：</b>"我要把受益人改成我爱人"——先识别这是办理类意图，抽取变更要素（保单 / 变更项 / 新受益人及关系），再按险种规则校验（是否允许变更、关系限制、是否需要回执），最后给办理引导。<b>规则判定不能交给 LLM</b>。</li>
</ul>
<div class="callout"><b>业务红线（面试必讲）：</b>保险是强监管行业——答案必须可溯源到条款原文；办理与计算必须走确定性链路；LLM 的职责被严格限定在"理解、抽取、组织语言"，判定与计算交给规则引擎和系统接口。</div>

<h2>二、架构设计（分层）</h2>
<div class="arch">
<div class="layer l1"><b>接入层</b> ｜ 企微侧 / 坐席工作台，会话上下文与会话 ID 贯穿</div>
<div class="arrow">↓</div>
<div class="layer l2"><b>意图层：场景识别 + 意图匹配 + 置信度路由</b><br><small>规则层（高风险词 / 固定话术正则）→ 小模型分类（高频意图粗筛）→ LLM 兜底细分类；置信度低转人工。<span style="color:#b45309">这是整条链路的调度中枢。</span></small></div>
<div class="arrow">↓ 按 intent 分流</div>
<div class="layer l3a"><b>链路 A · 条款知识问答（RAG）</b><br><small>条款 PDF 解析（表格专项提取）→ 结构感知分块 → Milvus 混合检索（向量 + BM25）→ Rerank 精排 → Grounded 生成（强制引用条款原文 + 无依据即拒答）</small></div>
<div class="layer l3b"><b>链路 B · 佣金问答（数字不过 LLM）</b><br><small>槽位抽取（险种 / 佣金月份 / 人员身份）→ 权限校验 → 调佣金系统 API 取数 → 模板化拼装回答（口径与免责声明固定）</small></div>
<div class="layer l3c"><b>链路 C · 保单变更办理</b><br><small>变更意图识别 → LLM 结构化抽取变更要素（JSON schema 约束）→ <b>规则引擎校验</b>（可变更项 / 关系限制 / 费用试算，全部确定性规则）→ 输出办理引导与材料清单（不直接改保单）</small></div>
<div class="arrow">↓</div>
<div class="layer l4"><b>评估与运营层</b> ｜ 分类别 Golden Set（条款 / 佣金 / 变更）· badcase 自动回流 · Prompt 版本管理与回归评测</div>
</div>

<h2>三、技术选型与取舍</h2>
<table class="sel">
<tr><th style="width:110px">决策点</th><th style="width:150px">最终选择</th><th style="width:170px">被否方案</th><th>取舍理由</th></tr>
<tr><td>知识注入方式</td><td><b>RAG</b></td><td>领域微调</td><td>产品条款高频上下架、监管口径会变：微调更新慢且不可溯源；RAG 答案可挂条款原文，满足合规审计。</td></tr>
<tr><td>意图识别</td><td><b>三层：规则 → 小模型 → LLM 兜底</b></td><td>端到端大模型直出意图</td><td>高频意图用规则/小模型毫秒级、零 token 成本且可解释；LLM 只处理长尾。纯 LLM 方案延迟、成本、可解释性都不达标——<b>面经印证：被问"怎么提升意图识别"时答"换更大的模型"是公认扣分项</b>。</td></tr>
<tr><td>变更规则判定</td><td><b>规则引擎</b></td><td>LLM 直接判定能否办理</td><td>合规要求判定过程确定、可复现、可审计；LLM 只负责把自然语言抽取成规则引擎的入参（结构化 JSON，schema 约束）。</td></tr>
<tr><td>佣金数字</td><td><b>查系统接口 + 模板拼装</b></td><td>LLM 计算 / NL2SQL</td><td>金额必须精确且涉及个人数据权限；接口返回既准又天然带权限控制，NL2SQL 的不确定性在"一分钱不能错"面前不可接受。</td></tr>
<tr><td>检索策略</td><td><b>混合检索 + Rerank</b></td><td>纯向量检索</td><td>"宽限期""现金价值"等术语与数字字段需要精确匹配，纯向量对专名/数字召回不稳；Rerank 修正融合后的排序。</td></tr>
<tr><td>长文档处理</td><td><b>结构感知分块 + 表格整体入库</b></td><td>固定长度切分</td><td>条款里的责任免除表/费率表被切断后，模型会"补全"缺失内容——这是幻觉的重要来源。</td></tr>
</table>

<h2>四、解决了哪些具体问题（badcase → 方案 → 效果）</h2>
<ul class="pts">
<li><b>多产品条款"张冠李戴"：</b>检索把 A 产品的条款片段和 B 产品的片段混在一起，生成时张冠李戴。→ 意图层前置产品名识别 + 检索层按产品元数据强过滤；跨产品对比类问题走专用对比链路。</li>
<li><b>表格切断诱发幻觉：</b>费率表 / 责任免除表被固定长度切块拦腰切断，模型自行"补全"缺失行。→ 结构感知分块：表格整体作为一个 chunk 并配表格标题元数据。</li>
<li><b>佣金数字幻觉：</b>早期直接把佣金规则文档喂给 LLM 让它算，金额偶发错误。→ 链路 B 上线后计算与取数全部走系统接口，LLM 不再接触算术。</li>
<li><b>办理规则编造：</b>模型曾输出"变更受益人需在 3 天内办理"这类编造规则。→ 规则文本统一由规则引擎按险种输出生成，LLM 零规则生成权限。</li>
<li><b>拒答与体验平衡：</b>拒答阈值过高压 THE 转人工率，过低引幻觉。→ 按意图分类别配阈值 + 拒答后给"相似问题推荐 / 转人工"软着陆。<span class="ph">拒答率 / 转人工率填真实值</span></li>
</ul>
<p class="sub">效果口径（面试表述用，务必替换为真实值）：条款问答准确率 <span class="ph">__%</span>、意图 Top1 准确率 <span class="ph">__%</span>、佣金类零算错、变更抽取结构化字段准确率 <span class="ph">__%</span>。</p>

<h2>五、工业界怎么做的（外部印证）</h2>
<ul class="case-src">
<li><b>平安人寿 AskBob</b>：代理人智能工作助理，实时解答产品条款与客户需求分析；核保场景 7×24 零等待、<b>有效解答率超 90%</b>；入选首个国家级"DeepSeek+保险"案例。（<a target="_blank" href="https://www.shaqiu.cn/article/1awlLodwVWzP">沙丘社区：12 个保险业大模型案例</a> / <a target="_blank" href="https://caijing.chinadaily.com.cn/a/202510/24/WS68fb2b51a310c4deea5ee0ba.html">中国日报</a>）</li>
<li><b>众安保险</b>："保险 + AI"全链路（产品 / 营销 / 运营 / 客服），发布国内保险业首份 AIGC 应用白皮书。（<a target="_blank" href="http://www.cb.com.cn/index/show/zj/cv/cv135228301260">中国经营网</a>）</li>
<li><b>行业口径</b>：大模型智能客服的咨询解决率普遍做到 <b>90% 以上</b>（阳光保险等）——你项目的准确率口径可以直接对标。（<a target="_blank" href="https://econ.pku.edu.cn/ccissr/bdbxpl/50161zgbxy387244.htm">北大经济学院</a>）</li>
<li><b>跨界同构案例 Morgan Stanley</b>：GPT-4 + 约 10 万份研究报告 / 数十万财富管理文档的知识库，服务 1.6 万名顾问，答案<b>只允许来自内部内容</b>并配套 AI evals 评估体系——与你的"内部条款库 + 溯源 + 评测"同构，国际大行验证了同一架构。（<a target="_blank" href="https://openai.com/index/morgan-stanley/">OpenAI 官方案例</a>）</li>
<li><b>意图识别工程化</b>：阿里云 PAI 官方给出基于 Qwen 的意图识别完整方案（数据准备→训练→评测→部署），印证三层意图体系的行业主流地位。（<a target="_blank" href="https://help.aliyun.com/zh/pai/use-cases/llm-based-intent-recognition-solution">阿里云 PAI</a> / <a target="_blank" href="https://developer.jdcloud.com/article/4457">京东云保险 AI 实战</a>）</li>
</ul>

<h2>六、学术界怎么做（论文与基准）</h2>
<ul class="case-src">
<li><b>TAT-QA</b>（ACL 2021，被引 700+，<a target="_blank" href="https://arxiv.org/abs/2105.07624">arXiv:2105.07624</a>）：真实财报上的"表格 + 文本"混合问答——正是佣金费率表 / 条款表格类问题的学术原型。</li>
<li><b>FinQA</b>（EMNLP 2021，<a target="_blank" href="https://arxiv.org/abs/2109.00122">arXiv:2109.00122</a>）：金融文档上的数值推理（带步骤程序），对应"佣金怎么算出来"的可解释计算链。</li>
<li><b>FinanceBench</b>（Patronus AI，<a target="_blank" href="https://arxiv.org/abs/2311.11944">arXiv:2311.11944</a>）：10,231 道开卷金融 QA，实证显示 LLM 直接作答错误率很高——这是"数字不过 LLM"最硬的学术依据。</li>
<li><b>InsuranceQA</b>（早期保险领域问答数据集）：保险垂直 QA 的先行基准，说明领域 QA 数据与通用 QA 的差异早在 LLM 之前就被验证。</li>
<li><b>意图识别 / 槽位填充</b>：从 SLU 经典任务到 LLM function calling 的结构化输出——保单变更抽取在学术上就是"意图分类 + slot filling + 校验"的组合。</li>
</ul>

<h2>七、与 20 篇论文的映射</h2>
<table class="tbl">
<tr><th>论文</th><th>在本案例中的落点</th></tr>
<tr><td><a href="../papers/anthropic-building-effective-agents.html">① Building Effective Agents</a></td><td>意图路由 = Routing 模式；条款问答链 = Chaining；Prompt 迭代闭环 = Evaluator-Optimizer。</td></tr>
<tr><td><a href="../papers/openai-practical-guide-building-agents.html">② OpenAI 落地指南</a></td><td>Guardrails 分层（输入过滤 / 权限过滤 / 事实校验 / 人工升级）在本案例的对应实现。</td></tr>
<tr><td><a href="../papers/manus-context-engineering.html">⑤ Manus 上下文工程</a></td><td>条款长文档的上下文预算：分块即"取"、rerank 截断即"选"、摘要即"压"。</td></tr>
<tr><td><a href="../papers/context-engineering-survey.html">⑥ 上下文工程综述</a></td><td>把整个平台描述为"一套面向保险领域的上下文工程系统"。</td></tr>
<tr><td><a href="../papers/mast-multi-agent-failure.html">⑧ MAST</a></td><td>验证层缺失是多智能体失败第三大类——变更链路"抽取与判定分离 + 规则引擎"正是对验证缺失的工程防御。</td></tr>
<tr><td><a href="../papers/bfcl-v3.html">⑱ BFCL V3</a></td><td>irrelevance detection ↔ 你的意图匹配与拒答：判断"该不该调工具/走哪条链路"是公认的一级评测维度。</td></tr>
<tr><td><a href="../papers/mcp-a2a-protocols.html">⑲ MCP / A2A</a></td><td>条款库 / 佣金接口可封装为 MCP Server，向代理人侧的 agent 生态输出能力。</td></tr>
</table>

<h2>八、面试怎么讲（场景 → 话术）</h2>
<div class="iv">开场 60 秒版本｜"我在通联数据负责的 AI 平台在民生保险落地，核心是三条链路：条款知识问答走 RAG（结构感知分块 + 混合检索 + Rerank + 引用拒答）；佣金问答因为'一分钱不能错'，我们让数字完全不过 LLM，走接口取数加模板；保单变更这类办理意图，LLM 只做要素抽取，判定交给规则引擎保证合规。意图层用'规则→小模型→LLM 兜底'三层路由。上线后条款问答准确率【__%】，佣金零算错。"</div>
<div class="iv">被问"为什么不用大模型直接判定变更规则"｜"监管口径下，判定必须确定、可复现、可审计。LLM 的角色是理解与抽取，规则的执行交给规则引擎——这符合 Anthropic 说的 workflow 优先原则，也是金融行业落地的通行做法（平安 AskBob 等同类场景的核保判定同样如此）。"</div>
<div class="iv">被问"意图识别准确率怎么提"｜"千万别答换大模型——面经里这是扣分项。我的三层：规则兜高频、小模型扛长尾、LLM 处理模糊与新增意图；再加 badcase 回流做半自动标注迭代，每次上线前跑分类别评测。"</div>
<div class="iv">被问"条款更新怎么保证知识库新鲜"｜"增量解析 + 增量索引更新 + 缓存失效；条款生效日期作为元数据参与过滤，旧版本条款不参与召回。"（呼应你简历里的增量索引更新。）</div>
<h2>九、高频追问清单</h2>
<ul class="pts deep">
<li>佣金问答为什么不做成 NL2SQL？——权限、口径、审计三座山；接口优先。</li>
<li>意图类别边界怎么定义的？变更类内部又如何细分险种 / 变更项？</li>
<li>条款里表格特别多，解析准确率怎么保障？坏例怎么发现？</li>
<li>拒答说"不知道"之后，怎么把用户引导回正轨（相似问题 / 转人工 / 工单）？</li>
<li>如果监管要求所有答案 100% 可溯源，你的架构要改哪里？——答：无引用不展示，引用覆盖率纳入评测。</li>
</ul>
"""

# ============ CASE 2 ============
case2_body = f"""
<div class="catline"><span class="chip" style="background:#7c2d12">实战案例 2 · 金融深度研究</span></div>
<h1>基金组合绩效评价系统：复用数据层 + 组件 API 封装 + skill 适配 × ReAct/Plan 多步推理</h1>

<h2>一、明确场景：给金融机构的基金组合资产配置绩效评价</h2>
<p><b>场景定义：</b>服务银行、保险、券商等金融机构的<b>基金组合资产配置绩效评价系统</b>。用户的提问形态："这个组合二季度为什么跑输基准？""帮我看看组合 A 和 B 上半年的风险收益对比""最大回撤发生在什么时候、归因到哪些持仓"。这类问题的特点：<b>答案是算出来的不是检索出来的</b>——需要多步调用计算组件（收益 / 风险 / 归因 / 对比），中间结果相互依赖，且每个数字必须与原系统对得上账。</p>
<p><b>三个架构前提（面试开场就讲清楚，体现架构判断力）：</b></p>
<ul class="pts">
<li><b>复用原有系统数据层：</b>基金净值、持仓、组合构成、基准曲线等数据原系统早就有了，且经过多年校验。agent 层坚决不建第二套数据源——两套数据层必然口径分裂，用户拿 agent 结论与系统页面对照时出现 7.2% vs 7.1% 就是信任崩塌事故。</li>
<li><b>能力组件封装为 API：</b>原系统后面的绩效计算、风险指标、Brinson 归因等能力组件已存在，但与人用页面耦合。把它们封装成 agent 可调用的工具 API（schema 化入参、幂等可重试、错误语义化），是整个系统的核心工程量。</li>
<li><b>skill 适配 + ReAct/Plan 多步推理：</b>结合用户提问场景适配 skill（收益评价 / 风险评价 / 归因分析 / 基准对比 / 持仓穿透 / 调仓评估），skill 内部用 Plan 生成任务 DAG 骨架、节点内用 ReAct 灵活执行——骨架防漂移、节点内防僵硬。</li>
</ul>

<h2>二、架构设计（skill 适配 + 组件编排的骨架）</h2>
<div class="arch">
<div class="layer l1"><b>① 场景识别与 skill 适配</b> ｜ 结合机构类型、提问语境、组合上下文识别分析场景 → 匹配 skill 卡片（场景描述 / 输入输出契约 / 前置条件 / 组件编排模板）；含 irrelevance 检测（预测类问题明确拒答）</div>
<div class="arrow">↓</div>
<div class="layer l2"><b>② Plan：任务 DAG 规划</b><br><small>分析问题拆解为组件调用 DAG（节点=指标计算/归因/对比，边=数据依赖）；依赖分析防环；执行中发现缺口允许受限重规划（最多 2 次、只调受影响子图）</small></div>
<div class="arrow">↓</div>
<div class="layer l3a"><b>③ ReAct：节点内执行 × 并行调度</b><br><small>无依赖节点并行调用组件 API（依赖感知调度 + 每端点独立限流）；节点内 ReAct 处理参数准备与异常；任务黑板管理中间结果（数字句柄化、结论卡常驻）</small></div>
<div class="layer l3b"><b>④ 数据层与能力组件（复用）</b><br><small>原系统数据层（净值/持仓/组合/基准）+ 封装后的绩效计算组件（收益/风险/归因）——agent 流量独立配额、让路生产流量；权限模型原样继承</small></div>
<div class="arrow">↓</div>
<div class="layer l4"><b>⑤ 勾稽校验与报告生成</b> ｜ 数字类结论 claim 级对账（与组件返回逐位一致、口径标签强制）；分析完整性 rubric 评估；缺口显式声明——宁短不错</div>
</div>

<h2>三、技术选型与取舍</h2>
<table class="sel">
<tr><th style="width:130px">决策点</th><th style="width:170px">选择</th><th style="width:170px">被否 / 暂缓方案</th><th>取舍理由</th></tr>
<tr><td>数据访问</td><td><b>复用原数据服务 API（协商加批量端点）</b></td><td>agent 直连数仓写 SQL / 新建数据视图</td><td>口径一致性是绩效评价的生命线；权限模型继承；SQL 路线的权限/口径/审计三关全挂。批量端点消解调用次数，独立配额避免与生产页面抢资源。</td></tr>
<tr><td>能力复用</td><td><b>agent 工具网关统一封装组件</b></td><td>直接暴露内部 RPC / 按 agent 场景重写组件</td><td>RPC 与页面会话耦合、错误码模型看不懂；重写丢掉原系统多年校验的正确性积累。网关做 schema 标准化 + 错误语义化 + 工具目录管理。</td></tr>
<tr><td>推理模式</td><td><b>Plan 骨架 + 节点内 ReAct</b></td><td>纯 ReAct / 纯 Plan-and-Execute</td><td>纯 ReAct 长任务漂移与循环；纯 Plan 无法应对执行期数据缺失。骨架防漂移、节点内灵活，重规划带预算（2 次、只调受影响子图）。</td></tr>
<tr><td>场景路由</td><td><b>skill 库 + 描述式路由</b></td><td>单一通用 agent / 微调场景分类模型</td><td>绩效评价问题空间是有限集（分析框架模式化），通用 agent 每次现场发挥等于重新发明分析流程；skill 增删时描述式路由零训练成本。</td></tr>
<tr><td>数字精度</td><td><b>数字不过 LLM：claim 级勾稽 + 模板段透传</b></td><td>生成后校验 / 全模板报告</td><td>数字经过生成环节就是概率性复制（抄错 120.3→102.3 实际发生过）；数字段模板化透传、叙述段生成后逐条勾稽对账。全模板会让分析表述僵化，混合是平衡点。</td></tr>
<tr><td>编排引擎</td><td><b>Prompt 编排先行，RL 作为演进</b></td><td>直接上 RL 训练的 agent</td><td>DeepResearcher 证明端到端 RL 是方向，但需要环境与奖励基建。绩效评价的天然优势：数字勾稽就是 verifier 奖励（可自动计算）——编排积累轨迹，评测升级为奖励，两步走。</td></tr>
</table>

<h2>四、解决了哪些具体问题</h2>
<ul class="pts">
<li><b>页面粒度 API 不适配 agent：</b>原 API 为页面交互设计，一次评价要串几十次调用——协商批量时序端点 + 接入层超时分级，调用次数与时延同时压下来。</li>
<li><b>并行计算打挂共享数据层：</b>agent 流量与生产页面流量抢配额，早盘事故后确立铁律——独立配额 + 错峰 + 依赖感知并行（无依赖节点才并行）。<b>这正是异步轮询框架（QPS 10×）功底的直接迁移</b>。</li>
<li><b>多步推理的中间结果爆炸：</b>十几步组件调用的中间结果撑爆上下文且注意力稀释（引用错组合的数字）——任务黑板：数字句柄化、结论卡常驻、过程性结果外置。</li>
<li><b>数字与口径的事故级风险：</b>转写错误 / 费前费后口径漂移 / 舍入尾差三类不一致——数字段不过 LLM + 口径元数据强制 + 勾稽一致率纳入回归，用户数字质疑工单清零。</li>
</ul>
<p class="sub">效果口径（替换真实值）：分析框架完整执行率 <span class="ph">__%</span>、数字勾稽一致率 <span class="ph">100%（硬门槛）</span>、单次评价编排时延 <span class="ph">__分钟 → __秒</span>、单任务成本降 <span class="ph">__%</span>。</p>

<h2>五、工业界怎么做的（外部印证）</h2>
<ul class="case-src">
<li><b>Wind（万得）Alice</b>：自研金融大模型，提供智能搜索 / 问答 / <b>报告神笔（40+ 模板）</b> / 文档智读 / <b>深度研究</b>，并推出<b>万得 MCP</b> 让外部 agent 直接调用其数据库——"数据能力接口化开放"与本方案的组件封装方向一致。（<a target="_blank" href="https://www.wind.com.cn/mobile/News/NewsDetail/zh.html?id=735">Wind 官网</a>）</li>
<li><b>东方财富"妙想"金融大模型</b>：2025 年 3 月通过备案；覆盖投研 / 投顾 / 投教场景，推出<b>妙想投研助理</b>、深度思考模式与 <b>Skills 能力体系</b>——skill 化的分析能力封装与本方案的 skill 适配层同构。（<a target="_blank" href="https://acttg.eastmoney.com/pub/web_dfcfsy_dbtg_top_05_02_02_1">东方财富官网</a>）</li>
<li><b>同花顺"问财" HithinkGPT</b>：国内首批备案的金融大模型；问财 2.0 引入"慢思考"；开放 <b>iFinD MCP</b> 供外部 agent 调用数据库。（<a target="_blank" href="https://www.nbd.com.cn/articles/2024-01-15/3208042.html">每日经济新闻</a>）</li>
<li><b>行业趋势判断（面试引用）</b>：金融数据终端厂商正从"卖数据"转向"卖 AI 分析能力"，<b>DeepResearch 形态 + MCP/Skills 开放生态</b>是新战场——本方案"复用数据层 + 组件 API 封装 + skill 编排"正踩在这个趋势上，且比通用 deep research 更贴金融场景（数字勾稽是硬约束）。</li>
</ul>

<h2>六、学术界怎么做（论文与基准）</h2>
<ul class="case-src">
<li><b>DeepResearcher</b>（EMNLP 2025，被引 460+，<a target="_blank" href="https://arxiv.org/abs/2504.03160">arXiv:2504.03160</a>）：首个在<b>真实 web 环境</b>中端到端 RL（GRPO）训练深度研究 agent 的框架——RL 化演进的参照系，但需要环境与奖励基建，工程节奏上编排先行。</li>
<li><b>Search-R1</b>（<a target="_blank" href="https://arxiv.org/abs/2503.09516">arXiv:2503.09516</a>）：RL 训练模型在推理链中自主交错调用搜索引擎，这条技术线的开山之作。</li>
<li><b>Tongyi DeepResearch</b>（阿里，<a target="_blank" href="https://arxiv.org/abs/2510.24701">arXiv:2510.24701</a>）：30.5B（激活 3.3B）的深度研究专用模型，大规模合成数据 + agentic RL——工业界可直接参考其训练配方。</li>
<li><b>金融问答三基准</b>：<a target="_blank" href="https://arxiv.org/abs/2105.07624">TAT-QA</a>（表格+文本混合问答）/ <a target="_blank" href="https://arxiv.org/abs/2109.00122">FinQA</a>（数值推理）/ <a target="_blank" href="https://arxiv.org/abs/2311.11944">FinanceBench</a>（10,231 题开卷金融 QA）——数字结论的校验难度可对标这三者的任务分类。</li>
<li><b>Anthropic 多智能体研究系统</b>（<a target="_blank" href="https://www.anthropic.com/engineering/built-multi-agent-research-system">工程博客</a>）：编排者-执行者拓扑与成本数据（90.2% 提升 / 15× token）——并行编排的成本依据。</li>
</ul>

<h2>七、与 20 篇论文的映射</h2>
<table class="tbl">
<tr><th>论文</th><th>在本方案中的落点</th></tr>
<tr><td><a href="../papers/anthropic-multi-agent-research-system.html">③ 多智能体研究系统</a></td><td>编排者-执行者拓扑的原型：规划器拆任务 DAG、并行组件调用、状态增量保存；token 成本方差的量化依据。</td></tr>
<tr><td><a href="../papers/mast-multi-agent-failure.html">⑧ MAST</a></td><td>勾稽校验层直接回应"任务验证失败"类失败模式；受限重规划的触发条件设计参考其失败分类。</td></tr>
<tr><td><a href="../papers/manus-context-engineering.html">⑤ Manus</a></td><td>任务黑板的句柄化设计：文件系统当上下文、KV-cache 友好的追加式上下文。</td></tr>
<tr><td><a href="../papers/tongyi-deepresearch.html">⑮ Tongyi DeepResearch</a></td><td>RL 化演进路线的参照：合成任务数据 + agentic RL 的配方与成本结构。</td></tr>
<tr><td><a href="../papers/agentic-rl-survey.html">⑯ Agentic RL 综述</a></td><td>用 POMDP 语言形式化"组件调用 + 勾稽"：动作=工具调用，奖励=勾稽一致率与分析完整性。</td></tr>
<tr><td><a href="../papers/bfcl-v3.html">⑲ BFCL V3</a></td><td>skill 适配层的 irrelevance 检测（预测类问题拒答）与工具调用评测维度。</td></tr>
<tr><td><a href="../papers/mcp-a2a-protocols.html">⑳ MCP / A2A</a></td><td>工具网关的封装规范对齐 MCP（schema/描述/错误语义），未来跨团队 agent 经 A2A 委托分析子任务。</td></tr>
</table>

<h2>八、面试怎么讲（场景 → 话术）</h2>
<div class="iv">开场 60 秒版本｜"我做的金融 DeepResearch 是面向银行/保险/券商的基金组合绩效评价系统。三个架构决策先说清楚：数据层复用原系统——口径一致性比什么都值钱，坚决不建第二套数据源；原有能力组件封装成工具 API——schema 化入参、幂等、错误语义化，这是给 agent 用的接口不是给人用的接口；推理层 skill 适配加 Plan/ReAct 混合——Plan 出任务 DAG 骨架防漂移，节点内 ReAct 应对数据缺失。红线是数字勾稽：agent 每个数字必须与原系统对得上账，数字段不过 LLM。工程上并行调度的限流、超时、降级，是我异步轮询框架功底的直接迁移。"</div>
<div class="iv">被问"为什么复用老系统 API 而不是自建数据层"｜"两个原因：口径和权限。用户会拿 agent 结论与系统页面互查，两套数据层出现 7.2% 对 7.1% 就是信任事故；权限模型继承原系统的机构/用户/组合可见性，自建等于重做一遍合规。代价是接入工程——批量端点、独立配额、超时分级——但这些都是有标准解法的工程问题。"</div>
<div class="iv">被问"Plan 和 ReAct 为什么混着用"｜"各自缺陷互补：纯 ReAct 局部性好但长任务漂移循环，纯 Plan 全局清晰但执行期无法应对数据缺失。骨架防漂移、节点内防僵硬。关键设计是受限重规划——最多 2 次、只调受影响子图，无限重规划等于失控。"</div>
<div class="iv">被问"怎么保证数字不出错"｜"结构性防御：数字段模板化透传不过 LLM 改写——生成模型对数字是概率性复制，抄错 120.3 成 102.3 真实发生过；组件返回强制带口径元数据（费前费后/时间窗/单位/舍入）；报告拆 claim 逐条勾稽对账，一致率 100% 才出报告。这和我在保险佣金链路用的是同一条原则——数字不过 LLM，跨场景复用的架构原则。"</div>
<div class="iv">被问"为什么用 prompt 编排而不是 RL 训练"｜"DeepResearcher 证明 RL 是方向，但它需要环境与奖励基建。绩效评价恰好有天然优势——数字勾稽就是可自动计算的 verifier 奖励。我的节奏：编排先拿业务结果、埋点积累任务轨迹、勾稽评测升级为奖励函数，两步走不冲突——评测集就是未来 RL 的奖励基建。"</div>

<h2>九、高频追问清单</h2>
<ul class="pts deep">
<li>skill 怎么设计的，粒度怎么定？——按分析框架聚合（8 个），太细路由错误率高、太粗等于通用 agent；skill 卡片结构化（场景/契约/前置条件/编排模板）。</li>
<li>工具多了模型选不准怎么办？——按 skill 分组限定可见工具集，选择空间收窄；枚举参数动态拉取候选，模型只能选不能编。</li>
<li>组件挂了怎么办？——核心指标幂等重试 + 熔断；非核心标注缺口继续；重规划只处理任务级失败——缺口显式声明，宁短不错。</li>
<li>agent 流量会不会打挂生产系统？——独立配额 + 错峰 + 依赖感知并行；这个约束是复用内部数据层的代价，也是架构决策的一部分。</li>
<li>和 Wind Alice / 妙想这些产品的差距？——它们是通用投研助手，我做的是嵌入式绩效评价：壁垒在勾稽精度、skill 化的分析框架和与原系统的权限/口径继承——这些恰好是通用产品最难做的。</li>
</ul>
"""

c1 = page("民生保险：知识库问答 + 佣金问答 + 意图匹配（保单变更识别 + 规则校验）", case1_body)
c2 = page("基金组合绩效评价：数据层复用 + 组件 API 封装 + skill×ReAct/Plan", case2_body)

os.makedirs(os.path.join(BASE, "cases"), exist_ok=True)
with open(os.path.join(BASE, "cases", "case-minsheng-insurance.html"), "w", encoding="utf-8") as f:
    f.write(c1)
with open(os.path.join(BASE, "cases", "case-finance-deepresearch.html"), "w", encoding="utf-8") as f:
    f.write(c2)

# 把案例区挂进 index.html（插在"六大分类导航"之前）
idx_path = os.path.join(BASE, "index.html")
idx = open(idx_path, encoding="utf-8").read()
if "实战案例" not in idx:
    case_section = """<h2>实战案例 · 我的项目 × 论文（面试主战场）</h2>
<div class="grid">
<a class="card" href="cases/case-minsheng-insurance.html">
<div class="card-top"><span class="chip" style="background:#0f766e">实战案例 1 · 保险垂直场景</span><span class="date">民生保险落地</span></div>
<h3>知识库问答 + 佣金问答 + 意图匹配（保单变更识别 + 规则校验）</h3>
<div class="org">RAG · 三层意图路由 · 规则引擎 · 引用拒答</div>
<p>条款问答 / 佣金（数字不过 LLM）/ 变更办理（LLM 抽取 + 规则引擎校验）三条链路；含选型取舍、badcase 故事、工业案例（平安 AskBob、Morgan Stanley）与学术基准（TAT-QA / FinQA / FinanceBench）。</p>
<div class="tags"><span class="rtag">①Routing 模式</span><span class="rtag">②Guardrails</span><span class="rtag">⑧MAST 验证层</span><span class="rtag">⑱BFCL irrelevance</span></div></a>
<a class="card" href="cases/case-finance-deepresearch.html">
<div class="card-top"><span class="chip" style="background:#7c2d12">实战案例 2 · 金融深度研究</span><span class="date">DeepResearch 方案</span></div>
<h3>多路并行取数 + 结果校验 + 问答报告链路</h3>
<div class="org">规划 DAG · 并行取数 · 证据治理 · 交叉校验 · 分节报告</div>
<p>子问题拆解 → 多源/多查询并行取数（并发控制/超时降级）→ 证据治理与数字双源一致 → 分节引用报告；对标 OpenAI/Gemini Deep Research、Wind Alice、东方财富妙想、同花顺问财，论文锚点 DeepResearcher / Search-R1 / Tongyi。</p>
<div class="tags"><span class="rtag">③Orchestrator-worker</span><span class="rtag">⑮Tongyi DeepResearch</span><span class="rtag">⑯Agentic RL</span><span class="rtag">⑰BrowseComp</span></div></a>
</div>

"""
    idx = idx.replace("<h2>六大分类导航</h2>", case_section + "<h2>六大分类导航</h2>")
    open(idx_path, "w", encoding="utf-8").write(idx)
print("cases done, index patched:", "实战案例" in open(idx_path, encoding="utf-8").read())
