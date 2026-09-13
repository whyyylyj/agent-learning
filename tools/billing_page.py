# -*- coding: utf-8 -*-
"""实战案例三：Agent 平台计费系统（预付费点数 · 次数+流量双维 · API 倍数体系）"""
import os
BASE = os.environ.get("KB_SITE") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

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
"""

BODY = """
<div class="catline"><span class="chip" style="background:#1e3a8a">实战案例 3 · 平台工程 / 商业化</span></div>
<h1>Agent 平台计费系统：充值点数预付费 × 次数 + 流量双维计费 × API 倍数体系</h1>

<h2>一、场景与计费模型（先把商业问题说清）</h2>
<p><b>业务背景：</b>AI 应用平台把问答、RAG 检索、文档解析、报告生成等 agent 能力以 API 形式开放给 B 端客户（保险公司 / 券商等）。算力有真金白银的成本，能力不能白用——需要一套<b>可运营的计量计费体系</b>，并且是<b>预付费</b>：客户先充值点数，后消费，杜绝后付费的坏账风险。</p>
<p><b>计费模型一句话：</b></p>
<div class="iv"><b>本次扣点 = API 倍数 ×（调用基础点 + 流量点）</b>，其中 流量点 = 输入 token × 输入费率 + 输出 token × 输出费率（输出更贵）；非 LLM 类 API 的"流量"按字节数 / 文档页数折算成等价点。<br>调用基础点保底（覆盖一次调用的固定开销），流量点按量浮动——<b>次数 + 流量双维</b>：纯按次对重查询亏、纯按 token 对轻查询不友好，双维 + 保底是两者平衡。</div>
<p><b>倍数体系（每个 API 一个倍数，定价的调参旋钮）：</b>倍数不是拍脑袋，是三个维度的乘积：</p>
<table class="sel">
<tr><th>维度</th><th>示例</th><th>设计理由</th></tr>
<tr><td><b>API / 链路复杂度</b></td><td>单轮问答 1.0 · RAG 检索问答 2.0 · 保单变更（抽取+规则）3.0 · DeepResearch 报告 8.0</td><td>多轮多工具的长链路消耗成倍增长（Anthropic 复盘：多智能体 15× token），倍数反映真实成本结构</td></tr>
<tr><td><b>模型档位</b></td><td>小模型 0.3× · 旗舰模型 1.0×</td><td>意图路由把简单请求分给小模型，客户账单直接打折——路由策略与计费联动</td></tr>
<tr><td><b>SLA / 优先级档</b></td><td>标准队列 1.0× · 优先队列 1.5×</td><td>为高峰期资源抢占定价：加钱插队，用价格杠杆调需求</td></tr>
</table>
<div class="callout"><b>面试一句话：</b>倍数体系 = 把"成本结构"翻译成"价格结构"的 DSL。调价不改代码，配置中心改倍数、灰度生效——运营与工程解耦。</div>

<h2>二、架构设计（一次计费请求的完整生命周期）</h2>
<div class="arch">
<div class="layer l1"><b>① 接入网关（计费切面）</b> ｜ 鉴权 → 租户路由 → 计费前置拦截（统一入口，业务服务无感知）</div>
<div class="arrow">↓</div>
<div class="layer l2"><b>② 预检与冻结</b> ｜ 查余额 → 不足拒付（402）→ 按"预估最大用量 × 倍数"<b>预冻结点数</b>（两阶段第一步）</div>
<div class="arrow">↓</div>
<div class="layer l3a"><b>③ 能力调用</b> ｜ LLM / RAG / 工具链执行；网关透传 request_id（幂等键）贯穿全程</div>
<div class="arrow">↓</div>
<div class="layer l3b"><b>④ 用量回传</b> ｜ LLM：usage（prompt/completion tokens，流式在末 chunk）；非 LLM：字节 / 页数折算</div>
<div class="arrow">↓</div>
<div class="layer l3c"><b>⑤ 结算（两阶段第二步）</b> ｜ 实测扣点 = 倍数 ×（基础点 + 流量点）→ 与冻结额比对，<b>多退少补</b>；失败请求按策略退回</div>
<div class="arrow">↓</div>
<div class="layer l4"><b>⑥ 异步落账</b> ｜ 扣减流水（append-only，带幂等键）→ 日 / 月账单聚合 → 定时对账（流水 Σ vs 余额变动 diff = 0）</div>
</div>

