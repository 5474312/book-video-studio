<div align="center">
   
# 📚 Book Video Studio (书单视频工坊) v3 YouTube Pro
   
**把一本书变成一套高权重、SEO 友好的多平台视频矩阵 (YouTube / Shorts / TikTok)**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version: 0.3.0](https://img.shields.io/badge/Version-0.3.0-blue)](https://github.com/5474312/book-video-studio)
[![Category: Content Generation](https://img.shields.io/badge/Category-Content-orange)](https://github.com/5474312/book-video-studio)

</div>

**不是读书笔记，是 YouTube 流量武器。**

---

## ✨ 核心亮点 (v3 YouTube Pro)

- **🎬 YouTube 算法适配**：自动生成 SEO 标题、标签、简介（含时间戳章节）。
- **🖼️ 高点击率封面策略**：专为 YouTube 生成高 CTR 封面 Prompt，拒绝平庸截图。
- **📱 多平台自适应**：16:9 (YouTube 长视频) vs 9:16 (Shorts/TikTok) 自动切换构图。
- **🎣 交互式钩子筛选**：先审 3 秒开头，再做全片，确保完播率。
- **⚡ 全自动化组装**：SRT 字幕自动生成 + FFmpeg 脚本一键合成。

## 🚀 快速使用

在支持 Hermes Skill 的 AI Agent 中安装：

```bash
# 本地安装
git clone https://github.com/5474312/book-video-studio.git
cp -r book-video-studio ~/.hermes/skills/
```

**YouTube 长视频指令示例：**
> "用 book-video-studio 拆解《纳瓦尔宝典》，我要做 YouTube 长视频 (15min)，帮我选个高点击率封面风格。"

**TikTok/Shorts 指令示例：**
> "用 book-video-studio 拆解《被讨厌的勇气》，做一个 TikTok (9:16) 短视频。"

## 📦 目录结构

```
book-video-studio/
├── SKILL.md                  # 核心工作流与规则定义 (v3 YouTube Pro)
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