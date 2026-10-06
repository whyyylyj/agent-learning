/* 页面模块：总览 / 国金真题主线 / 编码题 / 冲刺速查 */
(function(){
const M = window.GJ_MODULES = window.GJ_MODULES || [];
/* app.js 在本文件之后加载，故惰性解析帮助函数（调用时 app.js 已就绪） */
const C = (...a) => window.GJ_checkbox(...a);
const PROG = () => window.GJ_progressCards();

/* ---------- 总览（放到最前） ---------- */
const overview = {
  id: "overview", icon: "🎯", name: "总览与答题心法", type: "page",
  desc: "",
  pageItems: ["ov-formula","ov-principle","ov-habits","ov-start"],
  page(){
    return `<div>
  <div class="page-hero">
    <h1>佣金宝后端面试作战室</h1>
    <p>目标岗位：国金证券 · 佣金宝 App · Java 后端开发。本站由你的国金调研资料库（yjb 12 篇）+ 互联网检索整理而成，🔴 标记的题目全部来自牛客可核验的国金真实面经。</p>
    <div class="hero-chips"><span>8 年经验版话术</span><span>两份已核验面经</span><span>${M.length - 1} 大知识模块</span><span>学习 / 自测双模式</span><span>进度本地保存</span></div>
  </div>
  ${PROG()}
  <div class="chain-box">
    <h2>🧠 8 年经验答题公式：C · R · E · W</h2>
    ${C("ov-formula","我已理解并能运用 CREW 公式：每个回答按四层展开")}
    <p>普通候选人背八股，资深候选人<b>用框架输出判断</b>。每道题按这四层说，面试官听到的是眼界和深度：</p>
    <table class="tbl">
      <thead><tr><th>层</th><th>说什么</th><th>例子（答「索引失效」）</th></tr></thead>
      <tbody>
        <tr><td><b>C 结论</b><br>Conclusion</td><td>先给判断，30 秒内说清立场，不绕</td><td>「失效本质是两种物理原因，不是背规则」</td></tr>
        <tr><td><b>R 原理</b><br>Root cause</td><td>讲机制和为什么，点到关键细节（露一手但不倒内存）</td><td>「索引存的是原始值的序，函数算完就对不上了」</td></tr>
        <tr><td><b>E 实战</b><br>Experience</td><td>1 个真实锚点：项目 / 事故 / 数字</td><td>「我们那条候选人搜索的 LIKE，我是抽字段+ES 分工解的」</td></tr>
        <tr><td><b>W 权衡</b><br>Weighing</td><td>什么场景我会反过来选 + 生产化边界与指标</td><td>「小结果集 != 也可能走索引，最终以 EXPLAIN ANALYZE 为准」</td></tr>
      </tbody>
    </table>
    <h3>让面试官眼前一亮的四个习惯</h3>
    ${C("ov-principle","我能说出四个「眼前一亮」习惯并已在答案中练习")}
    <ul>
      <li><b>主动暴露风险</b>：讲完方案主动说「我项目的这块有 X 风险，我的改进计划是……」——知道风险的人才是真的懂。</li>
      <li><b>量化一切</b>：不说「优化了很多」，说「20 秒到 100ms，口径是同模型压测」。</li>
      <li><b>讲反例和边界</b>：主动说「在什么条件下我会选相反方案」「这个结论不适用于……」。</li>
      <li><b>挂业务后果</b>：技术决策连着钱——「超时说失败会诱导重复委托，这是资金事故」。</li>
    </ul>
    <h3>使用方法</h3>
    ${C("ov-habits","我已熟悉学习/自测模式切换和进度勾选")}
    <ul>
      <li><b>学习模式</b>：完整展示话术；<b>自测模式</b>：先遮住答案自己说，再对照——建议最后三天全用自测模式。</li>
      <li>每张卡片右上角 <b>✓ 勾选「已掌握」</b>，侧边栏和本页实时显示进度。掌握标准（资料原文）：不背名词，每题都能答出原理、项目实现、边界风险、改进与验证。</li>
      <li>顶部搜索框可跨全站搜题；「国金真题」卡片优先刷。</li>
      <li>⚠️ 所有涉及「我做过」的话术锚点（萝卜投资、私行项目、AI 系统、Fury）都必须与你简历口径一致，不一致的先改简历或改话术。</li>
    </ul>
    ${C("ov-start","我今天就开始：先刷 🔴 国金真题模块")}
  </div>
  <div class="chain-box">
    <h2>🗺️ 国金面试考察方式（两份真实面经的共同模式）</h2>
    <div class="chain-flow">候选人简历中的项目/关键词
  ↓ 先问业务背景与具体实现
  ↓ 追问底层原理
  ↓ 追问替代方案和边界
  ↓ 要求给出项目实践证据</div>
    <p>结论：<b>项目先于八股，追问深于广度</b>。把「我项目里怎么用的 + 我知道它的边界」练成本能，比多背五十道八股有用。不同候选人问题差异很大，业务方向接受度和稳定性也是考察项。</p>
  </div>
</div>`;
  }
};
M.unshift(overview);

/* ---------- 国金真题主线 ---------- */
const real = {
  id: "real", icon: "🔴", name: "国金真题主线演练", type: "page",
  desc: "",
  pageItems: [],
  page(){
    return `<div>
  <div class="page-hero">
    <h1>🔴 国金真题主线演练</h1>
    <p>来源：牛客《国金证券 Java 面经》2024-05（社招，DayDreamerw）+《国金证券 Java 实习面经（offer）》（栀枊）。两份均为可核验原帖。这一页按原帖追问顺序串起全部真题，用于「面经原教旨」演练。</p>
  </div>
  <div class="chain-box">
    <h2>主线一：社招 Java 面经（2024-05）追问链</h2>
    <div class="chain-flow">项目开场（2 分钟介绍 → 十个项目事实）
  ↓
JWT 原理 → 登录传输安全 → 密码存储 → Token 风险
  ↓
Bean 生命周期 → BeanPostProcessor → AOP 代理
  ↓
循环依赖 → 三级缓存 → AOP 早期代理 → 如何消除
  ↓
项目 AOP → 代理机制 → 自调用 → 实际价值
  ↓
MySQL → 索引 → 聚簇索引 → 慢查询 → 失效 → 项目实践</div>
    <h3>按顺序演练（点击直达）</h3>
    <div class="chain-links">
      <a href="#/spring/sp-jwt">① JWT 工作原理</a>
      <a href="#/spring/sp-login-sec">② 登录安全（MD5 吗）</a>
      <a href="#/spring/sp-bean">③ Bean 生命周期</a>
      <a href="#/spring/sp-circular">④ 循环依赖三级缓存</a>
      <a href="#/spring/sp-aop">⑤ 项目 AOP 使用</a>
      <a href="#/mysql/my-btree">⑥ MySQL 了解 / B+Tree</a>
      <a href="#/mysql/my-cluster">⑦ 单列 vs 主键 / 聚簇索引</a>
      <a href="#/mysql/my-invalid">⑧ 索引失效</a>
      <a href="#/mysql/my-slow">⑨ 慢查询优化</a>
      <a href="#/mysql/my-composite">⑩ 索引实践（订单表）</a>
    </div>
    <h3>准备标准（资料原文）</h3>
    <p>准备标准不是背出名词，而是每题都能回答：<b>① 原理是什么 ② 当前项目具体怎么实现 ③ 当前实现有哪些边界或风险 ④ 如果改进为什么这样改 ⑤ 如何用测试或指标证明有效</b>。</p>
  </div>
  <div class="chain-box">
    <h2>主线二：实习面经（AI Agent 方向）追问漏斗</h2>
    <div class="chain-flow">为什么做（背景与价值）
  ↓ 怎么从需求做到上线（六阶段）
  ↓ 这个系统到底诊断什么（边界）
  ↓ 结果为什么可信（幻觉治理）
  ↓ RAG 之外还能做什么
  ↓ 长上下文怎么处理（压缩）
  ↓ 三层上下文如何装配与溢出</div>
    <h3>按顺序演练</h3>
    <div class="chain-links">
      <a href="#/ai/ai-why">① 做这个 Agent 的背景</a>
      <a href="#/ai/ai-how">② 从需求到落地</a>
      <a href="#/ai/ai-boundary">③ 诊断 bug 吗 / Agent vs Workflow</a>
      <a href="#/ai/ai-hallucination">④ 怎么减少幻觉</a>
      <a href="#/ai/ai-beyond-rag">⑤ 除了 RAG 还有什么</a>
      <a href="#/ai/ai-context">⑥ 上下文压缩</a>
      <a href="#/ai/ai-context3">⑦ 三层上下文与溢出</a>
      <a href="#/ai/ai-java">⑧ Java×AI：LLM 调用 30 秒线程会怎样</a>
    </div>
    <p style="margin-top:10px">⚠️ 注意：AI 题来自候选人简历，是「简历驱动追问」的证据——你的简历里有 AI 系统，这条主线对你大概率触发。</p>
  </div>
  <div class="chain-box">
    <h2>主线三：模拟追问 40 连（原题衍生的高概率追问）</h2>
    <p>以下不是已核验原题，是按国金追问风格生成的高概率问题，用于压力演练。全部来自资料 09/10 篇。</p>
    <h3>JWT 链</h3>
    ${C("r-jwt1","JWT 三段分别是什么？Payload 能放密码吗？")} ${C("r-jwt2","HS256 和 RS256 区别？密钥怎么管理？")}
    ${C("r-jwt3","Token 放 localStorage 有什么风险？如何实现退出和主动失效？")} ${C("r-jwt4","角色变更如何及时生效？Access/Refresh 怎么设计？JWT 被盗如何发现？")}
    <h3>Spring 链</h3>
    ${C("r-sp1","@PostConstruct 与构造器的顺序？BeanPostProcessor 做什么？")} ${C("r-sp2","AOP 代理什么时候创建？为什么构造器循环依赖解决不了？")}
    ${C("r-sp3","有 AOP 时早期引用为什么复杂？Boot 2.7 对循环依赖默认策略？")} ${C("r-sp4","项目中真有循环依赖吗？如何从设计上消除？")}
    <h3>AOP 链</h3>
    ${C("r-aop1","Filter、Interceptor、AOP 区别？JDK 代理和 CGLIB 区别？")} ${C("r-aop2","为什么自调用失效？private/final 方法能否被代理？")}
    ${C("r-aop3","审计切面该不该打印参数？切面异常影响主流程吗？审计与事务的顺序？")}
    <h3>MySQL 链</h3>
    ${C("r-my1","B+Tree 为什么适合数据库？二级索引叶子存什么？")} ${C("r-my2","回表和覆盖索引？为什么主键不宜太宽？")}
    ${C("r-my3","联合索引顺序怎么定？范围后的列一定无效吗？")} ${C("r-my4","LIKE '%x%' 怎么优化？慢 SQL 如何拿到并验证？当前项目哪条 SQL 可优化？")}
    <h3>Agent 链</h3>
    ${C("r-ai1","为什么是 Agent 不是 Workflow？停止条件是什么？")} ${C("r-ai2","工具调用失败怎么重试？总超时和成本预算怎么控？")}
    ${C("r-ai3","文档怎么切块？召回率和答案正确率的区别？")} ${C("r-ai4","日志里有 Prompt Injection 怎么办？Agent 怎么防越权读数据？")}
    ${C("r-ai5","评测集怎么来、怎么防泄漏？哪个指标达标才能自动执行？")}
  </div>
</div>`;
  }
};
M.push(real);

/* ---------- 编码题 ---------- */
const coding = {
  id: "coding", icon: "💻", name: "编码题清单", type: "page",
  desc: "",
  pageItems: ["cd-check","cd-conc","cd-sql"],
  page(){
    return `<div>
  <div class="page-hero">
    <h1>💻 编码题清单</h1>
    <p>重要结论：公开渠道没有可核验的「国金出过的 LeetCode 原题」——两份真实面经都没考算法，2022 年笔试帖是「20 道 Spring Boot 选择题」。券商技术面风格是项目+八股驱动。<b>刷题投入 ≤ 30%，其余给项目和八股。</b>以下清单按证据推断分级。</p>
  </div>
  <div class="chain-box">
    <h2>第一优先：资料明确建议的题型（映射到题号）</h2>
    <table class="tbl">
      <thead><tr><th>题型</th><th>LeetCode</th><th>要点</th></tr></thead>
      <tbody>
        <tr><td>LRU Cache</td><td><a href="https://leetcode.cn/problems/lru-cache/" target="_blank">146</a></td><td>哈希+双向链表 O(1)；能讲清缓存淘汰场景</td></tr>
        <tr><td>合并区间（交易日历）</td><td><a href="https://leetcode.cn/problems/merge-intervals/" target="_blank">56</a></td><td>排序后线性合并</td></tr>
        <tr><td>Top K</td><td><a href="https://leetcode.cn/problems/kth-largest-element-in-an-array/" target="_blank">215</a> / <a href="https://leetcode.cn/problems/top-k-frequent-elements/" target="_blank">347</a> / <a href="https://leetcode.cn/problems/merge-k-sorted-lists/" target="_blank">23</a></td><td>堆 O(nlogk) vs 快选 O(n)；讲流式场景（行情涨幅榜）</td></tr>
        <tr><td>生产者消费者</td><td><a href="https://leetcode.cn/problems/design-bounded-blocking-queue/" target="_blank">1188(会员)</a></td><td>阻塞队列、锁/条件变量、优雅退出</td></tr>
        <tr><td>并发打印系列</td><td><a href="https://leetcode.cn/problems/print-in-order/" target="_blank">1114</a> / <a href="https://leetcode.cn/problems/print-foobar-alternately/" target="_blank">1115</a> / <a href="https://leetcode.cn/problems/print-zero-even-odd/" target="_blank">1116</a> / <a href="https://leetcode.cn/problems/building-h2o/" target="_blank">1117</a></td><td>Semaphore / CAS自旋 / synchronized+wait-notify 三种写法</td></tr>
        <tr><td>限流器 / 日志去重</td><td><a href="https://leetcode.cn/problems/logger-rate-limiter/" target="_blank">359</a> / <a href="https://leetcode.cn/problems/design-hit-counter/" target="_blank">362(会员)</a></td><td>滑动窗口+时间分桶；配合手写令牌桶</td></tr>
        <tr><td>SQL 窗口函数</td><td>—</td><td>每账户最近 N 笔（ROW_NUMBER）、找重复 requestId、状态超时统计</td></tr>
      </tbody>
    </table>
  </div>
  <div class="chain-box">
    <h2>第二优先：券商 Java 通用高频 / 第三优先：证券业务应景</h2>
    <p><b>通用高频（挑 6-8 道保持手感）</b>：<a href="https://leetcode.cn/problems/reverse-linked-list/" target="_blank">206 反转链表</a> · <a href="https://leetcode.cn/problems/two-sum/" target="_blank">1 两数之和</a> · <a href="https://leetcode.cn/problems/merge-two-sorted-lists/" target="_blank">21 合并有序链表</a> · <a href="https://leetcode.cn/problems/linked-list-cycle/" target="_blank">141/142 环形链表</a> · <a href="https://leetcode.cn/problems/longest-substring-without-repeating-characters/" target="_blank">3 无重复字符</a> · <a href="https://leetcode.cn/problems/maximum-subarray/" target="_blank">53 最大子数组和</a> · <a href="https://leetcode.cn/problems/merge-sorted-array/" target="_blank">88 合并有序数组</a> · <a href="https://leetcode.cn/problems/binary-tree-level-order-traversal/" target="_blank">102 层序遍历</a> · <a href="https://leetcode.cn/problems/min-stack/" target="_blank">155 最小栈</a> · <a href="https://leetcode.cn/problems/binary-search/" target="_blank">704 二分</a> · <a href="https://leetcode.cn/problems/3sum/" target="_blank">15 三数之和</a> · <a href="https://leetcode.cn/problems/sort-an-array/" target="_blank">912 手撕排序</a></p>
    <p><b>证券业务应景（会 121/122 即可）</b>：<a href="https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/" target="_blank">121/122 买卖股票系列</a> · <a href="https://leetcode.cn/problems/sliding-window-maximum/" target="_blank">239 滑动窗口最大值（K线最高价）</a> · <a href="https://leetcode.cn/problems/find-median-from-data-stream/" target="_blank">295 数据流中位数（行情中位数）</a></p>
  </div>
  <div class="chain-box">
    <h2>现场编码纪律</h2>
    ${C("cd-check","我能复述现场编码检查清单")}
    <ul>
      <li>先复述输入、输出和边界，再动手；</li>
      <li>给简单正确解，再优化；写清复杂度；</li>
      <li>空值、溢出、重复、极端规模过一遍；</li>
      <li><b>金额不用 double</b>；并发题说明线程安全范围；SQL 说明索引和数据规模；</li>
      <li>至少口述 3 个测试用例收尾。</li>
    </ul>
    <h3>并发手写样板：生产者消费者（wait/notify 版）</h3>
    ${C("cd-conc","我能白板默写生产者消费者（wait/notify 与 Condition 两版）")}
    <pre>class BoundedBuffer&lt;T&gt; {
  private final Queue&lt;T&gt; buf = new ArrayDeque&lt;&gt;();
  private final int cap;
  BoundedBuffer(int cap){ this.cap = cap; }
  public synchronized void put(T t) throws InterruptedException {
    while (buf.size() == cap) wait();      // while 不是 if：防虚假唤醒
    buf.add(t); notifyAll();               // notifyAll 防丢失唤醒
  }
  public synchronized T take() throws InterruptedException {
    while (buf.isEmpty()) wait();
    T t = buf.poll(); notifyAll();
    return t;
  }
}</pre>
    <p>考点延伸：为什么 while 不是 if（虚假唤醒）；notifyAll vs notify（丢失唤醒）；Condition 版本写法；语义升级——「队列满时 put 拒绝还是阻塞」由业务定，下单场景宁可快速失败进降级。</p>
    <h3>SQL 手写样板：每账户最近 N 笔订单</h3>
    ${C("cd-sql","我能白板写窗口函数 SQL 并解释索引需求")}
    <pre>SELECT * FROM (
  SELECT o.*, ROW_NUMBER() OVER (
    PARTITION BY account_id ORDER BY created_at DESC, id DESC
  ) AS rn FROM orders o WHERE biz_date = :bizDate
) t WHERE t.rn &lt;= 3;
-- 说明：联合索引 (biz_date, account_id, created_at, id) 匹配过滤与排序</pre>
  </div>
</div>`;
  }
};
M.push(coding);

/* ---------- 冲刺速查 ---------- */
const sprint = {
  id: "sprint", icon: "⚡", name: "冲刺与速查清单", type: "page",
  desc: "",
  pageItems: ["s30-prod","s30-biz","s30-tech","s30-design","s30-story","s30-ask","story1","story2","story3","d1","d2","d3","d4","d5","d6","d7"],
  page(){
    return `<div>
  <div class="page-hero">
    <h1>⚡ 冲刺与速查清单</h1>
    <p>面试前 30 分钟速查 + 7 天冲刺计划。全部来自资料 06/08 篇，按勾选清单使用。</p>
  </div>
  <div class="chain-box">
    <h2>面试前 30 分钟速查</h2>
    <h3>产品（3 分钟）</h3>
    ${C("s30-prod","佣金宝定位（账户+交易+财富）、近期版本方向、后端四难点、App 后端≠撮合")}
    <h3>证券业务（5 分钟）</h3>
    ${C("s30-biz","委托受理≠申报≠成交；部成/撤单只撤未成；超时=未知先查询；可用≠可取；基金异步确认；适当性留痕；对账兜底")}
    <h3>技术（8 分钟）</h3>
    ${C("s30-tech","幂等三件套（clientRequestId+唯一约束+返回原结果）；状态机+version；Outbox+幂等+对账；Cache Aside；MQ 四件套；总 deadline；故障域隔离；先证据后调参；鉴权防重放脱敏审计")}
    <h3>系统设计（5 分钟）</h3>
    ${C("s30-design","澄清边界与规模 → API与业务状态 → 主链路与权威源 → 数据与一致性 → 超时/重复/乱序 → 容量热点降级容灾 → 安全审计指标演进")}
    <h3>个人故事（5 分钟）× 反问（4 分钟）</h3>
    ${C("s30-story","三个故事（复杂模块/性能/故障）各有背景-动作-指标-取舍-反思，数字口径一致")}
    ${C("s30-ask","反问 3 个：岗位业务线 / 当前技术挑战 / 新人 3 个月成功标准")}
  </div>
  <div class="chain-box">
    <h2>⚠️ 红线（说了就扣分）</h2>
    <table class="tbl">
      <thead><tr><th>不要这样说</th><th>改成</th></tr></thead>
      <tbody>
        <tr><td>下单接口 200 就成功了</td><td>HTTP 成功和业务状态分开表达</td></tr>
        <tr><td>超时就重试三次</td><td>副作用请求先幂等和查询确认</td></tr>
        <tr><td>Redis 分布式锁绝对安全</td><td>锁是协调手段，唯一约束/版本才是防线</td></tr>
        <tr><td>MQ 保证 exactly-once</td><td>业务副作用仍需幂等和对账</td></tr>
        <tr><td>所有 A 股都 T+1</td><td>按市场、品种和业务规则确认</td></tr>
        <tr><td>上两地三中心就高可用</td><td>先按系统分级定义 RTO/RPO 并演练</td></tr>
        <tr><td>国金内部肯定用了 Kafka</td><td>公开资料未确认；说明自己的候选设计</td></tr>
        <tr><td>我参与了优化</td><td>说明你做的动作、证据和结果</td></tr>
      </tbody>
    </table>
  </div>
  <div class="chain-box">
    <h2>🗓️ 7 天冲刺计划（可按剩余天数压缩）</h2>
    <p>原则：🔴 真题 > 高频八股 > 系统设计 > 扩展题；每天产出是「能脱稿讲」，不是「看过」。</p>
    <table class="tbl">
      <thead><tr><th>天</th><th>主题</th><th>产出验收</th></tr></thead>
      <tbody>
        <tr><td>D1</td><td>🔴 国金真题主线一：JWT + 登录安全 + Spring 三连</td><td>自测模式下 10 张卡片全部脱稿</td></tr>
        <tr><td>D2</td><td>🔴 MySQL 五连 + 你项目的索引/N+1 实践</td><td>白板写出订单表索引设计并逐列解释</td></tr>
        <tr><td>D3</td><td>证券业务地图 + ⛏️ 深挖追问链（幂等悬挂 / 部分成交×撤单 / 跨资源事务 / 回报剧场）</td><td>深挖链只看母题能自己推演四层；业务闭卷自测 10 题全对</td></tr>
        <tr><td>D4</td><td>🔴 AI 主线七连 + LLM 工程化追问</td><td>七层漏斗脱稿 + 幻觉五层框架默写</td></tr>
        <tr><td>D5</td><td>系统设计三题 + 🔧 实操演练场（白板五题 / 事故剧本 / SQL 诊疗 / 数字防守）</td><td>三道设计题各 8 分钟讲完；白板五题能默写骨架+口述三句话</td></tr>
        <tr><td>D6</td><td>项目表达：自我介绍 + STAR+R + 简历防守自查</td><td>录音回听自我介绍，数字口径全一致</td></tr>
        <tr><td>D7</td><td>编码题热身 + 全站自测模式过一遍 + 速查清单</td><td>总进度 ≥ 90%，红线表默写</td></tr>
      </tbody>
    </table>
    ${C("d1","D1 真题主线一完成")} ${C("d2","D2 MySQL 主线完成")} ${C("d3","D3 证券业务完成")} ${C("d4","D4 AI 主线完成")} ${C("d5","D5 系统设计完成")} ${C("d6","D6 项目表达完成")} ${C("d7","D7 冲刺复盘完成")}
  </div>
  <div class="chain-box">
    <h2>面试后 30 分钟复盘模板</h2>
    <ul>
      <li>问题（尽量还原原话）/ 我的回答主线 / 面试官追问（真正关注点）/ 缺口类型（知识/表达/项目证据/业务）/ 查证后的正确答案 / 下次的一句话版本。</li>
      <li>只修复<b>重复出现</b>或岗位高度相关的问题，不因一次冷门题打乱全部计划。</li>
    </ul>
  </div>
</div>`;
  }
};
M.push(sprint);
})();