<h2>三、核心机制设计（工程难点逐个击破）</h2>
<ul class="pts">
<li><b>账户模型：</b>租户 → 钱包（点数余额）→ 三本流水（充值 / 冻结 / 扣减），全部 append-only。充值走"待确认户"，支付回调确认后才进可用余额。</li>
<li><b>两阶段冻结-结算：</b>预冻结按"预估 max token × 倍数"（防超卖），结算按实测 usage（公平）。预估不准的极端长请求触发<b>分段补冻</b>：用量过半且余额不足以覆盖预估时，中途补冻结一次。</li>
<li><b>幂等设计：</b>request_id 是唯一幂等键，冻结、结算、退回三步都带。客户端重试 / 网关重试 / MQ 重投都不会重复扣点。</li>
<li><b>并发扣减：</b>Redis Lua 脚本原子完成"校验余额 + 冻结/扣减"（单线程语义天然防并发穿透），成功后异步落 MySQL；DB 是账本、Redis 是热路径。T+1 对账任务兜底两者不一致。</li>
<li><b>冻结泄漏治理：</b>进程崩溃会留下"冻而未结"的悬挂冻结——每笔冻结带 TTL，补偿任务扫描过期冻结自动解冻退回。</li>
<li><b>倍数热更新：</b>倍数与费率放配置中心（Nacos），网关监听推送秒级生效；改价先灰度一个租户观察账单波动，再全量——<b>计费配置的错误直接是资损</b>，按发布纪律对待（校验非负、上下限、审批）。</li>
<li><b>欠费与预警：</b>余额 &lt; 单次预估均值 × N 时推送预警（租户 + 销售）；归零后<b>软停</b>——拒绝新请求、进行中的请求完成结算，不硬杀。</li>
<li><b>计量双通道：</b>信任下游 usage（准）+ 网关侧按输入字数估算（兜底），差异超阈值告警——usage 缺失时用估算并打"估算计费"标记，账单可解释。</li>
</ul>

<h2>四、技术选型与取舍</h2>
<table class="sel">
<tr><th style="width:120px">决策点</th><th style="width:170px">最终选择</th><th style="width:160px">被否方案</th><th>取舍理由</th></tr>
<tr><td>扣减一致性</td><td><b>Redis 原子预扣 + 异步落库 + 对账</b></td><td>DB 行锁 / SELECT FOR UPDATE</td><td>计费在网关热路径，QPS 高时行锁串行化成为瓶颈；最终一致 + append-only 流水 + 对账兜底，兼顾吞吐与资金正确性。</td></tr>
<tr><td>计费位置</td><td><b>网关统一切面</b></td><td>各能力服务自报用量</td><td>切面对业务零侵入、口径统一、倍数一处生效；服务自报会漂移出 N 套计费逻辑，口径无法对账。</td></tr>
<tr><td>冻结策略</td><td><b>按预估 max 冻结 + 分段补冻</b></td><td>不冻结 / 全额冻结</td><td>不冻结会超卖（并发穿透出负余额）；全额冻结伤体验（余额被大预估占满，轻请求发不出）。预估冻结 + 过半补冻是折中。</td></tr>
<tr><td>计费粒度</td><td><b>次数保底 + token 阶梯</b></td><td>纯按次 / 纯按 token</td><td>纯按次对 DeepResearch 类重链路亏本；纯按 token 对高频轻查询劝退。基础点保底覆盖固定开销，流量点按量付费。</td></tr>
<tr><td>预付费 vs 后付费</td><td><b>预付费点数</b></td><td>月度后付费账单</td><td>B 端坏账风险 + 用量弹性大；点数预付现金流好、超卖风险锁定在"已充额度"内，欠费即停的边界清晰。</td></tr>
<tr><td>倍数管理</td><td><b>配置中心 + 灰度</b></td><td>代码常量 / DB 手改</td><td>调价是运营动作，频率高于发版；灰度 + 审批 + 快速回滚把配错资损半径压到最小。</td></tr>
</table>

<h2>五、异常 case 集（计费系统的试金石）</h2>
<div class="iv"><b>① 重复回调 / 重试重复扣费</b>｜客户端超时重发、MQ 重投 → 同一 request_id 再次到达。<b>解：</b>幂等键贯穿冻结-结算-退回三步，重复请求返回首次结果快照。</div>
<div class="iv"><b>② 冻结后进程崩溃</b>｜预冻结成功、结算没来得及跑 → 点数被永久占住。<b>解：</b>冻结带 TTL + 补偿任务扫描过期悬挂冻结自动解冻；客户无感。</div>
<div class="iv"><b>③ 网关超时但下游实际成功</b>｜响应没回来但 LLM 已消耗 → 不扣是平台亏、照扣客户投诉。<b>解：</b>以实测 usage 为准结算（用量回传与响应解耦）；极端场景进人工仲裁队列，账单可修正。</div>
<div class="iv"><b>④ usage 缺失</b>｜第三方 API 偶发不返回 usage 字段。<b>解：</b>网关侧按输入字数 × 经验系数估算，账单打"估算计费"标记，事后可复核——宁可标记不可瞎扣。</div>
<div class="iv"><b>⑤ 并发穿透负余额</b>｜多请求同时通过余额检查。<b>解：</b>Redis Lua 原子扣减消灭检查-扣减间隙；允许 ≤ 单次预估的小额负值（结算滞后），超阈值风控熔断。</div>
<div class="iv"><b>⑥ 倍数配置事故</b>｜新 API 倍数误配 0 / 负数 → 免费调用资损。<b>解：</b>配置校验（非负、上下限、与同链路 API 离散度检查）+ 灰度租户先行 + 一键回滚；对账任务发现"零扣点高调用"异常即告警。</div>
<div class="iv"><b>⑦ 充值回调乱序</b>｜重复充值回调 / 掉单。<b>解：</b>充值进待确认户，支付平台回调确认后入可用余额；回调幂等 + 掉单主动查证任务。</div>

