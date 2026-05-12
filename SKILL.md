---
name: book-video-studio
description: 书单视频全自动流水线 (v3 YouTube Pro)：拆书提取爆点 -> 交互钩子筛选 -> 多平台分镜 (16:9/9:16) -> 风格锁定 -> 自动 SEO/Chapters/封面生成 -> 视频组装。Use for YouTube 读书频道、TikTok Shorts、自动化视频生成。
metadata:
  openclaw:
    emoji: "📚"
    homepage: "https://github.com/5474312/book-video-studio"
    requires:
      anyBins: ["python3", "ffmpeg"]
  version: "0.3.0"
  category: "content-generation"
  author: "副业工坊"
  license: "MIT"
---

# Book Video Studio (书单视频工坊) v3 - YouTube Pro

**把一本书变成一套高权重、SEO 友好的多平台视频矩阵 (YouTube / Shorts / TikTok)**

## 🔥 核心理念 (v3 升级：YouTube 深度适配)

- **YouTube 算法优先**：不仅生成视频，还生成 **高点击率封面 (CTR)** 和 **SEO 元数据**（标题、简介、标签）。
- **长视频完播率优化**：自动生成 **视频章节 (Timestamps/Chapters)**，提升搜索展示和用户体验。
- **多平台自适应**：横屏 (16:9) 做 YouTube 长视频，竖屏 (9:16) 做 Shorts/TikTok。
- **交互钩子筛选**：防止“开头不行，全片白费”，先审 3s 开头，再做后续。
- **音画与字幕对齐**：基于语速自动估算时长，生成 SRT 字幕文件，确保 FFmpeg 合成严丝合缝。

## 🎬 时长与平台策略矩阵

| 规格 | 核心目标 | 脚本结构 | 视觉与交互策略 | 适用平台 |
| :--- | :--- | :--- | :--- | :--- |
| **60s** | **流量漏斗 (Hook)** | 3s 痛点 + 15s 反常识 + 10s 解法 + 2s CTA | 快切、大字报 (Safe Zone: 避开底部字幕区)、高对比 | Shorts, TikTok, Reels |
| **5min** | **干货输出** | 引入 - 3 个核心观点 - 总结 | 清晰图表、关键词浮现、中景、平稳节奏 | YouTube, Bilibili, Video 号 |
| **10-15min** | **深度拆解** | 背景引入 - 深度解析 (4-5 点) - 现实应用 | 丰富多变：生图 + 思维导图 + 原文滚动 + 数据图表 | **YouTube (主力)** |
| **20-30min** | **沉浸精读** | 纪录片式叙事/播客感：故事线串联全书 | 电影感：慢节奏氛围图，人物场景重现，Ken Burns 运镜 | YouTube, Podcast |

## 📦 流水线阶段 (Execution Workflow)

### Phase 1: 🔥 爆款情报与拆书 (Viral Deconstruction)
1.  **找槽点/共鸣**：从豆瓣/Goodreads 找差评（争议）和热门划线（共鸣）。
2.  **情绪定位**：确定基调（搞钱焦虑、认知觉醒、治愈系）。
3.  **提取反直觉**：找出书中颠覆常识的观点，作为 Hook 素材。

### Phase 1.5: 🎣 交互钩子筛选 (Interactive Hook Screening) ⛔ **BLOCKING STEP**
- **规则**：生成 **5 个不同维度的 3 秒开头**（痛点型/反常识型/利益型/悬念型/数据型）。
- **操作**：**输出这 5 个钩子后停止**，询问大哥选择哪一个（或组合）。
- **原因**：开头定生死，必须由人工把关。

### Phase 2: 📝 脚本与分镜生成 (Script & Storyboard)
基于选定钩子，生成 `storyboard.json`。

**多平台适配规则 (Platform Adaptation):**
- **Aspect Ratio**: 用户指定 `TikTok/Shorts` -> Prompt 后缀强制 `--ar 9:16`; `YouTube` -> `--ar 16:9`.
- **Safe Zone (9:16 专用)**: 文案禁止遮挡：底部 30% 预留给字幕，顶部 20% 预留给 TikTok UI 按钮。

**视觉一致性规则 (Style Lock):**
- **Character Lock**: 定义一个通用主角描述，强制附加到每一帧的 Prompt 后面。
- **Seed Consistency**: 生成一个随机 `seed`，全片通用。

**YouTube 专属元数据生成 (Metadata Generation):**
- **SEO Title**: 3 个备选标题（包含高搜索量关键词，Emoji 优化）。
- **Description**: 
  - 第一行：高诱惑力摘要。
  - 中部：Affiliate Link 占位符（Amazon/Kindle）。
  - 底部：**自动生成的 Chapters (时间戳)**，格式 `00:00 Intro`, `02:30 核心观点 1`。
- **Tags**: 20 个高权重 Tags。

**YouTube 封面策略 (Thumbnail Strategy):**
- 生成 **3 个高 CTR 封面 Prompt**。
- 规则：极简背景 + 夸张情绪表情/关键道具 + 粗体大字（不超过 5 字）。
- 注意：封面图虽然基于视频风格，但必须比视频内容更“夸张”以吸引点击。

**YouTube 结尾引导 (End Screen):**
- 在视频最后 20 秒标记 `End Screen Area`，提示用户点击订阅或观看下一集。

### Phase 3: 🎨 资产生成 (Asset Pipeline)
- **生图指令**: 根据 `image_prompt` 批量调用生图 API。
- **TTS 分段**: 根据 `audio_text` 生成音频文件，命名为 `tts_{index}.mp3`.
- **SRT 生成**: 输出配套的 `.srt` 字幕文件。

### Phase 4: 🎬 自动化合成 (Auto-Assembly)
使用 FFmpeg 组装。
- **命令**: `python3 scripts/auto_compose.py --storyboard storyboard.json --platform youtube`
- **合成要求**: 
    - 图片根据 `duration_estimated` 精确裁剪/缩放。
    - 自动添加 Ken Burns 运镜效果。
    - 烧录 SRT 字幕 (字体：黑体/思源黑体，底部居中，描边)。

## ✅ Done Condition
1. **钩子通过**：Phase 1.5 已获得用户确认。
2. **分镜输出**：`storyboard.json` 包含完整时间轴、估算时长、SRT 时间码。
3. **SEO 交付**：产出 Title, Description (含 Chapters), Tags, Thumbnail Prompts。
4. **平台适配**：Prompt 比例和构图已按目标平台调整。

## ⚠️ 避坑指南 (v3 Update)
- **封面即生命**：YouTube 点击率 (CTR) 决定生死，封面图必须单独优化 Prompt，不能直接用视频截图。
- **字数陷阱**：60s 视频文案绝不能超过 260 字。
- **Chapters 准确性**：生成的时间戳必须与实际视频内容精确匹配，否则会被 YouTube 判定为“误导性元数据”。
- **4K 趋势**：对于主力 YouTube 频道，建议生图时开启 4K 选项 (`--upbeta` 或 upscale)，提升画质权重。
