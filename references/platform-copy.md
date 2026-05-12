# Platform Copy Specs — 多平台适配矩阵

## Overview

This document defines platform-specific rules for script pacing, visual composition, SEO metadata, and engagement strategy. Always apply these rules when generating content for a specific platform.

## Platform Matrix

| Dimension | YouTube (长视频) | YouTube Shorts | TikTok | Bilibili |
|-----------|-----------------|---------------|--------|----------|
| Aspect Ratio | 16:9 | 9:16 | 9:16 | 16:9 |
| Resolution | 1920×1080 | 1080×1920 | 1080×1920 | 1920×1080 |
| Target Duration | 10-15 min | 30-60s | 15-60s | 5-10 min |
| Script Pacing | 深度展开，4-5 观点 | 极速，1 核心点 | 极速，1 核心点 | 干货密集，3-4 观点 |
| Word Count | ≤ 3500 chars | ≤ 260 chars | ≤ 260 chars | ≤ 2000 chars |
| Cut Frequency | Every 8-12s | Every 2-3s | Every 2-3s | Every 5-8s |
| Safe Zone | Standard 3% border | Top 20% + Bottom 30% | Top 20% + Bottom 30% + Right 15% | Standard 5% border |
| Font Size | 36px | 42px | 44px | 36px |
| BGM Style | Ambient / Lo-fi | Trending / Upbeat | Trending / Viral | Anime / Lo-fi / 电子 |

---

## YouTube (16:9, 10-15min)

### Script Structure
```
00:00-00:30  Hook (痛点/反常识)
00:30-02:00  Background & context
02:00-05:00  Core Point 1 + example
05:00-08:00  Core Point 2 + example
08:00-11:00  Core Point 3 + example
11:00-13:00  Synthesis & practical application
13:00-14:00  CTA + subscribe prompt
14:00-15:00  End Screen (recommended videos)
```

### SEO Metadata
```json
{
  "title_variants": [
    "读完这本书，我终于搞懂了XXX的底层逻辑 📖",
    "为什么聪明人都在读XXX？3个颠覆认知的观点",
    "别再XXX了！这本书告诉你真相（深度拆解）"
  ],
  "description_template": "📚 书名：{book_title}\n👤 作者：{author}\n\n在这期视频中，我们深度拆解了《{book_title}》的核心观点。如果你是XXX（目标受众），这本书可能会改变你对XXX的看法。\n\n⏰ Chapters:\n00:00 为什么读这本书？\n{auto_generated_chapters}\n\n📖 购买链接（Affiliate）: {affiliate_link}\n\n#读书分享 #认知觉醒 #书单推荐",
  "tags_count": 20,
  "tag_categories": {
    "core": ["读书", "书单", "{book_title}", "{author}"],
    "topic": ["认知提升", "个人成长", "思维方式", "干货"],
    "search": ["值得读的书", "2024必读书单", "高分好书推荐"],
    "branded": ["副业工坊", "读书频道名"]
  }
}
```

### Chapters/Timestamps
Generate AFTER video assembly. Format:
```
00:00 引言：为什么这本书改变了我的认知？
01:30 观点一：{core_point_1}
03:45 案例：{example_1}
05:20 观点二：{core_point_2}
08:10 观点三：{core_point_3}
10:30 现实应用：如何把这些用在生活中？
12:45 总结与推荐
```

### Thumbnail Strategy
- **Composition**: Subject face (extreme emotion) + book cover + 3-5 character text overlay
- **Colors**: High contrast, one saturated accent color
- **Text examples**: "真相揭秘", "别再被骗", "颠覆认知", "搞钱必看"
- **Don't**: Use busy video frames, small text, complex backgrounds

### End Screen (last 20s)
- Subscribe button placeholder
- "Watch next" video recommendation placeholder
- Keep visual simple so overlay buttons are visible

---

## YouTube Shorts / TikTok (9:16, 15-60s)

### Script Structure (60s)
```
00:00-00:03  HOOK (3秒抓注意力，必须强)
00:03-00:15  Problem / Pain point amplification
00:15-00:35  The counter-intuitive insight / solution
00:35-00:50  Proof / Example
00:50-00:60  CTA: Follow / Comment / Save
```

