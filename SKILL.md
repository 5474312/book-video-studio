---
name: book-video-studio
description: A research-first video pipeline that turns a book into a multi-platform video matrix (YouTube/Shorts/TikTok/Bilibili). Covers: viral hook deconstruction, storyboard generation, style-locked image prompts, SRT subtitle sync, FFmpeg auto-assembly, and SEO metadata export. Use when the user wants 书单视频、拆书文案、视频分镜、多平台视频矩阵、YouTube 读书频道、TikTok 短视频.
metadata:
  openclaw:
    emoji: "📚"
    homepage: "https://github.com/5474312/book-video-studio"
    requires:
      anyBins: ["python3", "ffmpeg"]
    primaryEnv: "OPENAI_API_KEY"
  version: "0.4.0"
  category: "content-generation"
  author: "副业工坊"
  license: "MIT"
---

# Book Video Studio (书单视频工坊) v4

**把一本书变成一套高权重、SEO 友好的多平台视频矩阵 (YouTube / Shorts / TikTok / Bilibili)**

<!-- // TODO: add video_upload.py for direct platform upload -->

## Core Rules

- Match the user's language (default: 中文).
- Ask one question at a time.
- Ask only when the answer changes genre, platform, length, or visual style.
- **Save a draft only. Never publish live.**
- Every claim in the script must be traceable to the book's actual content — never fabricate quotes.
- **Phase 1.5 (Hook Screening) is BLOCKING** — output 5 hook variants and STOP for user approval before proceeding.
- **Style Lock is mandatory** — every image/video prompt must share the same seed + character descriptor.
- Every video must include a `## 参考来源` section in the script citing the book title, author, and chapter/page references.
- Apply the full normalization checklist before final assembly.
- Never pretend the workflow has access to licensed video/music APIs when it does not.

## Operating Paths

- `Path A: viral-book-video` — full pipeline from book title/author to multi-platform video matrix.
- `Path B: hook-only` — generate only the 5 hook variants for user to preview.
- `Path C: storyboard-only` — generate storyboard JSON from an approved script.
- `Path D: asset-only` — generate image/video prompts from an existing storyboard.

Default routing by book genre:
- 商业/搞钱/认知类 → `deep-analysis` (10-15min YouTube, 60s Shorts cut)
- 心理学/情感/治愈类 → `emotional-narrative` (5min video essay, 30s emotional hook)
- 工具/方法论/实操类 → `tutorial` (step-by-step breakdown, infographic-heavy)

## Accepted Inputs

- book title (+ author if known)
- book notes, highlights, or reading summary
- specific chapter or quote to build around
- a URL (Goodreads, Douban, Amazon, blog review)
- a raw script the user wants converted to storyboard
- an existing storyboard.json to regenerate assets

## Output

Create one workspace per video:
`book-video-studio/YYYY-MM-DD-<book-slug>/<platform>-<duration>/`

Required assets:
- `source.md` — book metadata, key quotes, chapter references
- `viral-analysis.md` — hook angles, emotional triggers, anti-intuition points
- `script.md` — full approved script with timing markers
- `storyboard.json` — structured storyboard with frame-level specs
- `image-prompts.json` — batch-ready image generation prompts
- `video-prompts.json` — batch-ready video generation prompts
- `srt-output.srt` — synchronized subtitle file
- `seo-metadata.json` — title, description, tags, chapters (YouTube)
- `cover-prompt.md` — thumbnail generation prompt
- `assembly.sh` — FFmpeg assembly script
- `manifest.json` — pipeline state and asset registry

`manifest.json` must capture:
- `pathMode` (viral-book-video / hook-only / storyboard-only / asset-only)
- `platform` (youtube / shorts / tiktok / bilibili)
- `aspectRatio` (16:9 / 9:16 / 1:1)
- `durationTarget` (60s / 5m / 15m / 30m)
- `styleMode`
- `hookVariant` (selected hook index)
- `draftStatus`
- `assetsGenerated` (list of completed asset files)