<h2>六、与论文 / 工业界的映射</h2>
<table class="tbl">
<tr><th>参照</th><th>落点</th></tr>
<tr><td><a href="../papers/longcat-flash.html">⑭ LongCat-Flash</a></td><td>零计算专家 = 模型层降本；计费倍数 = 把降本传导给客户的定价层。两层配合才有"单位成本下降【占位：__%】"的商业闭环。</td></tr>
<tr><td><a href="../papers/mem0-long-term-memory.html">⑦ Mem0</a></td><td>记忆压缩 p95 −91% token → 直接变成客户账单上的流量点节省。计费系统是上下文工程收益的"计价器"。</td></tr>
<tr><td><a href="../papers/anthropic-multi-agent-research-system.html">③ 多智能体复盘</a></td><td>token 用量解释 80% 成本方差、15× 消耗 → DeepResearch 类 API 倍数定 8.0 的成本依据；倍数表要和成本观测对得上。</td></tr>
<tr><td><a href="../chapters/ch9.html">第 9 章 · 框架</a></td><td>Dify / Coze 的 credit 与套餐体系同构；OpenAI / Bedrock 的 token 计费（输入输出分价、batch 半价）是业界口径参照——自家费率对齐厂商口径，账单才能互查。</td></tr>
<tr><td><a href="case-finance-deepresearch.html">实战案例二</a></td><td>多路并行取数的成本预算（并发度 × 单价）最终都流经这套计费：预算控制点就在预检冻结这一步。</td></tr>
</table>

<h2>七、面试怎么讲（场景 → 话术）</h2>
<div class="iv">开场 60 秒｜"AI 平台对外商业化必须有计费。我设计的是预付费点数体系：客户充值点数，网关计费切面统一计量，扣点 = API 倍数 ×（调用基础点 + token 流量点），每个 API 的倍数反映链路复杂度、模型档位和 SLA。工程上最难的三件事：并发扣减防超卖（Redis 原子预扣 + 异步落账 + 对账）、两阶段冻结结算防悬挂（TTL 补偿解冻）、幂等防重复扣费（request_id 贯穿）——这套和支付系统的经典问题域完全同构。"</div>
<div class="iv">被问"为什么不直接按 token 计费"｜"纯 token 对高频轻量调用（意图分类、格式校验）单价过低覆盖不了调度开销；纯按次对 DeepResearch 重链路又亏。次数保底 + 流量按量 + 倍数调价，三个旋钮把成本结构翻译成价格结构，调价不动代码。"</div>
<div class="iv">被问"并发扣费怎么不超卖"｜"热路径全在 Redis Lua 里原子完成校验+扣减，单线程语义没有检查-扣减间隙；MySQL 只做账本异步落库，T+1 对账 diff 必须为零。宁可偶尔退回，不可超卖。"</div>
<div class="iv">被问"计费会不会拖慢请求"｜"计费切面在网关 P99 内只做一次 Redis 往返（冻结），结算和落账全异步。预检不足直接 402 快速失败，不打到下游——计费本身也要做过性能设计。"</div>

<h2>八、高频追问清单</h2>
<ul class="pts deep">
<li>点数和人民币怎么换算、怎么开发票？——充值即锁定汇率，账单双口径（点数 / 折算金额），发票按充值流水开。</li>
<li>怎么给销售 / 运营做优惠？——赠送点（营销户，单独流水、过期策略）+ 倍数活动价（限时倍数 0.8），不直接改余额，保证账务可解释。</li>
<li>客户投诉多扣了怎么查？——request_id 一键串联冻结 / 结算 / 退回三段流水 + 原始 usage，账单可回放。</li>
<li>怎么验证计费正确性？——对账三件套：流水 Σ = 余额变动；冻结余额 = 在途请求；零扣点高调用告警。上线前用流量回放做计费影子验证。</li>
<li>倍数怎么定才科学？——成本观测先行：按 API 统计 token / 算力 / 时长分布，倍数 = 目标毛利下的成本加成，定期校准（联动 ③ 的成本方差结论）。</li>
</ul>
"""


def build():
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Agent 平台计费系统：预付费点数 × 次数+流量 × API 倍数 - 实战案例</title>
<link rel="stylesheet" href="../assets/style.css"><style>{EXTRA}</style></head>
<body><div class="wrap">
<a class="back" href="../index.html">← 返回总览</a>
{BODY}
<div class="chapnav"><a class="pn" href="../index.html">目录</a><a class="pn" href="../cases/case-finance-deepresearch.html">← 上一章：金融 DeepResearch</a><a class="pn" href="../chapters/ch9.html">下一章：典型 Agent 开源框架 →</a><a class="pn" href="../cheatsheet.html">速查工具页 →</a></div>
<div class="foot">实战案例深度笔记 · Steven Li 面试准备知识库 · 待填真实数据见 <a href="../checklist.html">数据清单</a>（倍数表 / 费率 / 对账口径按真实项目替换）</div>
</div></body></html>"""
