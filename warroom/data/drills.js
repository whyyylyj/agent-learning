/* 模块：实操演练场 */
(function(){
const M = window.GJ_MODULES = window.GJ_MODULES || [];

M.push({
  id: "drills", icon: "🔧", name: "实操演练场",
  desc: "面试的实操环节三件套：白板编码、现场排障、口径防守。本模块全部按「考场还原」编写——每题给出可默写的骨架代码/剧本 + 写完后必须口述的三句话。事故剧本按真实时间线演练，练的是「先止血再定位」的肌肉记忆。",
  cards: [
    {
      id: "dr-code", q: "白板编码五题：骨架 + 考点 + 口述三句话", tags:["白板","编码"],
      scene: "券商 Java 面试的手撕题偏工程型：并发工具、限流、状态机、聚合编排，而不是纯算法。这五题覆盖最高频工程手写题，每题给可默写的最小骨架（考场写出这个程度就够了）。",
      script: [
        {t:"h", md:"题 1 · 带总 deadline 的并行聚合（资产页面的原型）"},
        {t:"code", text:"// 考点：总预算控制、隔离线程池、部分失败表达\nExecutorService pool = Executors.newFixedThreadPool(4); // 实际按下游隔离命名\nlong deadline = System.nanoTime() + TimeUnit.MILLISECONDS.toNanos(800);\nCompletableFuture<FundPos> fund = CompletableFuture.supplyAsync(this::queryFund, pool)\n        .orTimeout(400, TimeUnit.MILLISECONDS);\nCompletableFuture<EquityPos> eq = CompletableFuture.supplyAsync(this::queryEquity, pool)\n        .orTimeout(300, TimeUnit.MILLISECONDS);\nCompletableFuture<Quote> quote = CompletableFuture.supplyAsync(this::queryQuote, pool)\n        .orTimeout(150, TimeUnit.MILLISECONDS);\nlong remainMs = TimeUnit.NANOSECONDS.toMillis(deadline - System.nanoTime());\nCompletableFuture.allOf(fund, eq, quote)\n        .completeOnTimeout(null, remainMs, TimeUnit.MILLISECONDS)  // 总预算兜底\n        .join();\n// 组装时逐个判：完成→取值；异常→该模块标记「暂不可用」；超时未完成→标记「刷新中」\n// 绝不把缺失模块当 0 处理"},
        {t:"p", md:"写完必口述：① 三个子超时之和大于总预算是故意的——总预算是硬顶，子超时是理想值；② 每个异常单独 catch 成「模块降级」，一个失败不毁整页；③ 实际生产会再加：MDC 上下文传递、取消传播、按下游拆池。"},
        {t:"h", md:"题 2 · 令牌桶限流器（手写高频）"},
        {t:"code", text:"class TokenBucket {\n  private final long capacity;      // 桶容量（允许的突发）\n  private final double rate;        // 每秒生成令牌数\n  private double tokens;\n  private long lastRefillNanos;\n  TokenBucket(long capacity, double rate) {\n    this.capacity = capacity; this.rate = rate;\n    this.tokens = capacity; this.lastRefillNanos = System.nanoTime();\n  }\n  synchronized boolean tryAcquire(int n) {\n    long now = System.nanoTime();\n    tokens = Math.min(capacity, tokens + (now - lastRefillNanos) * rate / 1e9);\n    lastRefillNanos = now;\n    if (tokens >= n) { tokens -= n; return true; }\n    return false;                   // 快速失败，不等待\n  }\n}"},
        {t:"p", md:"写完必口述：① 懒惰补充——不靠定时线程，取令牌时按时间差补；② capacity 决定突发容忍，rate 决定均速，两者语义不同；③ 这个桶只在单机有效，全局限流要 Redis+Lua 或网关层做，单机桶是最后一道本地保护。"},
        {t:"h", md:"题 3 · 订单状态机的乐观锁更新（一行 SQL 定乾坤）"},
        {t:"code", text:"UPDATE orders\nSET status = :newStatus, version = version + 1, updated_at = NOW(3)\nWHERE order_id = :orderId\n  AND version = :expectedVersion\n  AND status IN (:allowedPrevStates);\n-- 影响行数判定：\n--   1 → 迁移成功\n--   0 → 读回记录：version 相同但 status 不在 allowed → 重复/迟到事件，幂等跳过\n--        version 更大 → 乱序事件，按重放策略处理\n--        无记录 → 数据异常，告警人工"},
        {t:"p", md:"写完必口述：① 「影响行数 0」不是失败而是信息——三分支处置；② 终态保护隐含在 allowedPrevStates 里（终态永远不在任何迁移的前置集合中）；③ 这行 SQL 同时解决并发、乱序、重复三类问题，是「状态机+版本」的落地形态。"},
        {t:"h", md:"题 4 · 幂等下单伪代码（含并发冲突分支）"},
        {t:"code", text:"Order placeOrder(PlaceCmd cmd) {\n  validate(cmd);                                    // 参数/归属校验\n  try {\n    idemRepo.insert(PENDING, cmd.accountId(), cmd.requestId(), now()); // 抢唯一约束\n  } catch (DuplicateKeyException e) {               // 并发重复请求\n    Order prev = idemRepo.load(cmd.accountId(), cmd.requestId());\n    if (prev.isFinal())   return prev.businessResult();            // 返回原结果\n    if (prev.isPending()) return OrderResponse.confirming(prev.queryUrl()); // 处理中\n    throw new ConflictException();                  // 状态异常，人工\n  }\n  order = orders.create(cmd);   // 同事务：幂等记录置 PROCESSING + 订单落库\n  try {\n    CounterResp r = counterGateway.submit(order);   // 调柜台（舱壁池+短超时）\n    order.transition(r.accepted() ? ACCEPTED : REJECTED, r.counterOrderId());\n  } catch (TimeoutException e) {\n    order.transition(CONFIRMING);  // 不是失败！后台任务按流水查柜台收敛\n  }\n  return order.businessResult();\n}"},
        {t:"p", md:"写完必口述：① catch DuplicateKey 不是异常路径而是==幂等的主路径之一==；② 超时转 CONFIRMING 而不是 FAILED——超时是未知态；③ 后台补偿任务扫描超时 CONFIRMING，按「悬挂治理」收敛（联动 ⛏️ 深挖模块 dd-order）。"},
        {t:"h", md:"题 5 · 三个线程循环交替打印（Semaphore 版最稳）"},
        {t:"code", text:"class Alternator {\n  private final Semaphore a = new Semaphore(1);\n  private final Semaphore b = new Semaphore(0);\n  private final Semaphore c = new Semaphore(0);\n  private final int n;\n  Alternator(int n) { this.n = n; }\n  Runnable A = () -> { for (int i=0;i<n;i++) { a.acquireUninterruptibly(); System.out.print(\"A\"); b.release(); } };\n  Runnable B = () -> { for (int i=0;i<n;i++) { b.acquireUninterruptibly(); System.out.print(\"B\"); c.release(); } };\n  Runnable C = () -> { for (int i=0;i<n;i++) { c.acquireUninterruptibly(); System.out.print(\"C\"); a.release(); } };\n}"},
        {t:"p", md:"写完必口述：① 信号量把「谁先谁后」变成结构而不是等待逻辑，比 wait/notify 版少一个状态变量；② 追问就现场背另外两版：synchronized+wait/notify（while 防虚假唤醒）、LockSupport.park/unpark（无锁对象）；③ 生产对应物：流水线交接、顺序消费的分区屏障。"}
      ],
      shine: ["五题全是「工程型手撕」——正是券商面（vs 互联网纯算法面）的风格","每题的「口述三句话」就是加分项本身：写完代码的那三十秒决定面试官对你的分层判断"]
    },
    {
      id: "dr-incident", q: "事故演练剧本：开盘 5 分钟下单 P99 从 80ms 飙到 3 秒", tags:["事故","应急","剧本"],
      scene: "主管面/二面的经典题：「开盘高峰下单突然变慢，说说你怎么办」。考的不是知识点是==处置节奏==——先止血还是先定位、什么时候升级、怎么对外沟通。按下面的时间线演练，练到 10 分钟能讲完。",
      script: [
        {t:"flow", text:"T+0min  告警：下单 P99 3s（基线 80ms），错误率 2%（多为超时），影响=全量用户\n   │ 第一个动作：查变更——昨夜有无发布/配置/扩缩容（人为变因最快排除）\n   ▼\nT+1min  快速分诊（三看）：\n   ① 入口量：QPS 是否超容量模型（洪峰 or 异常流量/重试风暴）\n   ② 依赖：柜台/DB/Redis/行情 谁的 P99 先恶化（trace 拆解：排队?应用?DB?下游?）\n   ③ 自身：GC、线程池队列、连接池等待、CPU\n   ▼\nT+3min  止血决策（按分诊结果，可并行）：\n   ① 洪峰超容量 → 入口限流收紧（保柜台优先额度）+ 非核心降级（内容/活动全停）\n   ② 下游劣化（柜台超时）→ 暂停自动重试防放大 + 下单入口友好降级提示\n   ③ 自身资源（连接池耗尽/慢SQL）→ 摘除异常实例 + kill 慢查询\n   同步：值班群同步影响面+措施；重大则拉应急小组（TL/DBA/业务接口人）\n   ▼\nT+8min  用户侧沟通口径（客服话术就位）；确认止血：P99 回落曲线\n   ▼\nT+15min 转入定位：现场已保全（thread dump/GC log/慢SQL样本）\n   根因假设→验证→修复方案→评估当日能否上线（交易时段变更纪律）\n   ▼\n盘后    复盘：时间线/根因/监控为何没更早发现/预案有效性/改进项"},
        {t:"p", md:"演练时的三个「资深信号」，务必练进表达："},
        {t:"ul", items:[
          "==先问变更再查性能==——一上来扎进 GC 日志是新人路径；人为变更是最快能确认或排除的变量；",
          "==止血动作全部可逆且留痕==——限流参数、降级开关、摘实例，每步在值班群报备，回滚路径明确；「先止血再定位」不是口号：定位可以花一小时，用户不能等一小时；",
          "==错误率 2% 的构成要看==——全是超时还是混着业务拒绝？超时为主说明容量/依赖问题；混着涨跌停拒绝说明可能只是行情剧烈波动的正常业务现象（这个区分能救你一次误判）。"
        ]},
        {t:"say", items:["被追问「如果止血不了呢」的底牌：==逐级收缩影响面==——先降非核心，再限流非核心用户群，极端情况（柜台故障）按预案把下单入口切成「维护/确认中」模式，让用户明确知道系统受限而不是反复失败；同时保护已受理订单的收敛链路（回报消费和状态推进不能停）。这一段展示的是「牺牲范围换正确性」的取舍能力。"]}
      ],
      shine: ["时间线剧本可直接当面试答案讲——每分钟都有动作","「先问变更再查性能」「2% 错误的构成」两个细节就是资深信号","底牌段展示逐级收缩的取舍——面试官要的成熟度"]
    },
    {
      id: "dr-sql-clinic", q: "SQL 诊疗室：一条深分页慢 SQL 的现场优化", tags:["SQL","EXPLAIN","实操"],
      scene: "给真实 SQL 和 EXPLAIN 让你现场分析是 MySQL 实操的最高频形式。这题是券商订单列表的经典慢查询：按账户查历史订单，翻到第 500 页开始变慢。练到能口述完整分析流。",
      script: [
        {t:"p", md:"**症状**：`SELECT * FROM orders WHERE account_id=8817 AND biz_date='2026-09-30' ORDER BY created_at DESC LIMIT 998000, 2000;` —— 耗时 4.2s，且越往后翻越慢。"},
        {t:"code", text:"EXPLAIN 关键列：\nkey: idx_account_date_time        ← 索引确实用上了\nkey_len: 16                       ← 只用到 (account_id, biz_date) 前缀\nrows: 1000200                     ← 预估扫描约 100 万行！\nExtra: Using where                ← 没有 Using index（回表了）"},
        {t:"p", md:"**现场口述分析流（四步）**："},
        {t:"ol", items:[
          "==诊断==：LIMIT 深偏移迫使存储引擎扫过并丢弃前 99.8 万行——索引用对了但工作量是 O(offset+limit)，且 SELECT * 每行回表。==这不是索引缺失，是访问模式问题==，加索引救不了；",
          "==方案一（首选）：游标分页==——`WHERE account_id=? AND biz_date=? AND (created_at, id) < (:lastCreatedAt, :lastId) ORDER BY created_at DESC, id DESC LIMIT 2000`。无论第几页都是定位+读 2000 行，O(limit)；(created_at, id) 行值比较保证同毫秒排序稳定；",
          "==方案二（受限场景）：限制翻页深度==——产品约定「最近 3 个月+最多翻 50 页」，更早走归档查询入口。深翻页本身是伪需求，==砍需求也是优化==；",
          "==方案三（导出类需求）==：真要全量走异步导出+流式分批读，不占在线接口。"
        ]},
        {t:"say", items:["写完方案必带的三句口述：① 为什么 `(created_at, id)` 行值比较——created_at 可能重复，id 兜底保证游标唯一不丢行不重行；② 方案一前提是索引能覆盖排序——联合索引 (account_id, biz_date, created_at, id) 前两列等值命中后后两列天然有序，==索引的有序性是排序的免费午餐==；③ 改造要兼容旧版 App——游标分页是协议变化，灰度期两接口并存，深 offset 老接口加阈值保护。"]}
      ],
      shine: ["「不是索引缺失，是访问模式问题」——第一句诊断就把你和背题的人分开","「索引的有序性是排序的免费午餐」","砍需求也是优化——产品协同意识"]
    },
    {
      id: "dr-numbers", q: "数字口径防守演练：简历上的数字被三连问", tags:["防守","口径","实操"],
      scene: "8 年简历的每个数字都是靶子。演练方式：每个数字按「口径→来源→可比性」三连问过一遍。这是面试前一晚的必修自查——数字被问倒，前面所有铺垫全部归零。",
      script: [
        {t:"tbl", head:["简历数字","追问三连","防守答法"], rows:[
          ["核心指标计算 20s → 100ms","哪两段贡献最大？压测还是生产？前后请求模型一致吗？","「两段：服务间调用改进程内 SDK 贡献约 60%（省序列化+网络 RTT×N），计算优化与缓存贡献其余；口径是同一压测模型下的 P50，生产灰度后 P99 从 21s 到 120ms——两个数我分开说，不混用」"],
          ["CPU 峰值负载降低 90%","峰值怎么定义？哪套集群？把压力转嫁给谁了？","「开盘后峰值时段均值 CPU（max 15 分钟窗口），生产 12 台均值；不是转移——SDK 化后计算仍在集群内，省掉的是序列化/网络开销，下游调用量下降是副作用不是代价」"],
          ["知识问答准确率 90%+","谁标的 ground truth？多大标注集？上线后还成立吗？","「双人标注+分歧仲裁，标注集 1200 问（高频+长尾+对抗）；90% 是离线口径，线上人工修正率 8% 佐证量级一致——两个数能互相对上，说明离线评测没有骗我」"],
          ["17 人跨地域团队","怎么分工？时区重叠多少？直接管几人？","「4 个后端小组+算法+测试，我直接带 6 人；两地时区重叠 6 小时，核心评审全放重叠窗口，异步靠文档+录制。『管』我诚实定义：技术决策我拍板，绩效不在我」"]
        ]},
        {t:"p", md:"防守总原则三条："},
        {t:"ul", items:[
          "==口径先行==：任何数字先说口径（P50/P99、峰值/均值、压测/生产、离线/在线）再说数值——先给分母的人不会被质疑分子；",
          "==数字之间要能互相印证==：离线准确率 vs 线上修正率、压测提升 vs 生产曲线——面试官会拿两个数字互相对，对不上是硬伤；",
          "==答不了的提前处理==：说不清口径的数字，要么删掉要么降级表述（「大约提升了一个量级」），不带病上场。"
        ]}
      ],
      shine: ["每个数字的防守答法都示范「先给口径再给数值」的结构","「离线 90% 和线上 8% 修正率互相印证」——数字互证是最强的可信度信号"]
    },
    {
      id: "dr-load", q: "压测设计：怎么给开盘场景建一个可信的压测模型？", tags:["压测","容量","实操"],
      scene: "「你怎么压测的」是验证性能经历真伪的照妖镜——背过「用过 JMeter」和真做过压测设计，两句话就能区分。核心考点：流量模型、数据模型、通过标准、以及压测的坑。",
      script: [
        {t:"p", md:"一个可信的开盘压测模型有四要素，按设计顺序："},
        {t:"ol", items:[
          "==流量画像==：从生产监控提取真实形态——不是匀速！开盘脉冲：9:25-9:30 集合竞价导入盘流量约为平峰 10 倍、随后 30 分钟指数衰减；读写比（下单:查询 ≈ 1:20~1:50）；热点分布（Top 50 标的占 30% 请求、Top 1% 账户贡献显著份额——热点账户必须显式建模）；",
          "==数据模型==：库容量级对齐生产（索引深度、buffer pool 命中率才有意义）；账户/标的样本按真实分布造数，覆盖极端样本（单账户千笔委托的机构户）；缓存冷热对齐——预热脚本先加载开盘会命中的数据；",
          "==依赖处理==：柜台等外部依赖用挡板（可编程延迟+错误注入）还是引流真实下游？我的答案：容量验收用挡板（可控可复现），上线前用生产流量回放/影子库做一轮真实验证——==两种都要==，只说一种都不完整；",
          "==通过标准==：提前定义——下单受理 P99<150ms、错误率<0.1%、柜台调用 P99 不超其 SLA、无状态堆积（在途订单回落）；并规定==观测什么==：每层资源水位（连接池/线程池/GC/DB），不是只看响应时间。"
        ]},
        {t:"say", items:["最后主动讲三个压测的坑（这段最加分）：① ==空业务压测==——接口通了但业务规则全走最简分支，生产一遇涨跌停校验/权限分支性能直接翻车；② ==没造失败流量==——只压成功路径，超时和重试的放大效应完全没测到（真实故障恰恰发生在这里）；③ ==压完不留档==——报告和水位快照要存档作为下次扩容与回归基线，否则每次都从零开始猜。这三条每一条我都见过对应的事故。"]}
      ],
      shine: ["四要素按设计顺序展开，流量画像精确到脉冲形态和热点分布","「挡板 vs 流量回放，两种都要」——不是单选题","三个坑对应三类真实事故——压测老手的感觉"]
    }
  ]
});
})();
