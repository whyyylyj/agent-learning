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
<h1>金融 DeepResearch 方案：多路并行取数 + 结果校验 + 问答报告链路</h1>

<h2>一、明确场景：研究型问题需要"多步 + 多源 + 可验证"</h2>
<p><b>场景定义：</b>投研 / 研究型提问——"某行业近三年的竞争格局与头部公司对比"、"这只基金的风格漂移情况"。这类问题的特点：<b>答案分散在多类数据源（公告 / 研报 / 财报 / 行情 / 新闻）、需要多跳推理、单轮 RAG 必然不完整、结论必须有证据链</b>。</p>
<p><b>与知识库问答的关系：</b>知识库问答是"单轮检索 → 单次生成"的 1.0 形态；DeepResearch 是"规划 → 并行取数 → 校验 → 综合"的长程 2.0 形态。两者共享同一套底层资产：检索质量、评估闭环、引用溯源。</p>

<h2>二、架构设计（并行取数 + 校验的骨架）</h2>
<div class="arch">
<div class="layer l1"><b>问题理解与规划</b> ｜ 研究问题 → 拆解为子问题 DAG（如"竞争格局"→ 市场规模 / 玩家份额 / 壁垒 / 近期事件），每个子问题绑定数据源与工具</div>
<div class="arrow">↓</div>
<div class="layer l2"><b>多路并行取数</b><br><small>两个维度的并行：①数据源并行——公告库 / 研报库 / 财报结构化库 / 行情 API / 新闻各自独立检索；②查询变体并行——同一子问题生成多个改写 query。统一并发控制、超时与降级（单路失败不阻塞整体）</small></div>
<div class="arrow">↓</div>
<div class="layer l3a"><b>证据治理</b><br><small>去重 · 时间戳与统计口径对齐（不同源"营收"口径可能不同）· 证据打分（来源权威度 / 新鲜度 / 相关度）</small></div>
<div class="layer l3b"><b>交叉校验</b><br><small>数字类结论要求多源一致（≥2 个独立源）；日期 / 单位 / 口径规则校验；无证据支撑的 claim 直接剔除或标记"未证实"——<b>校验不过的证据不进报告</b></small></div>
<div class="arrow">↓</div>
<div class="layer l4"><b>综合与报告生成</b> ｜ 分节生成 + 全文引用溯源 + rubric 质量评估（结构完整 / 观点有据 / 口径一致）</div>
</div>

<h2>三、技术选型与取舍</h2>
<table class="sel">
<tr><th style="width:130px">决策点</th><th style="width:160px">选择</th><th style="width:170px">被否 / 暂缓方案</th><th>取舍理由</th></tr>
<tr><td>执行拓扑</td><td><b>编排者 + 并行取数单元</b></td><td>纯串行 RAG / 完全自主多智能体</td><td>研究任务天然可并行（子问题独立），并行买的是时延与覆盖广度；但完全自主多智能体引入巨大 token 成本与调试复杂度（Anthropic 数据：多智能体 token ≈ 15× 聊天，收益集中在可并行任务）。</td></tr>
<tr><td>取数方式</td><td><b>内部数据源 API / 接口优先</b></td><td>通用爬虫</td><td>金融数据有版权与合规约束；接口数据结构化、可鉴权、可审计。爬虫只作为公开新闻的补充。</td></tr>
<tr><td>校验机制</td><td><b>多源一致性 + 规则校验</b></td><td>单模型自检</td><td>让生成答案的模型自己检查自己，等于既当运动员又当裁判；多源独立证据的一致性 + 确定性规则（日期 / 单位 / 口径）才可信。</td></tr>
<tr><td>编排引擎</td><td><b>Prompt 编排先行</b></td><td>直接上 RL 训练的 agent</td><td>DeepResearcher 证明端到端 RL 是方向（真实 web 环境 + GRPO），但需要环境、奖励与基建投入；工程上先用编排拿到业务结果，RL 化作为演进路线。</td></tr>
<tr><td>报告生成</td><td><b>分节生成 + 引用</b></td><td>一次生成全文</td><td>长文一次生成无法控制结构与证据绑定；分节生成每节带证据集，才能保证"观点有据"。</td></tr>
</table>

