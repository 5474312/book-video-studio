<div align="center">
   
# 📚 Book Video Studio (书单视频工坊)
   
**把一本书变成一套多平台视频矩阵 (YouTube / Shorts / TikTok)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform: Hermes](https://img.shields.io/badge/Platform-Hermes-blue)](https://github.com/hermes-agent)
[![Category: Content Generation](https://img.shields.io/badge/Category-Content-orange)](https://github.com/5474312/book-video-studio)

</div>

**不是读书笔记，是流量武器。**

---

## ✨ 核心亮点

- **🎬 全时长覆盖**：60s (Shorts) / 5min / 15min / 30min 一键生成不同策略脚本。
- **🔥 爆款引擎**：基于情绪/痛点/反直觉提取，不做平庸摘要。
- **📝 分镜自动化**：输出标准 JSON 分镜表 -> 自动生图 Prompt -> 自动 TTS 分段。
- **🎨 一键合成**：内置 FFmpeg 自动化脚本，快速组装成片。
- **📖 多平台适配**：YouTube, Bilibili, TikTok, 小红书，一套内容全分发。

## 🚀 快速使用

在支持 Hermes Skill 的 AI Agent 中安装：

```bash
# 本地安装
git clone https://github.com/5474312/book-video-studio.git
cp -r book-video-studio ~/.hermes/skills/
```

然后输入指令：
> "用 book-video-studio 帮我拆解《被讨厌的勇气》，出一个 60s 短视频脚本"

## 📦 目录结构

```
book-video-studio/
├── SKILL.md                  # 核心工作流与规则定义
├── references/
│   ├── prompt-styles.md      # 5 种生图风格模板 (电影级/3D/手绘等)
│   └── script-templates/     # 4 种时长脚本模板
│       ├── 60s-template.md
│       ├── 5m-template.md
│       ├── 15m-template.md
│       └── 30m-template.md
└── scripts/
    └── auto_compose.py       # FFmpeg 自动化合成脚本
```

## 💡 适用书籍类型
- 商业管理类 (《纳瓦尔宝典》《穷查理宝典》)
- 个人成长类 (《原子习惯》《被讨厌的勇气》)
- 心理学/认知觉醒类 (《思考快与慢》)
- 搞钱/副业/技能类

---

<div align="center">

**由 [副业工坊](https://www.fuyegongfang.com) 开发 | 让 AI 为你打工**

</div>
