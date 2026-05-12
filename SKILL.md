---
name: book-video-studio
description: 书单视频全自动流水线：从拆书提取爆点 -> 多时长脚本生成 -> 分镜/生图脚本 -> TTS/BGM 合成 -> 视频组装。支持 60s/5min/15min/30min 全场景覆盖。Use for 书单视频制作、拆书文案、YouTube 读书频道、自动视频生成。
metadata:
  openclaw:
    emoji: "📚"
    homepage: "https://github.com/5474312/book-video-studio"
    requires:
      anyBins: ["python3", "ffmpeg"]
  version: "0.1.0"
  category: "content-generation"
  author: "副业工坊"
  license: "MIT"
---

# Book Video Studio (书单视频工坊)

**把一本书变成一套多平台视频矩阵（Shorts -> YouTube）**

## 🔥 核心理念

- **不做读书笔记，只做流量武器。**
- **时长决定策略：** 60s 抓眼球，5min 给干货，15min 讲逻辑，30min 做沉浸。
- **情绪驱动：** 所有的拆解都围绕“痛点、焦虑、共鸣、反直觉”。
- **全自动化：** 输出标准分镜 JSON -> 自动调生图/TTS/BGM -> 自动 FFmpeg 组装。

## 🎬 时长策略矩阵

| 时长 | 核心目标 | 脚本结构 | 视觉风格 (Visual Style) | 适用平台 |
| :--- | :--- | :--- | :--- | :--- |
| **60s** | **流量漏斗 (Hook)** | 3s 痛点 + 15s 反常识 + 10s 解法 + 2s CTA | 快切、大字报、高对比、强视觉冲击 | Shorts, TikTok, Reels |
| **5min** | **干货收藏 (Value)** | 引入 + 3 个核心观点 (案例支撑) + 总结 | 清晰图表、关键词浮现、中景、平稳节奏 | YouTube, Bilibili |
| **10-15min** | **深度拆解 (Depth)** | 背景引入 + 深度解析 (4-5 点) + 现实应用 + 互动 | 丰富多变：生图 + 思维导图 + 原文滚动 + 数据图表 | YouTube (广告变现主力) |
| **20-30min** | **沉浸精读 (Immersion)** | 纪录片式叙事 / 播客感：故事线串联全书 + 延伸 | 电影感、慢节奏氛围图、动态运镜 (Ken Burns)、微电影质感 | YouTube, Podcast (高粘性) |

## 📦 流水线阶段

### Phase 1: 🔥 爆款情报与拆书 (Viral Deconstruction)

1. **找槽点/共鸣**：从豆瓣/Goodreads 找差评（争议）和热门划线（共鸣）。
2. **情绪定位**：确定基调（搞钱焦虑、认知觉醒、治愈系、人际内耗）。
3. **提取反直觉**：找出书中颠覆常识的观点，作为 Hook。
4. **输出**：`analysis.md` (包含 5 个爆款标题、3 个核心痛点、1 个核心反直觉观点)。

### Phase 2: 📝 脚本与分镜生成 (Script & Storyboard)

根据用户选择的时长，生成对应结构的 `storyboard.json` 和 `script.md`。

**分镜表字段要求：**
```json
[
  {
    "time": "00:00-00:03",
    "type": "hook",
    "visual_description": "一个人在深夜黑暗中看着发光的手机屏幕，孤独感",
    "image_prompt": "cinematic shot, lonely man in dark room, phone screen light illuminating face, moody, hyper-realistic, 8k --ar 16:9",
    "audio_text": "深夜 2 点，你还在刷手机吗？其实你不是睡不着，你是不甘心。",
    "bgm_hint": "低沉钢琴，带有心跳声",
    "action": "slow_zoom_in",
    "tts_emotion": "whisper, anxious"
  },
  ...
]
```

**⚠️ 关键规则：**
- **Prompt 规范**：必须包含风格词（cinematic, 3d render, illustration 等）和比例 `--ar 16:9`。
- **动作标记**：针对长视频，添加 `action` 字段（pan_left, zoom_out, parallax），避免画面静止。
- **文案口语化**：禁止书面语，必须是“人话”。

### Phase 3: 🎨 资产生成 (Asset Pipeline)

*Skill 本身不直接生成图片/音频，而是生成执行指令供 AI Agent 调用：*

1. **生图指令**：根据 `image_prompt` 批量调用生图 API（如 Midjourney/DALL-E）。
   - 建议工具：`python3 scripts/generate_images.py storyboard.json`
2. **TTS 分段**：将文案切分为多个短句，标注情感。
   - 建议工具：`python3 scripts/split_for_tts.py storyboard.json`
3. **BGM 匹配**：根据情绪标签推荐 BGM 风格。

### Phase 4: 🎬 自动化合成 (Auto-Assembly)

使用 FFmpeg 组装视频。Skill 提供 `scripts/auto_compose.py` 生成合成脚本。

```bash
python3 scripts/auto_compose.py \
  --storyboard storyboard.json \
  --images-dir ./assets/images \
  --audio-dir ./assets/audio \
  --bgm ./assets/bgm.mp3 \
  --output final_video.mp4
```

**合成要求：**
- **字幕**：自动生成 `.srt`，样式要求：底部居中，黑底白字，关键帧高亮。
- **转场**：自动添加 0.5s 淡入淡出。
- **封面**：生成 3 款不同风格的封面图 Prompt。

## ✅ Done Condition

1. 已输出 `storyboard.json`，包含完整时间轴、文案、生图 Prompt。
2. 所有生图 Prompt 经过风格一致性检查。
3. 提供了可直接运行的 FFmpeg 合成脚本。
4. 提供了 3 个高点击率封面方案。

## ⚠️ 避坑指南

- **图片一致性**：确保同一视频的 Prompt 中风格词保持一致（如全部使用 `cinematic, moody lighting`）。
- **TTS 情感**：长视频不要只用一种音色，高潮部分切换情绪或语速。
- **封面法则**：封面文字不超过 5 个字，必须有大字报冲击力。
- **版权**：所有 BGM 必须使用无版权/生成式音乐，文案注明"AI 辅助生成”。