### Safe Zone (9:16) — CRITICAL
```
┌─────────────────────┐
│   TOP 20%           │  ← TikTok logo / Like button area
│   AVOID TEXT HERE   │
├─────────────────────┤
│                     │
│   MIDDLE 50%        │  ← SAFE ZONE for text & key visuals
│   (Primary content) │
│                     │
├─────────────────────┤
│   BOTTOM 30%        │  ← Comment / Caption / Music area
│   SUBTITLES ONLY    │  ← Keep text minimal here
└─────────────────────┘
         ↕
   Left 10% / Right 15% also avoid (side buttons on TikTok)
```

### Title / Caption
- **YouTube Shorts**: First 3 words must hook. "如果你经常焦虑..." ✅ "这本书讲了三个观点..." ❌
- **TikTok**: Hook + question. Example: "读完这本书我沉默了...你经历过这种情况吗？"

### Hashtag Strategy
```
# Broad (reach):     #读书 #书单 #知识分享 #自我提升
# Niche (targeting): #认知觉醒 #搞钱思维 #心理学书单
# Branded (identity): #副业工坊读好书 #今日读书
Total: 8-12 hashtags (not too many, not too few)
```

### Visual Rules (9:16)
- **No horizontal content**: Don't crop 16:9 video into 9:16. Generate native 9:16.
- **Fast cuts**: Every 2-3 seconds, change the visual.
- **Dynamic text**: Animate key words (zoom, color change) to maintain attention.
- **No dead space**: Every frame must have visual interest.

---

## Bilibili (16:9, 5-10min)

### Script Structure
```
00:00-00:20  Hook（B站风格：悬念/共鸣型开头）
00:20-01:30  背景引入 + 为什么做这期
01:30-04:00  核心内容 1-2（干货密集）
04:00-07:00  核心内容 3-4 + 案例
07:00-08:30  个人感受 + 实操建议
08:30-09:30  互动引导（三连 + 评论区讨论）
09:30-10:00  下期预告
```

### Title Style
B站标题有独特的「标题党」文化，但不是纯标题党：
- 使用《》「」包裹书名和关键词
- 加入情感词：「看完沉默了」「颠覆认知」「太狠了」
- 加入数字：「3个观点」「5分钟」
- 示例：「看完《XXX》我沉默了...这3个观点颠覆了我的认知」

### Description / Tags
```
书籍信息：《{book_title}》/ {author} / {publisher}

视频标签（Tag）：
读书分享 | 书单推荐 | 认知提升 | {book_title} | {author} | 
个人成长 | 干货 | {genre} | 副业工坊

互动引导：
"你读过这本书吗？在评论区分享你的看法！"
"觉得有用请一键三连 ⭐"
```

### B站 Special Rules
- ❌ No affiliate links (not applicable)
- ✅ Add 「弹幕互动点」— moments where viewers can comment
- ✅ Use B站 native memes/references when appropriate
- ✅ 结尾加"一键三连"引导
- ✅ 封面图可以稍微"标题党"一些（B站用户对封面党接受度更高）

---

## Cross-Platform Adaptation Rules

### When Repurposing Content
If generating for multiple platforms from one book:

1. **Generate the long-form (YouTube 15min) first** — this is the master script.
2. **Extract the strongest hook** — use it for Shorts/TikTok.
3. **Condense the core points** — pick the single most impactful point for 60s.
4. **Adjust pacing** — same content, different speed.
5. **Regenerate visuals** — 16:9 images ≠ 9:16 images. Must re-prompt with `--ar 9:16`.
6. **Regenerate metadata** — platform-specific titles, tags, descriptions.

### What NOT to Cross-Post
- ❌ Don't upload a horizontal video to TikTok (will get cropped badly)
- ❌ Don't upload a vertical video to YouTube (will look amateurish)
- ❌ Don't use YouTube SEO tags on TikTok (irrelevant algorithm)
- ❌ Don't use TikTok-style fast cuts for a 15min YouTube video (exhausting)
