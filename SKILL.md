---
name: book-video-studio
description: 书单视频全自动流水线：拆书提取爆点 -> 交互筛选钩子 -> 多平台分镜 (16:9/9:16) -> 风格锁定 -> 时长估算 -> SRT 生成 -> 视频组装。Use for 书单视频制作、YouTube 读书频道、TikTok Shorts、自动化视频生成。
metadata:
  openclaw:
    emoji: "📚"
    homepage: "https://github.com/5474312/book-video-studio"
    requires:
      anyBins: ["python3", "ffmpeg"]
  version: "0.2.0"
  category: "content-generation"
  author: "副业工坊"
  license: "MIT"
---

# Book Video Studio (书单视频工坊) v2

**把一本书变成一套多平台视频矩阵 (YouTube / Shorts / TikTok)**

## 🔥 核心理念 (v2 升级)

- **拒绝一次性盲盒**：实行 **"钩子先行"** 策略，先过 3s 开头，再做后续内容。
- **视觉一致性 (Style Lock)**：全片角色和画风必须锁定，禁止随机发散。
- **多平台自适应**：横屏 (16:9) 做 YouTube，竖屏 (9:16) 做 Shorts/TikTok，自动适配构图。
- **音画对齐 (Timing Sync)**：基于语速自动估算时长，生成 SRT 字幕文件，确保 FFmpeg 合成严丝合缝。

## 🎬 时长与平台策略矩阵

| 规格 | 核心目标 | 脚本结构 | 视觉风格 (Visual Style) | 适用平台 |
| :--- | :--- | :--- | :--- | :--- |
| **60s** | **流量漏斗 (Hook)** | 3s 痛点 + 15s 反常识 + 10s 解法 + 2s CTA | 快切、大字报 (Safe Zone: 避开底部字幕区)、高对比 | Shorts, TikTok, Reels |
| **5min** | **干货输出** | 引入 - 3 个核心观点 - 总结 | 清晰图表、关键词浮现、中景、平稳节奏 | YouTube, Bilibili, Video号 |
| **10-15min** | **深度拆解** | 背景引入 - 深度解析 (4-5 点) - 现实应用 | 丰富多变：生图 + 思维导图 + 原文滚动 + 数据图表 | YouTube (广告变现主力) |
| **20-30min** | **沉浸精读** | 纪录片式叙事/播客感：故事线串联全书 | 电影感：慢节奏氛围图，人物场景重现，Ken Burns 运镜 | YouTube, Podcast |

## 📦 流水线阶段 (Execution Workflow)

### Phase 1: 🔥 爆款情报与拆书 (Viral Deconstruction)
1.  **找槽点/共鸣**：从豆瓣/Goodreads 找差评（争议）和热门划线（共鸣）。
2.  **情绪定位**：确定基调（搞钱焦虑、认知觉醒、治愈系）。
3.  **提取反直觉**：找出书中颠覆常识的观点，作为 Hook 素材。

### Phase 1.5: 🎣 交互钩子筛选 (Interactive Hook Screening) ⛔ **BLOCKING STEP**
- **规则**：生成 **5 个不同维度的 3 秒开头**（痛点型/反常识型/利益型/悬念型/数据型）。
- **操作**：**输出这 5 个钩子后停止**，询问大哥选择哪一个（或组合）。
- **原因**：开头定生死，必须由人工把关或通过反馈修正，避免生成垃圾长视频。

### Phase 2: 📝 脚本与分镜生成 (Script & Storyboard)
基于选定钩子，生成 `storyboard.json`。

**多平台适配规则 (Platform Adaptation):**
- **Aspect Ratio**: 用户指定 `TikTok/Shorts` -> Prompt 后缀强制 `--ar 9:16`; `YouTube` -> `--ar 16:9`.
- **Safe Zone (9:16 专用)**: 
    - 文案禁止遮挡：底部 30% 预留给字幕，顶部 20% 预留给 TikTok UI 按钮。
    - 生图 Prompt 提示：`centered subject, avoid top right and bottom center details`.

**视觉一致性规则 (Style Lock):**
- **Character Lock**: 定义一个通用主角描述 (如 `a young asian man, white t-shirt, minimalist style`)，强制附加到每一帧的 Prompt 后面。
- **Seed Consistency**: 生成一个随机 `seed` (如 `--seed 42`)，全片通用。

**分镜表 JSON 字段标准:**
```json
[
  {
    "time": "00:00-00:03",
    "visual_description": "一个人在深夜黑暗中看着发光的手机屏幕",
    "image_prompt": "cinematic shot, [Character Lock] looking at phone in dark room, blue screen light --ar 16:9 --seed 42",
    "audio_text": "深夜 2 点，你还在刷手机吗？",
    "duration_estimated": 2.5, 
    "srt_index": 1,
    "srt_time": "00:00:00,000 --> 00:00:02,500",
    "action": "zoom_in"
  },
  ...
]
```

### Phase 3: 🎨 资产生成 (Asset Pipeline)
- **生图指令**: 根据 `image_prompt` 批量调用生图 API。
- **TTS 分段**: 根据 `audio_text` 生成音频文件，命名为 `tts_{index}.mp3`.
- **SRT 生成**: 输出配套的 `.srt` 字幕文件。

### Phase 4: 🎬 自动化合成 (Auto-Assembly)
使用 FFmpeg 组装。
- **命令**: `python3 scripts/auto_compose.py --storyboard storyboard.json --platform youtube`
- **合成要求**: 
    - 图片根据 `duration_estimated` 精确裁剪/缩放。
    - 自动添加 Ken Burns 运镜效果（针对静态图）。
    - 烧录 SRT 字幕 (字体：黑体/思源黑体，底部居中，描边)。

## ✅ Done Condition
1. **钩子通过**：Phase 1.5 已获得用户确认。
2. **分镜输出**：`storyboard.json` 包含完整时间轴、估算时长、SRT 时间码。
3. **平台适配**：Prompt 比例和构图已按目标平台调整。
4. **风格锁定**：所有 Prompt 包含统一的 Character Lock 和 Seed。
5. **SRT 就绪**：提供 `.srt` 内容，可直接用于字幕烧录。

## ⚠️ 避坑指南 (v2 Update)
- **字数陷阱**：中文语速约 4.5 字/秒。60s 视频文案绝不能超过 260 字！AI 常写多，必须砍！
- **9:16 构图**：生成竖屏图时，AI 容易把人放在边缘。必须加 `centered composition` 到 Prompt。
- **TTS 停顿**：在 JSON 中标注 `pause` 字段，合成时插入静音，模拟人类呼吸感。
- **版权**：BGM 必须无版权或 AI 生成；封面字体使用思源黑体/站酷系列（免费商用）。