## Script Directory

Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>`.

| Script | Purpose |
|--------|---------|
| `scripts/auto_compose.py` | FFmpeg assembly entrypoint (`render`, `compose`, `info`, `srt`) |
| `scripts/timing_calculator.py` | Duration estimation and SRT generation engine |

## Native Capability Contract

This skill executes every stage itself:
- viral deconstruction and hook generation via native article/script analysis
- storyboard planning with platform-specific aspect ratio and safe-zone rules
- image/video prompt generation with style lock enforcement
- SRT subtitle sync via timing calculator script
- FFmpeg assembly via auto_compose script
- SEO metadata generation for YouTube algorithm optimization

## Delivery Ladder

Resolve video delivery in this order:
1. `L0 local-assembly`: ffmpeg available locally, run `auto_compose.py` to produce final video
2. `L1 cloud-render`: local ffmpeg unavailable, output `assembly.sh` + all assets for cloud rendering
3. `L2 manual-handoff`: stop with exact file paths and asset descriptions when assembly cannot proceed

## Author Config (EXTEND.md)

The pipeline reads an optional `EXTEND.md` for author-specific preferences: channel name, CTA style, watermark text, affiliate link templates.

Lookup order: project dir → `~/.config/book-video-studio/` → `~/.book-video-studio/`

See [author-config.md](references/author-config.md) for the full format and field reference.

## Style Resolution

Resolve visual style in this order:
1. explicit user instruction
2. preset mode from `design.pen`
3. genre-based default (see [style-engine.md](references/style-engine.md))
4. custom brief

Visual rendering is decided by:
- `styleMode`
- `platform` (drives aspect ratio and composition rules)
- `durationTarget` (drives pacing and cut frequency)

## Model Routing (接口与模型配置)

Each pipeline stage requires specific model types. Use this routing table:

| Stage | Task | Recommended Model Type | Interface / API |
|-------|------|----------------------|-----------------|
| Phase 1-2 | 爆款拆解、钩子生成、情绪定位 | **High-Quality LLM** (deep reasoning) | OpenAI GPT-4o / Claude Sonnet / mcxapi `high_quality_general` |
| Phase 3 | 脚本撰写（多平台适配） | **Creative LLM** (long-form, tone control) | mcxapi `creative` / MiniMax-M2.5 / GPT-4o |
| Phase 4 | 分镜 JSON 生成 | **Structured LLM** (JSON output, strict schema) | mcxapi `coding` / qwen3-coder-plus / GPT-4o (json_schema) |
| Phase 5 | 图片 Prompt → 生图 | **Text-to-Image Model** | Midjourney v6 / DALL-E 3 / Flux.1 / Stable Diffusion XL |
| Phase 5b | 视频 Prompt → 生视频 | **Text-to-Video Model** | Kling AI / Runway Gen-3 / Luma Dream Machine / Pika / Sora |
| Phase 6 | TTS 配音（多角色/情感） | **Text-to-Speech** | Azure TTS / ElevenLabs / OpenAI TTS / Edge-TTS |
| Phase 7 | SRT 字幕 + FFmpeg 合成 | **Local Python + FFmpeg** | `scripts/auto_compose.py` + `scripts/timing_calculator.py` |
| Phase 8 | SEO 元数据 + 封面 Prompt | **High-Quality LLM** (SEO knowledge) | mcxapi `high_quality_general` / GPT-4o |

**Model fallback rules:**
- If the primary image model fails, retry with a different seed + simplify the prompt (remove secondary elements).
- If TTS emotional range is insufficient, split the script into shorter emotional segments and batch-generate.
- For cost-sensitive runs: use open-weight models (Flux.1-dev, Stable Video Diffusion) on local GPU.

## Execution

Run the video through these phases:

1. **intake and book deconstruction** — extract core thesis, key quotes, chapter structure, controversial/emotional points.

2. **viral analysis and strategic clarification** — analyze Douban/Goodreads reviews for pain points (差评=争议) and popular highlights (划线=共鸣). Determine emotional positioning.

3. **hook generation (⛔ BLOCKING)** — generate **5 hook variants** across dimensions:
   - 痛点型 (pain point)
   - 反常识型 (anti-intuition)
   - 利益型 (benefit-driven)
   - 悬念型 (suspense)
   - 数据型 (data/shocking stat)
   
   **STOP here.** Present all 5 hooks with estimated CTR potential. Ask the user to select or combine.

4. **script writing** — based on selected hook, write the full script with:
   - **Platform-specific pacing**: see [platform-copy.md](references/platform-copy.md)
   - **Safe Zone rules** (9:16): keep text clear of TikTok UI overlays
   - **Word count limits**: 60s ≤ 260 chars, 5min ≤ 1200 chars, 15min ≤ 3500 chars
   - **Hook-Body-CTA structure**: ensure smooth transitions

5. **storyboard generation** — produce `storyboard.json` with:
   - frame-level breakdown (visual description + audio text + duration)
   - **Style Lock**: append character descriptor + seed to every visual prompt
   - **Platform aspect ratio**: `--ar 16:9` (YouTube) or `--ar 9:16` (Shorts/TikTok)
   - `duration_estimated` per frame based on speech rate (~4.5 Chinese chars/sec)

6. **asset prompt generation** — produce batch-ready prompts:
   - `image-prompts.json`: one per storyboard frame (for Midjourney/Flux/SDXL)
   - `video-prompts.json`: motion-enhanced variants (for Kling/Runway/Luma)
   - `cover-prompt.md`: 3 thumbnail variants optimized for high CTR
   - **Quality gate**: every prompt passes the two-tier check from [style-engine.md](references/style-engine.md)

7. **asset generation coordination** — when models are available:
   - batch-generate images from `image-prompts.json`
   - batch-generate video clips from `video-prompts.json` (if video model API keys available)
   - generate TTS audio from script text (`audio_text` per frame)
   - generate SRT subtitles via `scripts/timing_calculator.py`

8. **assembly and delivery** — run `python3 "${SKILL_DIR}/scripts/auto_compose.py" compose --storyboard storyboard.json`

   **Pre-assembly compliance gate (BLOCKING):**
   1. **Verify Style Lock consistency**: all image prompts share the same seed + character descriptor. Check with `grep`.
   2. **Verify word count vs duration**: no frame's text exceeds `duration_estimated * 4.5` Chinese chars.
   3. **Verify Safe Zone compliance** (for 9:16): no critical visual elements in bottom 30% or top 20%.
   4. **Verify SRT timecode accuracy**: total subtitle duration ≈ total storyboard duration.
   5. **Verify FFmpeg assets exist**: all referenced image/video/audio files are present.

   Output a checklist with ✅/❌. Fix any ❌ before running compose.

   **Known issue: FFmpeg image duration mismatch.**
   If an image's display time doesn't match the TTS audio length, the video will desync. Fix: use `auto_compose.py`'s built-in timing calculator to pad/crop images dynamically. Detection: `python3 scripts/timing_calculator.py verify --storyboard storyboard.json --audio-dir audio/`

   **Known issue: SRT encoding breaks on special characters.**
   Chinese punctuation (，。！？) and emoji in SRT files can cause rendering issues on some platforms. Fix: run SRT through UTF-8 normalization and replace full-width punctuation with half-width equivalents where needed.

   **Known issue: Thumbnail CTR drops with cluttered compositions.**
   AI-generated covers tend to be too busy. Fix: enforce the "Rule of 3" — max 3 visual elements (background + subject + text overlay). See [style-engine.md](references/style-engine.md) thumbnail section.

9. **SEO metadata export and multi-platform adaptation** — generate platform-specific metadata:

   **YouTube (16:9, 10-15min):**
   - 3 SEO title variants (keyword-optimized, emoji-enhanced)
   - Description with: hook summary + affiliate link placeholder + **Chapters/Timestamps**
   - 20 high-weight tags
   - End Screen markers (last 20s: subscribe + next video)
   
   **Shorts/TikTok (9:16, 60s):**
   - Hook-optimized title (first 3 words must grab attention)
   - Hashtag strategy: 3 broad + 5 niche + 2 branded
   - No chapters needed (too short)
   - CTA: "Follow for more" + comment prompt
   
   **Bilibili (16:9, 5-15min):**
   - Title with B站-native style (「」《》 brackets, emotional keywords)
   - Description with 标签 (tags) + 互动引导
   - No affiliate links (not applicable on B站)

Phase 9 only executes when the user explicitly requests it.

Use the execution contract in [execution-contract.md](references/execution-contract.md).
Use the platform copy specs in [platform-copy.md](references/platform-copy.md).
Use the style engine in [style-engine.md](references/style-engine.md).

## Done Condition

The skill is complete only when all of these hold:
- Phase 1.5 hook screening was presented and user-approved
- the script's tone matches the book's genre and target audience
- the storyboard JSON is valid and contains all required fields
- every visual prompt passes Style Lock (same seed + character descriptor)
- word count per frame ≤ `duration_estimated * 4.5` Chinese characters
- SRT timecodes align with total audio duration (±2s tolerance)
- FFmpeg assembly completed without errors
- SEO metadata matches the actual video content and platform requirements
- the video reads as informative before it reads as promotional
- the workflow can stop safely at the highest-quality completed artifact if a later handoff fails
- if Phase 9 was triggered, platform copies follow [platform-copy.md](references/platform-copy.md) and manifest includes their entries
