# Agent 论文知识库（2025 – 2026.09）

> 面向面试与持续学习的 **AI Agent / Multi-Agent / 上下文工程** 知识库。
> 20 篇典型高引论文 × 8 章循序渐进 × 2 个实战案例 × 20 张手绘机制图 × 8 类面试场景话术。

作者：Steven Li（李一俊）· AI 应用技术负责人 / 软件架构师

## ✨ 特性

- **章节式循序渐进**：范式 → 上下文工程 → 多智能体 → 底座模型 → RL 与深度研究 → 评测与协议 → 两个实战案例收束
- **每篇论文「总分总」**：解决什么问题 → 主旨思路与设计理念 → 分要点 → 关键数据 → 一句话总结
- **一图胜千言**：每篇配一张针对论文精髓单独绘制的核心机制图（inline SVG，零依赖）
- **关联关系网**：每篇标注前置阅读 / 相关论文 / 进阶应用 / 案例落点，页间互相跳转
- **面试导向**：每篇含"面试怎么结合"话术；速查工具页汇总 8 类场景 × 30 秒话术
- **两个实战案例**：保险知识库平台（RAG + 三层意图路由 + 规则引擎）、金融 DeepResearch（多路并行取数 + 交叉校验）

## 📖 在线阅读

推送到 GitHub 后开启 **Settings → Pages → Deploy from branch (main / root)**，即可通过
`https://<你的用户名>.github.io/agent-papers-kb/` 直接访问。

## 🗂 章节目录

| 章 | 主题 | 论文 |
|---|---|---|
| 1 | Agent 设计范式与方向 | Building Effective Agents · OpenAI 落地指南 · The Second Half |
| 2 | 上下文工程与记忆 | Manus · Context Engineering 综述 · Mem0 |
| 3 | 多智能体：模式、失败与框架 | 多智能体研究系统复盘 · MAST 失败分类 · AgentScope 1.0 |
| 4 | Agentic 底座模型 | DeepSeek-R1 · Qwen3 · Kimi K2 · GLM-4.5 · LongCat-Flash |
| 5 | Agent RL 与深度研究 | Agentic RL 综述 · 通义 DeepResearch |
| 6 | 交互、评测与协议 | UI-TARS · BrowseComp · BFCL V3 · MCP / A2A |
| 7 | 实战案例一 | 民生保险：知识库问答 + 佣金问答 + 意图匹配（保单变更识别 + 规则校验） |
| 8 | 实战案例二 | 金融 DeepResearch：多路并行取数 + 结果校验 + 问答报告链路 |

## 🛠 本地构建

站点由 `tools/` 下的三个脚本生成（数据即代码），零第三方依赖：

```bash
python3 tools/gen_papers.py     # 1. 论文数据 → 基础页面
python3 tools/gen_cases.py      # 2. 生成两个实战案例页
python3 tools/gen_site_v2.py    # 3. 章节式重建（门户/章节/论文/速查）+ 案例章节导航
python3 tools/check_links.py    # 4. QA：全站断链检查（应为 0）
```

默认输出到仓库根目录；可用 `KB_SITE=/path/to/out` 覆盖输出目录。

## ➕ 如何新增内容

新增论文 / 行业案例 / 面试场景的完整方法论已沉淀为技能文件：
[`skills/agent-kb/SKILL.md`](skills/agent-kb/SKILL.md) —— 包含数据源清单、总分总字段模板、
机制图（SVG helpers）绘制方法、QA 验收清单。

## 📁 目录结构

```
├── index.html          门户（学习路径 + 案例入口）
├── cheatsheet.html     速查工具页（面试前 30 分钟）
├── chapters/           第 1–6 章（每章含总分总速览 + 学习目标）
├── papers/             20 篇论文深度笔记（每篇含核心机制图）
├── cases/              2 个实战案例（民生保险 / 金融 DeepResearch）
├── assets/style.css    共享样式
├── tools/              构建脚本（数据即代码，可复现）
└── skills/             扩展技能（数据源 / 模板 / 生图方法）
```

## 📚 主要数据来源

- 论文：[arXiv](https://arxiv.org/)（检索核实 arXiv ID 与引用量级）
- 工程博客：[Anthropic Engineering](https://www.anthropic.com/engineering) · [OpenAI](https://openai.com/index/) · [美团 LongCat](https://github.com/meituan-longcat/LongCat-Flash-Chat) · [Qwen](https://github.com/QwenLM) · [智谱](https://github.com/zai-org/GLM-4.5) · [月之暗面](https://github.com/MoonshotAI/Kimi-K2)
- 行业案例：[OpenAI × Morgan Stanley](https://openai.com/index/morgan-stanley/) · [证券时报：金融终端 AI 竞争](https://stcn.com/article/detail/3620915.html) · [沙丘社区：保险业大模型案例](https://www.shaqiu.cn/article/1awlLodwVWzP)
- 面经：[AgentGuide（小红书面经整合）](https://github.com/adongwanai/AgentGuide) · [代码随想录大模型面经](https://notes.kamacoder.com/interview/llm/) · 知乎 / 牛客 / CSDN

## License

MIT
