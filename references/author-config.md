# Author Config — 作者专属配置

Create an `EXTEND.md` file in your project directory to customize the pipeline with your channel's identity.

## Location (checked in order)
1. `project_dir/EXTEND.md`
2. `~/.config/book-video-studio/EXTEND.md`
3. `~/.book-video-studio/EXTEND.md`

## Format

```markdown
---
channel_name: "副业工坊·读书频道"
cta_style: "soft"
watermark_text: "@fuyegongfang"
affiliate_link_template: "https://amzn.to/{asin}"
bilibili_space: "https://space.bilibili.com/{uid}"
---

## CTA (Call to Action)

# For YouTube:
如果这期视频对你有帮助，请点赞订阅。
每周更新一本好书的深度拆解。

# For TikTok/Shorts:
关注我，每天一本书的精华 📚

# For Bilibili:
觉得有用请一键三连！
评论区聊聊你读这本书的感受 👇

## Channel Branding

- 频道口号: "让AI为你拆书，让好书改变认知"
- 更新频率: 每周2-3期
- 目标受众: 25-40岁，有自我提升需求的知识工作者
```

## CTA Styles

| Style | Description | Best For |
|-------|-------------|----------|
| `soft` | 温和引导，不强势 | 知识分享、读书频道 |
| `direct` | 直接明确 | 教程、工具类 |
| `emotional` | 情感共鸣式 | 心理学、治愈类 |
| `humorous` | 幽默调侃式 | 轻松话题、年轻化内容 |

## Fields Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `channel_name` | string | Yes | Your channel name |
| `cta_style` | enum | No | See CTA styles above (default: soft) |
| `watermark_text` | string | No | Watermark text on videos |
| `affiliate_link_template` | string | No | Amazon affiliate link template |
| `bilibili_space` | string | No | Bilibili channel URL |
| `custom_rules` | list | No | Additional rules for this channel |