<h2>四、解决了哪些具体问题</h2>
<ul class="pts">
<li><b>多源数据冲突：</b>同一指标在公告、新闻、第三方库中数字不一致。→ 证据治理层做口径与时间戳对齐，数字类结论强制双源一致，冲突时并列展示来源与口径。</li>
<li><b>并行取数的工程问题：</b>多路并发的限流、超时、失败重试、部分失败下的降级（缺哪路就标注数据缺口而不是编造）——<b>这正是你分布式异步轮询框架的功底所在</b>。</li>
<li><b>无证据编造：</b>拆解出的子问题若数据源覆盖不到，模型倾向于"合理推断"。→ 校验层强制 claim-evidence 绑定，未证实内容显式标注。</li>
<li><b>长报告上下文爆炸：</b>多源证据总量远超窗口。→ 证据按相关度与来源分选压缩，报告分节生成，节间只传结论性摘要——上下文工程（Manus：文件系统当上下文）。</li>
</ul>
<p class="sub">效果口径（替换真实值）：端到端报告可用率 <span class="ph">__%</span>、数字结论双源一致率 <span class="ph">__%</span>、平均耗时从人工 <span class="ph">__小时 → __分钟</span>。</p>

<h2>五、工业界怎么做的（外部印证）</h2>
<ul class="case-src">
<li><b>OpenAI Deep Research</b>（2025.02 发布）与 <b>Gemini Deep Research</b>、<b>Kimi-Researcher</b>（月之暗面，2025.06）：deep research 成为 2025 年所有前沿实验室的标配产品形态——印证"单轮 RAG → 长程研究"是行业公认的演进方向。</li>
<li><b>Wind（万得）Alice</b>：自研金融大模型，提供智能搜索 / 问答 / <b>报告神笔（40+ 模板）</b>/ 文档智读 / <b>深度研究</b>，并推出<b>万得 MCP</b> 让外部 agent 直接调用其数据库；Alice 投顾助手获 2025 金融 AI 创新应用"标杆奖"。（<a target="_blank" href="https://www.wind.com.cn/mobile/News/NewsDetail/zh.html?id=735">Wind 官网</a>）</li>
<li><b>东方财富"妙想"金融大模型</b>：2025 年 3 月通过备案；覆盖投研 / 投顾 / 投教场景，推出<b>妙想投研助理</b>、深度思考模式与 Skills 能力体系。（<a target="_blank" href="https://acttg.eastmoney.com/pub/web_dfcfsy_dbtg_top_05_02_02_1">东方财富官网</a> / <a target="_blank" href="https://wallstreetcn.com/articles/3774077">华尔街见闻</a>）</li>
<li><b>同花顺"问财" HithinkGPT</b>：国内首批备案的金融大模型；问财 2.0 引入"慢思考"；开放 <b>iFinD MCP</b> 供外部 agent 调用数据库。（<a target="_blank" href="https://www.nbd.com.cn/articles/2024-01-15/3208042.html">每日经济新闻</a>）</li>
<li><b>行业趋势判断（面试引用）</b>：金融数据终端厂商正从"卖数据"转向"卖 AI 工具"，<b>DeepResearch 能力 + MCP/Skills 开放生态</b>是新战场（<a target="_blank" href="https://stcn.com/article/detail/3620915.html">证券时报</a>）——你的"多路并行取数 + 校验"方案正踩在这个趋势上。</li>
</ul>

<h2>六、学术界怎么做（论文与基准）</h2>
<ul class="case-src">
<li><b>DeepResearcher</b>（EMNLP 2025，被引 460+，<a target="_blank" href="https://arxiv.org/abs/2504.03160">arXiv:2504.03160</a>）：首个在<b>真实 web 环境</b>中端到端 RL（GRPO）训练深度研究 agent 的框架，显著优于 RAG 与 SFT 基线——证明"取数-推理-校验"行为可以被 RL 学出来。</li>
<li><b>Search-R1</b>（<a target="_blank" href="https://arxiv.org/abs/2503.09516">arXiv:2503.09516</a>）：RL 训练模型在推理链中自主交错调用搜索引擎，是这条技术线的开山之作。</li>
<li><b>Tongyi DeepResearch</b>（阿里，<a target="_blank" href="https://arxiv.org/abs/2510.24701">arXiv:2510.24701</a>）：30.5B（激活 3.3B）的深度研究专用模型，大规模合成数据 + agentic RL，开源 deep research 系基准第一梯队——工业界可直接参考其训练配方。</li>
<li><b>The Landscape of Agentic RL</b>（<a target="_blank" href="https://arxiv.org/abs/2509.02547">arXiv:2509.02547</a>）：把深度研究 agent 形式化为 POMDP，系统化奖励设计与多轮信用分配——给"多路取数 + 校验"提供理论语言。</li>
<li><b>金融问答三基准</b>：<a target="_blank" href="https://arxiv.org/abs/2105.07624">TAT-QA</a>（表格+文本混合问答，ACL 2021）/ <a target="_blank" href="https://arxiv.org/abs/2109.00122">FinQA</a>（数值推理，EMNLP 2021）/ <a target="_blank" href="https://arxiv.org/abs/2311.11944">FinanceBench</a>（10,231 题开卷金融 QA）——报告里数字结论的校验难度可对标这三者的任务分类。</li>
<li><b>Anthropic 多智能体研究系统</b>（<a target="_blank" href="https://www.anthropic.com/engineering/built-multi-agent-research-system">工程博客</a>）：编排者-执行者的工业级实现与成本数据（90.2% 提升 / 15× token）。</li>
</ul>

