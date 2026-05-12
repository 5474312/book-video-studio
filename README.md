<div align="center">

# 📚 Book Video Studio (书单视频工坊) v4 Pro

**把一本书变成一套高权重、SEO 友好的多平台视频矩阵 (YouTube / Shorts / TikTok / Bilibili)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: 0.4.1](https://img.shields.io/badge/Version-0.4.1-blue)](https://github.com/5474312/book-video-studio)
[![Category: Content Generation](https://img.shields.io/badge/Category-Content-orange)](https://github.com/5474312/book-video-studio)
[![Powered by: Hermes](https://img.shields.io/badge/Powered%20by-Hermes-purple)](https://github.com/hermes-ai-agent/hermes-agent)

</div>

> **不是读书笔记，是 YouTube 流量武器。**
> 
> 一套工业级、全链路的短视频生成 SOP。从拆书提取爆点，到多平台 SEO 分发，全程自动化。

---

## 📖 目录 (Table of Contents)

- [✨ 核心亮点](#-核心亮点)
- [🎬 流水线全景](#-流水线全景)
- [🧠 模型路由矩阵](#-模型路由矩阵)
- [📦 目录结构](#-目录结构)
- [🚀 快速开始](#-快速开始)
- [📋 多平台适配](#-多平台适配)
- [🛡️ 内容安全合规](#️-内容安全合规)
- [💡 适用书籍类型](#-适用书籍类型)
- [🤝 贡献与反馈](#-贡献与反馈)

---

## ✨ 核心亮点

| 模块 | 特性 | 价值 |
| :--- | :--- | :--- |
| **🎣 交互钩子筛选** | 5 维度 Hook 变体生成 + 人工确认 | 开头定生死，确保 3 秒完播率 |
| **🔒 Style Lock** | 统一 Seed + 角色描述符强制绑定 | 彻底解决 AI 画面风格漂移 |
| **🧠 智能模型路由** | 每阶段自动匹配最优 LLM/生图/TTS 模型 | 质量与成本的最佳平衡 |
| **📱 多平台自适应** | 16:9/9:16 构图 + Safe Zone 规则 + SEO 元数据 | 一键生成 YouTube/Shorts/TikTok/B 站 |
| **🛡️ 内容合规审核** | 8 大类违规词库 + 广告法检测 + 自动改写 | 避免限流/封号，安全过审 |
| **⚡ FFmpeg 自动化** | `auto_compose.py` (info/srt/verify/render/compose) | 音画字幕一键合成，无需手动剪辑 |

---

## 🎬 流水线全景

```
[Phase 1-2] 爆款拆解 & 情绪定位 ──→ 提取反直觉观点、痛点共鸣
         ↓
 [Phase 3] 5 维度钩子生成 ──→ ⛔ 暂停等待用户确认
         ↓
 [Phase 4] 脚本撰写 ──→ 平台适配节奏 + 字数控制
         ↓
 [Phase 5] ⛔ 内容合规审核 ──→ 敏感词/广告法/引流检测 & 改写
         ↓
 [Phase 6] 分镜 JSON 生成 ──→ 画面/音频/时长/SRT 时间码
         ↓
 [Phase 7] 资产生成 ──→ Midjourney/Flux 生图 + Edge-TTS 配音
         ↓
 [Phase 8] FFmpeg 自动合成 ──→ 图片+音频+BGM+字幕 → 最终视频
         ↓
[Phase 9-10] SEO 元数据导出 ──→ 标题/标签/Chapters/封面 Prompt
```

---

## 🧠 模型路由矩阵

| 阶段 | 任务 | 推荐模型类型 | 接口/API |
| :--- | :--- | :--- | :--- |
| **1-2** | 爆款拆解、钩子生成 | **High-Quality LLM** (深度推理) | mcxapi `high_quality_general` / GPT-4o / Claude Sonnet |
| **3** | 脚本撰写 | **Creative LLM** (语气控制) | mcxapi `creative` / MiniMax-M2.5 |
| **4** | 分镜 JSON 生成 | **Structured LLM** (严格 Schema) | mcxapi `coding` / qwen3-coder-plus |
| **5** | 合规审核改写 | **Fast LLM** (模式匹配) | mcxapi `fast` / qwen-flash |
| **6** | TTS 配音 | **Text-to-Speech** | Azure TTS / ElevenLabs / Edge-TTS |
| **7** | 图片生成 | **Text-to-Image** | Midjourney v6 / DALL-E 3 / Flux.1 |
| **8** | 视频生成 (可选) | **Text-to-Video** | Kling AI / Runway Gen-3 / Luma |
| **9** | 合成 | **Local Python + FFmpeg** | `scripts/auto_compose.py` |
| **10** | SEO 元数据 | **High-Quality LLM** | mcxapi `high_quality_general` |

---

## 📦 目录结构

```
book-video-studio/
├── SKILL.md                        # 核心工作流与规则定义 (v4 Pro)
├── design.pen                      # 视觉风格参数配置（生图/BGM/字幕/字体）
├── references/
│   ├── style-engine.md             # 风格解析与 Prompt 锁定规则
│   ├── compliance-rules.md         # 违规词库与自动改写规则 (8 大类)
│   ├── execution-contract.md       # 执行契约与避坑指南
│   ├── platform-copy.md            # 多平台适配矩阵 (YouTube/Shorts/TikTok/B站)
│   └── author-config.md            # 作者专属配置模板
└── scripts/
    └── auto_compose.py             # FFmpeg 自动化合成脚本 (info/srt/verify/render/compose)
```

---

## 🚀 快速开始

在支持 Hermes Skill 的 AI Agent 中安装：

```bash
git clone https://github.com/5474312/book-video-studio.git
cp -r book-video-studio ~/.hermes/skills/
```

**使用示例：**

| 场景 | 指令示例 |
| :--- | :--- |
| **YouTube 长视频** | `"用 book-video-studio 拆解《纳瓦尔宝典》，YouTube 15min，电影风格。"` |
| **TikTok 短视频** | `"用 book-video-studio 拆解《被讨厌的勇气》，TikTok 60s，9:16。"` |
| **B 站视频** | `"用 book-video-studio 拆解《原子习惯》，B 站 5min，极简风。"` |
| **仅生成钩子** | `"用 hook-only 模式拆解《思考快与慢》的 5 个爆款开头。"` |

---

## 📋 多平台适配

| 维度 | YouTube (16:9) | Shorts/TikTok (9:16) | Bilibili (16:9) |
| :--- | :--- | :--- | :--- |
| **时长** | 10-15 min | 30-60s | 5-10 min |
| **节奏** | 深度展开 (8-12s/镜) | 极速快切 (2-3s/镜) | 干货密集 (5-8s/镜) |
| **SEO** | 标题/标签/Chapters/EndScreen | Hashtag 策略/Hook 标题 | 标题党/弹幕互动/三连 |
| **Safe Zone** | 标准 3% 边距 | 顶部 20% + 底部 30% 避让 | 标准 5% 边距 |

---

## 🛡️ 内容安全合规

内置 **8 大类违规词库**，在 Phase 5 强制扫描并自动改写：

- 🚫 **广告法极限词**：最、第一、绝对、包赚 → 领先、核心、提升
- 🚫 **引流违规**：加微信、私信、下单 → 看主页、粉丝群、橱窗
- 🚫 **平台黑话**：钱/死/杀 → 米/没/挂/领盒饭
- 🚫 **敏感话题**：政治/医疗/宗教/灰产 → 宏观/白大褂/传统文化
- 🚫 **视觉安全**：无血腥/裸露/Logo/货币/二维码
- 🚫 **版权保护**：提示使用免费字体 (思源黑体) 和版权音乐

---

## 💡 适用书籍类型

- ✅ **商业管理类** (《纳瓦尔宝典》《穷查理宝典》《精益创业》)
- ✅ **个人成长类** (《原子习惯》《被讨厌的勇气》《刻意练习》)
- ✅ **心理学/认知类** (《思考快与慢》《影响力》《乌合之众》)
- ✅ **搞钱/副业/技能类** (《副业赚钱》《纳瓦尔宝典》《一人企业》)

---

<div align="center">

**由 [副业工坊](https://www.fuyegongfang.com) 开发 | 让 AI 为你打工**

[![GitHub Stars](https://img.shields.io/github/stars/5474312/book-video-studio?style=social)](https://github.com/5474312/book-video-studio)
[![GitHub Issues](https://img.shields.io/github/issues/5474312/book-video-studio)](https://github.com/5474312/book-video-studio/issues)

</div>
