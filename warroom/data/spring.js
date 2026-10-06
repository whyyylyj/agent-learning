/* 模块：Spring 与 MyBatis */
(function(){
const M = window.GJ_MODULES = window.GJ_MODULES || [];

M.push({
  id: "spring", icon: "🌱", name: "Spring / 安全 / MyBatis",
  desc: "🔴 标记的 5 道题来自 2024-05 牛客《国金证券 Java 面经》已核验原题（JWT、登录安全、Bean 生命周期、循环依赖、AOP），是全站优先级最高的一组。答题策略：每题都挂一个你项目里的真实实现。",
  cards: [
    {
      id: "sp-jwt", q: "讲讲项目中 JWT 的工作原理（🔴国金真题）", zhen:true, tags:["安全","已核验原题"],
      scene: "2024-05 国金 Java 面经原题。从「你的项目里 JWT 怎么用的」切入，然后沿原理→风险→改进连续追问。答题要点：把三段结构、验签链路和「Payload 不是加密」讲清，并主动暴露你项目的风险点——主动暴露风险是资深信号。",
      script: [
        {t:"p", md:"先给三段结构，再立刻挂到自己项目上："},
        {t:"say", items:["JWT 常见的 JWS 形式是三段：==Base64Url(Header).Base64Url(Payload).Signature==。Header 声明类型和签名算法；Payload 放 claims——我的项目里是 subject=userName、role、业务类型、签发时间和过期时间；Signature 对前两段做完整性保护，服务端验签通过才信任里面的内容。**要特别强调 Payload 只是编码不是加密**，Base64 解码谁都能看，所以密码、敏感信息绝不能放进去。"]},
        {t:"say", items:["我项目里的完整链路：登录时 BCrypt 校验密码 → JJWT 生成 HS256 签名的 Token（HMAC，签发验签共用密钥）→ 前端存储，后续请求带 `Authorization: Bearer` → 自定义 `OncePerRequestFilter` 解析验签 → 写入 SecurityContext → Spring Security 按 URL+角色授权。这个链路里有几个我主动识别的生产化风险：==密钥写在配置文件里==（应该进 KMS/Secret 并支持轮换）；==Token 有效期 24 小时偏长==（应该短 Access + 受控 Refresh）；==没有 jti，无法单 Token 撤销==（用户改角色或被禁用后旧 Token 还有旧权限）；==前端放 localStorage 有 XSS 窃取风险==（应评估 HttpOnly Cookie）。"]},
        {t:"say", items:["JWT vs Session 的选择我不会说「JWT 一定更好」：JWT 的价值在无状态横向扩展和多服务共享身份，代价是**主动撤销困难、Claim 可能陈旧**。管理后台这种强撤销场景，服务端 Session 反而更合适——按场景选，这是我的态度。"]}
      ],
      shine: [
        "讲原理只花三分之一时间，大半时间在讲**自己项目的风险清单和改进方向**——这是 8 年人的典型结构",
        "「Payload 是编码不是加密」主动强调，堵住面试官最想挖的坑",
        "JWT vs Session 不站队，给场景化判断"
      ],
      fu: [
        {q:"HS256 和 RS256 区别？", a:"HS256 对称，签发验签同一密钥，内部服务简单高效但密钥一泄露任何人可签发；RS256 非对称，私钥签发公钥验签，公钥可分发（第三方/多服务验签），密钥管理更安全但性能开销和复杂度高。内部单体/少量服务 HS256 够用，开放平台选 RS256。"},
        {q:"用户被禁用/改角色后，旧 Token 怎么失效？", a:"短有效期 + 撤销机制：jti 黑名单（Redis）、用户级 tokenVersion（签发时校验版本号）、或高风险接口实时查账户状态。我的项目 24h 有效期+无撤销是已知短板，我会先降有效期再上 tokenVersion。"},
        {q:"Token 放 localStorage 还是 Cookie？", a:"localStorage 便于携带但 XSS 可读；HttpOnly+Secure+SameSite Cookie 防 XSS 窃取但要处理 CSRF（SameSite+CSRF Token）。金融场景我倾向 Cookie 方案+严格 CSP，配合登录风控。"},
        {q:"怎么发现 Token 被盗用？", a:"设备指纹/IP 突变、同 Token 并发多地域使用、行为模型异常；审计日志记录 Token 使用轨迹，异常时强制下线（需要撤销机制配合）。"}
      ],
      pit: ["把 Payload 说成「加密的」","只背结构不讲自己项目的实现和风险","说「JWT 比 Session 先进」这种绝对判断"],
      src: "牛客《国金证券 Java 面经》2024-05 · 已核验原题；细节对照 OWASP Password Storage Cheat Sheet 与 RFC 7519"
    },
    {
      id: "sp-login-sec", q: "登录时账号密码传进来的安全措施是什么？是 MD5 吗？（🔴国金真题）", zhen:true, tags:["安全","已核验原题"],
      scene: "原题原话里就带「MD5 吗」——面试官在测试你是否混淆「传输安全、存储安全、页面显示」三个层次，以及是否知道前端 MD5 为什么无效。",
      script: [
        {t:"say", items:["直接回答：==不是靠前端 MD5==。我分三层讲：**传输层**靠 HTTPS/TLS 防窃听和篡改；**存储层**靠慢密码哈希——我的项目用 BCrypt（自带随机盐和成本因子，数据库只存 BCrypt 结果，不需要单独的 salt 列）；**页面层**只是 `type=password` 防旁人偷看，和安全无关。"]},
        {t:"say", items:["为什么前端固定 MD5 没用？因为它==把这个 MD5 值变成了「等价密码」==——攻击者截获或拖库后拿 MD5 值直接重放登录即可，而且 MD5 计算太快，扛不住离线暴力破解。密码哈希要「故意慢、可调成本、带随机盐」，这就是 BCrypt/Argon2 的设计意图。服务端校验用 `passwordEncoder.matches(明文, 库里的哈希)`，日志中密码字段全程脱敏。"]},
        {t:"say", items:["再主动补一层登录防护的完整拼图，展示生产视野：登录失败限速和账号锁定（防爆破和撞库）、统一错误话术「用户名或密码错误」（防账号枚举）、MFA 用于高风险操作、密码修改后撤销旧 Token、默认密码强制首改。我的项目目前缺失败限速和唯一约束——数据库层用户名唯一索引还没加，应用层先查后插有并发竞态，这是我清单上的第一个改进项。"]}
      ],
      shine: [
        "三层次一次分清，直接把「MD5」这个坑连根拔掉",
        "「MD5 值会成为等价密码」——安全面试里最能体现深度的一句话",
        "主动说出自己项目「缺唯一索引、有并发竞态」——诚实+改进意识双加分"
      ],
      fu: [
        {q:"BCrypt 的 cost 参数什么作用？", a:"指数级控制哈希耗时（cost 10 约 100ms 量级），硬件升级后可调高而不破坏旧哈希（哈希串里自带 cost 和盐）。慢是为了让暴力破解代价高到不可行。"},
        {q:"前端用 RSA 加密密码再传，是不是更安全？", a:"可作为特定威胁模型的附加层，但替代不了 TLS：公钥怎么可信下发、密文是否可重放、私钥如何保护都是新问题。常规 Web 登录优先把 TLS、慢哈希、限流、MFA 做扎实。"},
        {q:"撞库攻击怎么防？", a:"多维风控：失败频率限速（按账号+IP+设备）、设备指纹、异常登录二次验证、泄露密码库检查（禁止常见密码）。"}
      ],
      pit: ["答「前端 MD5 一下再传」——这是原题里埋的标准错误答案","混淆「加密可逆」和「哈希不可逆」","只答 BCrypt 不讲传输层 TLS，层次混乱"]
    },
    {
      id: "sp-bean", q: "讲讲 Spring Bean 的生命周期（🔴国金真题）", zhen:true, tags:["Spring","已核验原题"],
      scene: "原题。背主线人人都会，区分度在于：① 主线顺序精确；② 能挂到自己项目里的真实例子；③ 知道 AOP 代理在哪个阶段形成。资料提醒：不用一上来背完所有 Aware/扩展点接口。",
      script: [
        {t:"say", items:["我按单例 Bean 的主线讲：**实例化**（构造器/工厂方法）→ **属性填充**（依赖注入）→ **Aware 回调**（BeanNameAware/ApplicationContextAware 等）→ **BeanPostProcessor 前置处理** → **初始化**（`@PostConstruct` → `afterPropertiesSet` → 自定义 init-method，按这个顺序）→ **BeanPostProcessor 后置处理**（==AOP 代理通常在这里生成==，AbstractAutoProxyCreator 就是个 BeanPostProcessor）→ Bean 可用 → 容器关闭时 **销毁回调**（`@PreDestroy` → destroy → destroy-method）。"]},
        {t:"p", md:"然后立刻落到项目——这是本题的胜负手："},
        {t:"say", items:["我项目里 `JwtTokenProvider` 就是个活例子：它用 `@Value` 注入 secret 和过期时间，然后在 `@PostConstruct init()` 里把配置转成 HMAC Key。这正说明**为什么初始化逻辑不能放构造器**——构造器执行时 `@Value` 还没注入，字段还是 null；`@PostConstruct` 保证了注入完成后执行。我也反思过：用构造器绑定配置（Boot 的 `@ConfigurationProperties` 或构造注入）会更类型安全、更好测——这是我下一版想改的。"]},
        {t:"say", items:["追问预备：BeanFactoryPostProcessor 作用在 **BeanDefinition 元数据**层（实例化之前，比如 PropertySourcesPlaceholderConfigurer），BeanPostProcessor 作用在 **Bean 实例**层（初始化前后）——一个改配方一个改成品。prototype Bean 容器创建并初始化它，但交付后不再管理其销毁回调。"]}
      ],
      shine: [
        "主线讲完 30 秒内挂上 JwtTokenProvider/@PostConstruct 的项目实例",
        "「AOP 代理在 BPP 后置阶段生成」这句是给面试官的钩子——他大概率顺着问 AOP/循环依赖，正好进入你的主场",
        "主动反思 @Value+@PostConstruct vs 构造器绑定的取舍"
      ],
      fu: [
        {q:"@PostConstruct、afterPropertiesSet、init-method 的顺序？", a:"@PostConstruct（BeanPostProcessor 的 CommonAnnotationBeanPostProcessor 驱动）→ afterPropertiesSet（InitializingBean）→ init-method。都在 BPP 前置之后、后置之前。"},
        {q:"BeanPostProcessor 对所有 Bean 生效吗？注册时机有影响吗？", a:"对容器内所有 Bean 生效；BPP 自身要尽早注册，普通 Bean 定义阶段之后注册的 BPP 可能错过部分 Bean——这也是为什么 BPP 通常用静态 @Bean 方法注册。"}
      ],
      pit: ["背 15 个 Aware 接口但没有一个项目例子","不知道代理在哪个阶段形成","把 BeanFactoryPostProcessor 和 BeanPostProcessor 混为一谈"]
    },
    {
      id: "sp-circular", q: "Spring 的循环依赖怎么解决？三级缓存为什么是三级？（🔴国金真题）", zhen:true, tags:["Spring","已核验原题"],
      scene: "原题，追问链很深：三级缓存→为什么不是两级→构造器为什么不行→AOP 场景→你的项目怎么办。资料给出关键提醒：你的项目是 Spring Boot 2.7（2.6+ 默认禁止循环引用），答「靠三级缓存正常运行」会露馅，正确姿态是「默认禁止，出现即重构」。",
      script: [
        {t:"say", items:["先分类，因为「能不能解」取决于注入方式：==setter/字段注入的单例==是经典可解场景；==构造器注入的循环依赖==解不了——A 构造要 B、B 构造要 A，谁都完不成实例化，提前暴露引用也无济于事；prototype 循环依赖容器也不解。"]},
        {t:"p", md:"三级缓存的机制和「为什么是三级」："},
        {t:"tbl", head:["缓存","内容","作用"], rows:[
          ["singletonObjects","完成初始化的成品 Bean","正常获取"],
          ["earlySingletonObjects","提前暴露的早期引用","避免工厂重复创建"],
          ["singletonFactories","能生成早期引用的 ObjectFactory","按需生成 + 给 BPP 介入机会"]
        ]},
        {t:"say", items:["核心问题只有一个：**三级 vs 两级**。A 创建中、B 依赖 A 时，如果没有 AOP，把 A 的半成品引用直接给 B 就够了，两级足够。但有了 AOP，最终容器里的 A 应该是**代理对象**——如果提前把原始对象给了 B，B 拿到的和容器里放的不是同一个对象。三级缓存的 ObjectFactory 允许**在真正被循环依赖需要时**，才通过 `SmartInstantiationAwareBeanPostProcessor.getEarlyBeanReference` 生成早期代理，保证 B 拿到的引用和最终代理一致。== factories 这层是把「要不要提前代理」的决策延迟到必要时刻==。"]},
        {t:"say", items:["落到我的项目：Spring Boot 2.7 **默认禁止循环引用**，出现就直接启动失败。我的核心 Service 全部构造器注入——这会让循环依赖在启动期立刻暴露，逼迫你面对设计问题。真出现了我会优先：拆职责、把共同依赖下沉为第三个组件、或改领域事件解耦；`@Lazy` 只做应急，它只是延迟问题不是解决问题；`allow-circular-references=true` 不进我的方案清单。"]}
      ],
      shine: [
        "「三级 vs 两级」用 AOP 代理一致性讲透——这是本题真正的区分点",
        "主动点破「我的 Boot 2.7 项目默认禁止循环引用」——防住面试官按 08 年老答案追问的反杀",
        "构造器注入=启动期暴露设计问题，把技术选择讲成工程哲学"
      ],
      fu: [
        {q:"为什么构造器注入解决不了？", a:"创建 A 需要先把 B 传进构造器，创建 B 又需要 A——死锁在实例化之前，连「半成品引用」都不存在，无从提前暴露。"},
        {q:"A 出现了，三级缓存里 earlySingletonObjects 和 factories 会怎么流转？", a:"第一次通过 factories 的 getObject 拿早期引用，结果放入 earlySingletonObjects 并删掉 factory——保证同一 Bean 的早期引用只生成一次、全局唯一。"},
        {q:"@Async / @Transactional 的 Bean 在循环依赖里有什么特殊问题？", a:"这些也是代理增强，同理依赖早期代理机制；部分场景（如 @Async 的代理与最终 Bean 不一致的历史问题）曾是三级缓存设计的直接动因。"}
      ],
      pit: ["背「三级缓存」说不出第三级为什么必须存在","不知道 Boot 2.6+ 默认禁止循环引用","把 @Lazy 说成「推荐解法」而不是应急手段"]
    },
    {
      id: "sp-aop", q: "讲讲你项目中 AOP 的使用（🔴国金真题）", zhen:true, tags:["AOP","已核验原题"],
      scene: "原题。这题的陷阱：如果你简历写了 AOP 而答不出真实用例，或者把 Filter 说成 AOP，直接掉分。资料给的策略是「诚实 + 展示设计能力」：当前项目用 Filter 做鉴权（说明为什么不用 AOP），再给一个我会写 AOP 的真实候选场景。",
      script: [
        {t:"say", items:["我如实说：我的项目里认证鉴权用的是 ==Servlet Filter + Spring Security 过滤器链==，不是自定义 @Aspect——因为鉴权要在进入 Controller 之前建立 SecurityContext，这是 HTTP 过滤器层的职责，AOP 管不到这一层。项目里我没有为了用 AOP 而用 AOP。"]},
        {t:"p", md:"但 AOP 的原理和适用场景我是清楚的："},
        {t:"say", items:["Spring AOP 基于代理：有接口默认 JDK 动态代理（实现 InvocationHandler），无接口用 CGLIB 子类代理；外部调用先进代理执行 advice 再到目标方法。==由此推出失效场景==：`this.method()` 自调用不走代理（事务/切面失效）、private 和 final 方法无法被子类代理拦截。适合 AOP 的是**方法级横切关注点**。"]},
        {t:"say", items:["如果这个项目要加 AOP，我会第一个用在==敏感业务操作审计==上——比如面试评价的修改：`@Around(\"@annotation(audited)\")` 环绕切面，记录操作者、动作、资源 ID、traceId、结果和耗时。设计时我会想清楚四个问题：**切面异常不能影响主业务**（审计写入 try-catch 隔离，失败进异步补偿）；**不打方法参数原文**（参数里可能有简历正文、密码，只记内部 ID 和摘要，这是合规要求）；**审计与业务事务的顺序**（审计要在事务提交后确认，否则记了审计但业务回滚，出现假审计）；**切面优先级**（相对事务切面的 order）。"]}
      ],
      shine: [
        "诚实说「当前没用 AOP」并给出技术理由——比硬编一个 AOP 用例可信十倍",
        "「Filter 管请求层、AOP 管方法层」边界清晰",
        "审计切面的四个设计考量（异常隔离/参数脱敏/事务顺序/优先级）——一眼就是写过生产级切面的人"
      ],
      fu: [
        {q:"自调用为什么失效？怎么解决？", a:"自调用是 this 调用，没经过代理对象，增强逻辑自然不执行。解决：注入自身代理（AopContext）、拆到另一个 Bean、或重构避免内部调用增强方法。"},
        {q:"JDK 动态代理和 CGLIB 怎么选的？", a:"有接口默认 JDK（Proxy+InvocationHandler，基于反射）；无接口或 proxyTargetClass=true 用 CGLIB（字节码生成子类）。final 类/方法无法被 CGLIB 覆盖。Boot 默认全部 CGLIB（spring.aop.proxy-target-class=true）。"},
        {q:"Filter、Interceptor、AOP 怎么分工？", a:"Filter 在 Servlet 容器层（CORS、认证入口、请求包装）；Interceptor 在 Spring MVC 层（Controller 前后、Handler 相关、preHandle 可终止）；AOP 在 Bean 方法层（审计、事务、指标）。鉴权放 Filter，业务审计放 AOP——按「离请求近用 Filter，离业务近用 AOP」记忆。"}
      ],
      pit: ["简历写了 AOP 却没有真实代码支撑——资料明确说这种情况应删掉技术词","把 JWT 过滤器说成 AOP 的应用","审计切面打印全量方法参数——合规红线"]
    },
    {
      id: "sp-tx", q: "@Transactional 在哪些情况下会失效？事务传播讲一下", tags:["事务","高频"],
      scene: "高频题。失效场景的本质只有一个：绕过了代理或没有事务可回滚。能从代理机制统一推导所有失效场景，就赢过 90% 背清单的候选人。",
      script: [
        {t:"say", items:["我记失效场景不用清单，用一句话推导：==事务是 AOP 代理实现的，所以「绕过代理」或「异常没有按规则抛出」就失效==。绕过代理的：同类自调用（this 不走代理）、方法非 public、对象不是 Spring Bean、catch 掉异常没抛出；规则不匹配的：默认只对 RuntimeException/Error 回滚，受检异常要配 `rollbackFor`；线程切换（`@Async` 或新开线程）离开事务上下文；还有多线程并发访问同一事务资源本身就不受事务保护。"]},
        {t:"say", items:["传播行为我重点用三个：REQUIRED（默认，有就加入没有就新建）是绝大多数场景；REQUIRES_NEW 用于「子操作必须独立提交」——比如审计日志，主业务回滚审计也要留下；NESTED 用保存点实现可回滚的子事务，但依赖 JDBC 保存点支持。==坑在边界==：REQUIRES_NEW 会挂起外层事务占用第二个连接，连接池紧张时是死锁放大器，我在压测里见过连接池被挂起事务吃满的案例。"]},
        {t:"say", items:["事务边界我的原则：**一个事务只包住单库的业务不变量**——校验、状态变更、流水落库在一个事务里；==慢 RPC、发外部消息不进事务==（长事务放大锁持有时间和 undo 压力）；跨资源一致性交给 Outbox/事务消息+幂等+对账（下一题展开）。"]}
      ],
      shine: ["「一句话推导所有失效场景」——从机制而不是清单理解","REQUIRES_NEW 连接池死锁的实战案例","事务边界的「单库不变量」原则"]
    },
    {
      id: "sp-outbox", q: "Spring 事务能保证「落库 + 发 MQ」的一致性吗？怎么解决？", tags:["一致性","Outbox"],
      scene: "从 Spring 事务延伸到分布式一致性的关键题。答「Transactional 注解包住发送代码」是典型错误；Outbox 方案的完整闭环是资深标志。",
      script: [
        {t:"say", items:["不能。数据库事务只覆盖数据库这一个资源：==先发消息再提交==，事务回滚了消息收不回来；==先提交再发消息==，提交后进程挂了消息就丢了。这是两个独立资源，本地 ACID 管不到。"]},
        {t:"p", md:"标准解是 Transactional Outbox（本地消息表）："},
        {t:"flow", text:"本地事务 {\n  更新订单状态;\n  INSERT outbox_event(event_id, payload, status=PENDING);\n}  ← 原子性由本地事务保证\n发布器：扫描/CDC 捕获 PENDING → 发 MQ → 标记 SENT（幂等）\n消费者：按 event_id 幂等消费\n兜底：对账任务比对 outbox 与 MQ，超时未 SENT 告警重投"},
        {t:"say", items:["代价也要说：消息有延迟（扫描间隔或 CDC 延迟）、outbox 表膨胀要归档、多实例扫描要做分片或抢占、发布器挂了要有监控。==消费者仍然必须幂等==——outbox 解决的是「发不发得出」，解决不了「被消费几次」。如果用 RocketMQ 的事务消息也行，半消息+回查把「先写库还是先发消息」的时序问题交给 broker，但回查逻辑要求本地事务状态可查询，两种方案我都评估过，团队有 CDC 基础设施时我倾向 Outbox，毕竟它是纯数据库方案，不引入对特定 MQ 特性的依赖。最后仍是那句话：**对账是最终防线**。"]}
      ],
      shine: ["两种时序颠倒的失败模式讲清楚再给方案","主动讲 Outbox 的四个运维代价——方案没有免费的","Outbox vs 事务消息的选型比较，有明确倾向和理由"]
    },
    {
      id: "sp-mybatis", q: "MyBatis 的 #{} 和 ${} 区别？MyBatis-Plus 在你项目里怎么用的？", tags:["MyBatis"],
      scene: "简历上有 MyBatis-Plus 就必被问。#{} / ${} 是 SQL 注入的入口题，顺带考你对框架「做了什么、没做什么」的清醒度。",
      script: [
        {t:"say", items:["`#{}` 是预编译参数占位，走 PreparedStatement，值作为参数绑定，==防 SQL 注入==；`${}` 是字符串拼接，有注入风险，只用在**白名单可控**的场景——动态表名、`ORDER BY` 列名这类无法参数化的位置，且必须在代码层枚举校验，绝不让用户输入直通 `${}`。"]},
        {t:"say", items:["MyBatis-Plus 在我项目里的使用保持克制：单表 CRUD、逻辑删除、分页插件这些标准能力直接用，==复杂查询仍然手写 XML==——QueryWrapper 堆复杂条件可读性很差，而且 Lambda 条件绕过 XML 会让 SQL 散落各处，Code Review 和 DBA 审计都困难。另外两个纪律：分页插件在深分页场景我不用 `LIMIT offset`（见 MySQL 模块），用游标；`selectOne` 我会注意多行结果会抛异常——我项目里用户名没加唯一索引时，`selectOne` 在重复数据下就会炸，这也是我推动加唯一索引的原因之一。"]}
      ],
      shine: ["${} 的「白名单+枚举校验」边界纪律","「复杂 SQL 手写 XML」的克制态度——对框架滥用有警惕","selectOne 抛异常直接关联到自己项目的索引改造，形成证据链"]
    }
  ]
});
})();