<h2>七、与 20 篇论文的映射</h2>
<table class="tbl">
<tr><th>论文</th><th>在本方案中的落点</th></tr>
<tr><td><a href="../papers/anthropic-multi-agent-research-system.html">③ 多智能体研究系统</a></td><td>编排者-执行者拓扑的原型：LeadAgent 拆解任务、subagent 并行取数、状态增量保存。</td></tr>
<tr><td><a href="../papers/mast-multi-agent-failure.html">⑧ MAST</a></td><td>校验层设计直接回应"任务验证失败"类失败模式；子任务说明书防止 agent 间对齐失败。</td></tr>
<tr><td><a href="../papers/manus-context-engineering.html">⑤ Manus</a></td><td>长报告的上下文预算：证据句柄化、分节生成、KV-cache 友好的追加式上下文。</td></tr>
<tr><td><a href="../papers/tongyi-deepresearch.html">⑮ Tongyi DeepResearch</a></td><td>RL 化演进路线的参照：合成任务数据 + agentic RL 的配方与成本结构。</td></tr>
<tr><td><a href="../papers/agentic-rl-survey.html">⑯ Agentic RL 综述</a></td><td>用 POMDP 语言形式化"多路取数 + 校验"：动作=检索/读取/校验，奖励=事实正确性与覆盖度。</td></tr>
<tr><td><a href="../papers/browsecomp-benchmark.html">⑰ BrowseComp</a></td><td>评测集设计原则"难找易验"：多跳、需交叉验证的问题分层，控制标注成本。</td></tr>
<tr><td><a href="../papers/mcp-a2a-protocols.html">⑲ MCP / A2A</a></td><td>数据源（公告/研报/行情）封装为 MCP 工具，跨团队 agent 经 A2A 委托研究子任务。</td></tr>
</table>

<h2>八、面试怎么讲（场景 → 话术）</h2>
<div class="iv">开场 60 秒版本｜"我的知识库问答是单轮 RAG 的 1.0；面向投研场景我设计了 DeepResearch 形态的 2.0：规划器把研究问题拆成子问题 DAG，多数据源与多查询变体并行取数，经过证据治理（去重、口径对齐、打分）后做交叉校验——数字要求双源一致，无证据的 claim 直接剔除——最后分节生成带引用的报告。工程上这套并行取数的并发控制、超时降级，正是我此前做异步轮询框架（QPS 10×）的功底迁移。"</div>
<div class="iv">被问"多源数据冲突怎么办"｜"三层处理：治理层做时间戳与口径对齐；校验层要求数字类结论双源一致、冲突时并列展示来源与口径；生成层明确标注分歧而不是和稀泥。金融场景里，诚实呈现分歧比强行给一个数更专业。"</div>
<div class="iv">被问"为什么用 prompt 编排而不是 RL 训练"｜"DeepResearcher 证明 RL 在真实 web 环境端到端训练效果更好（EMNLP 2025，被引 460+），但它需要环境与奖励基建。工程节奏上我用编排先拿业务结果、沉淀评测集，等环境成熟再 RL 化——评测集就是未来 RL 的奖励基建，两步走不冲突。"</div>
<div class="iv">被问"怎么评估报告质量"｜"两层：fact 层——把报告拆成 claim 逐条对证据核验（数字双源一致率）；report 层——rubric 评估结构完整性、覆盖度、口径一致性。这正是 BrowseComp'难找易验'原则的应用。"</div>
<h2>九、高频追问清单</h2>
<ul class="pts deep">
<li>并行度怎么定？——按数据源配额 + 成本预算动态调整；避免打爆上游接口（对应你的限流经验）。</li>
<li>某一路数据源挂了怎么办？——降级策略：标注数据缺口继续跑，还是等待重试？由结论关键性决定。</li>
<li>子问题拆解错了怎么办？——规划器输出先过一遍"拆解合理性"自检 + 允许执行中重规划。</li>
<li>报告长度与上下文窗口的矛盾？——分节生成 + 证据句柄化（文件系统当上下文）。</li>
<li>和通义/昆仑万维这些开源 deep research 的差距？——开源模型给的是能力上限参照，企业场景的核心壁垒在私有数据源接入与校验规则，这恰好是你方案的重点。</li>
</ul>
"""

c1 = page("民生保险：知识库问答 + 佣金问答 + 意图匹配（保单变更识别 + 规则校验）", case1_body)
c2 = page("金融 DeepResearch：多路并行取数 + 结果校验 + 问答报告链路", case2_body)

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
