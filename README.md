<div align="center">
   
# 📚 Book Video Studio (书单视频工坊) v4 Pro
   
**把一本书变成一套高权重、SEO 友好的多平台视频矩阵 (YouTube / Shorts / TikTok / Bilibili)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: 0.4.0](https://img.shields.io/badge/Version-0.4.0-blue)](https://github.com/5474312/book-video-studio)
[![Category: Content Generation](https://img.shields.io/badge/Category-Content-orange)](https://github.com/5474312/book-video-studio)

</div>

**不是读书笔记，是 YouTube 流量武器。**

---

## ✨ 核心亮点 (v4 Pro Max)

- **🎬 9 阶段完整流水线**：拆书 → 钩子筛选 → 脚本 → 分镜 → 生图/生视频 → TTS → 合成 → SEO 元数据，步步严谨
- **🧪 工业级参考文档**：`design.pen` 风格配置、`style-engine.md` 风格锁定规则、`execution-contract.md` 执行契约与避坑指南、`platform-copy.md` 多平台适配矩阵
- **🧠 模型路由矩阵**：每阶段推荐最优模型（LLM / 生图 / 生视频 / TTS / FFmpeg），含 API 接口指引
- **📱 多平台自适应**：16:9 (YouTube/B站) vs 9:16 (Shorts/TikTok) 自动切换构图 + Safe Zone 规则
- **🎣 交互式钩子筛选**：先审 3 秒开头（5 个变体），再做全片，确保完播率
- **🔒 Style Lock**：统一 seed + 角色描述符，彻底解决 AI 风格漂移问题
- **⚡ FFmpeg 自动化**：`auto_compose.py` 支持 info/srt/verify/render/compose 五大子命令

## 🚀 快速使用

在支持 Hermes Skill 的 AI Agent 中安装：

```bash
git clone https://github.com/5474312/book-video-studio.git
cp -r book-video-studio ~/.hermes/skills/
```

**YouTube 长视频指令示例：**
> "用 book-video-studio 拆解《纳瓦尔宝典》，我要做 YouTube 长视频 (15min)，电影风格。"

**TikTok/Shorts 指令示例：**
> "用 book-video-studio 拆解《被讨厌的勇气》，做一个 TikTok (9:16) 短视频。"

**仅生成钩子（预览）：**
> "用 book-video-studio hook-only 模式，帮我拆解《原子习惯》的 5 个爆款开头。"

## 📦 目录结构

```
book-video-studio/
├── SKILL.md                        # 核心工作流与规则定义 (v4 Pro)
├── design.pen                      # 视觉风格参数配置（生图/BGM/字幕/字体）
├── references/
│   ├── style-engine.md             # 风格解析与 Prompt 锁定规则
│   ├── execution-contract.md       # 执行契约与避坑指南
│   ├── platform-copy.md            # 多平台适配矩阵 (YouTube/Shorts/TikTok/B站)
│   └── author-config.md            # 作者专属配置模板
└── scripts/
    └── auto_compose.py             # FFmpeg 自动化合成脚本 (info/srt/verify/render/compose)
```

## 🧠 模型路由矩阵

| 阶段 | 任务 | 推荐模型 | 接口 |
|------|------|----------|------|
| Phase 1-2 | 爆款拆解、钩子生成 | **High-Quality LLM** | mcxapi `high_quality_general` / GPT-4o / Claude Sonnet |
| Phase 3 | 脚本撰写（多平台适配） | **Creative LLM** | mcxapi `creative` / MiniMax-M2.5 |
| Phase 4 | 分镜 JSON 生成 | **Structured LLM** | mcxapi `coding` / qwen3-coder-plus |
| Phase 5 | 图片 Prompt → 生图 | **Text-to-Image** | Midjourney v6 / DALL-E 3 / Flux.1 |
| Phase 5b | 视频 Prompt → 生视频 | **Text-to-Video** | Kling AI / Runway Gen-3 / Luma Dream Machine |
| Phase 6 | TTS 配音（多角色/情感） | **Text-to-Speech** | Azure TTS / ElevenLabs / Edge-TTS |
| Phase 7 | SRT 字幕 + FFmpeg 合成 | **Local Python + FFmpeg** | `scripts/auto_compose.py` |
| Phase 8 | SEO 元数据 + 封面 Prompt | **High-Quality LLM** | mcxapi `high_quality_general` |

## 💡 适用书籍类型
- 商业管理类 (《纳瓦尔宝典》《穷查理宝典》)
- 个人成长类 (《原子习惯》《被讨厌的勇气》)
- 心理学/认知觉醒类 (《思考快与慢》)
- 搞钱/副业/技能类

---

<div align="center">

**由 [副业工坊](https://www.fuyegongfang.com) 开发 | 让 AI 为你打工**

</div>
