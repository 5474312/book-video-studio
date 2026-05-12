     1|<div align="center">
     2|   
     3|# 📚 Book Video Studio (书单视频工坊) v4 Pro
     4|   
     5|**把一本书变成一套高权重、SEO 友好的多平台视频矩阵 (YouTube / Shorts / TikTok / Bilibili)**
     6|
     7|[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
     8|[![Version: 0.4.0](https://img.shields.io/badge/Version-0.4.0-blue)](https://github.com/5474312/book-video-studio)
     9|[![Category: Content Generation](https://img.shields.io/badge/Category-Content-orange)](https://github.com/5474312/book-video-studio)
    10|
    11|</div>
    12|
    13|**不是读书笔记，是 YouTube 流量武器。**
    14|
    15|---
    16|
    17|## ✨ 核心亮点 (v4 Pro Max)
    18|
    19|- **🎬 9 阶段完整流水线**：拆书 → 钩子筛选 → 脚本 → 分镜 → 生图/生视频 → TTS → 合成 → SEO 元数据，步步严谨
    20|- **🧪 工业级参考文档**：`design.pen` 风格配置、`style-engine.md` 风格锁定规则、`execution-contract.md` 执行契约与避坑指南、`platform-copy.md` 多平台适配矩阵
    21|- **🧠 模型路由矩阵**：每阶段推荐最优模型（LLM / 生图 / 生视频 / TTS / FFmpeg），含 API 接口指引
    22|- **📱 多平台自适应**：16:9 (YouTube/B站) vs 9:16 (Shorts/TikTok) 自动切换构图 + Safe Zone 规则
    23|- **🎣 交互式钩子筛选**：先审 3 秒开头（5 个变体），再做全片，确保完播率
    24|- **🔒 Style Lock**：统一 seed + 角色描述符，彻底解决 AI 风格漂移问题
    25|- **⚡ FFmpeg 自动化**：`auto_compose.py` 支持 info/srt/verify/render/compose 五大子命令
    26|
    27|## 🚀 快速使用
    28|
    29|在支持 Hermes Skill 的 AI Agent 中安装：
    30|
    31|```bash
    32|git clone https://github.com/5474312/book-video-studio.git
    33|cp -r book-video-studio ~/.hermes/skills/
    34|```
    35|
    36|**YouTube 长视频指令示例：**
    37|> "用 book-video-studio 拆解《纳瓦尔宝典》，我要做 YouTube 长视频 (15min)，电影风格。"
    38|
    39|**TikTok/Shorts 指令示例：**
    40|> "用 book-video-studio 拆解《被讨厌的勇气》，做一个 TikTok (9:16) 短视频。"
    41|
    42|**仅生成钩子（预览）：**
    43|> "用 book-video-studio hook-only 模式，帮我拆解《原子习惯》的 5 个爆款开头。"
    44|
    45|## 📦 目录结构
    46|
    47|```
    48|book-video-studio/
    49|├── SKILL.md                        # 核心工作流与规则定义 (v4 Pro)
    50|├── design.pen                      # 视觉风格参数配置（生图/BGM/字幕/字体）
    51|├── references/
    52|│   ├── style-engine.md             # 风格解析与 Prompt 锁定规则
    53|│   ├── execution-contract.md       # 执行契约与避坑指南
    54|│   ├── platform-copy.md            # 多平台适配矩阵 (YouTube/Shorts/TikTok/B站)
    55|│   └── author-config.md            # 作者专属配置模板
    56|└── scripts/
    57|    └── auto_compose.py             # FFmpeg 自动化合成脚本 (info/srt/verify/render/compose)
    58|```
    59|
    60|## 🧠 模型路由矩阵
    61|
    62|| 阶段 | 任务 | 推荐模型 | 接口 |
    63||------|------|----------|------|
    64|| Phase 1-2 | 爆款拆解、钩子生成 | **High-Quality LLM** | mcxapi `high_quality_general` / GPT-4o / Claude Sonnet |
    65|| Phase 3 | 脚本撰写（多平台适配） | **Creative LLM** | mcxapi `creative` / MiniMax-M2.5 |
    66|| Phase 4 | 分镜 JSON 生成 | **Structured LLM** | mcxapi `coding` / qwen3-coder-plus |
    67|| Phase 5 | 图片 Prompt → 生图 | **Text-to-Image** | Midjourney v6 / DALL-E 3 / Flux.1 |
    68|| Phase 5b | 视频 Prompt → 生视频 | **Text-to-Video** | Kling AI / Runway Gen-3 / Luma Dream Machine |
    69|| Phase 6 | TTS 配音（多角色/情感） | **Text-to-Speech** | Azure TTS / ElevenLabs / Edge-TTS |
    70|| Phase 7 | SRT 字幕 + FFmpeg 合成 | **Local Python + FFmpeg** | `scripts/auto_compose.py` |
    71|| Phase 8 | SEO 元数据 + 封面 Prompt | **High-Quality LLM** | mcxapi `high_quality_general` |
    72|
    73|## 💡 适用书籍类型
    74|- 商业管理类 (《纳瓦尔宝典》《穷查理宝典》)
    75|- 个人成长类 (《原子习惯》《被讨厌的勇气》)
    76|- 心理学/认知觉醒类 (《思考快与慢》)
    77|- 搞钱/副业/技能类
    78|
    79|---
    80|
    81|<div align="center">
    82|
    83|**由 [副业工坊](https://www.fuyegongfang.com) 开发 | 让 AI 为你打工**
    84|
    85|</div>
    86|