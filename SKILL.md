     1|---
     2|name: book-video-studio
     3|description: A research-first video pipeline that turns a book into a multi-platform video matrix (YouTube/Shorts/TikTok/Bilibili). Covers: viral hook deconstruction, storyboard generation, style-locked image prompts, SRT subtitle sync, FFmpeg auto-assembly, and SEO metadata export. Use when the user wants 书单视频、拆书文案、视频分镜、多平台视频矩阵、YouTube 读书频道、TikTok 短视频.
     4|metadata:
     5|  openclaw:
     6|    emoji: "📚"
     7|    homepage: "https://github.com/5474312/book-video-studio"
     8|    requires:
     9|      anyBins: ["python3", "ffmpeg"]
    10|    primaryEnv: "OPENAI_API_KEY"
    11|  version: "0.4.0"
    12|  category: "content-generation"
    13|  author: "副业工坊"
    14|  license: "MIT"
    15|---
    16|
    17|# Book Video Studio (书单视频工坊) v4
    18|
    19|**把一本书变成一套高权重、SEO 友好的多平台视频矩阵 (YouTube / Shorts / TikTok / Bilibili)**
    20|
    21|<!-- // TODO: add video_upload.py for direct platform upload -->
    22|
    23|## Core Rules
    24|
    25|- Match the user's language (default: 中文).
    26|- Ask one question at a time.
    27|- Ask only when the answer changes genre, platform, length, or visual style.
    28|- **Save a draft only. Never publish live.**
    29|- Every claim in the script must be traceable to the book's actual content — never fabricate quotes.
    30|- **Phase 1.5 (Hook Screening) is BLOCKING** — output 5 hook variants and STOP for user approval before proceeding.
    31|- **Style Lock is mandatory** — every image/video prompt must share the same seed + character descriptor.
    32|- Every video must include a `## 参考来源` section in the script citing the book title, author, and chapter/page references.
    33|- Apply the full normalization checklist before final assembly.
    34|- Never pretend the workflow has access to licensed video/music APIs when it does not.
    35|
    36|## Operating Paths
    37|
    38|- `Path A: viral-book-video` — full pipeline from book title/author to multi-platform video matrix.
    39|- `Path B: hook-only` — generate only the 5 hook variants for user to preview.
    40|- `Path C: storyboard-only` — generate storyboard JSON from an approved script.
    41|- `Path D: asset-only` — generate image/video prompts from an existing storyboard.
    42|
    43|Default routing by book genre:
    44|- 商业/搞钱/认知类 → `deep-analysis` (10-15min YouTube, 60s Shorts cut)
    45|- 心理学/情感/治愈类 → `emotional-narrative` (5min video essay, 30s emotional hook)
    46|- 工具/方法论/实操类 → `tutorial` (step-by-step breakdown, infographic-heavy)
    47|
    48|## Accepted Inputs
    49|
    50|- book title (+ author if known)
    51|- book notes, highlights, or reading summary
    52|- specific chapter or quote to build around
    53|- a URL (Goodreads, Douban, Amazon, blog review)
    54|- a raw script the user wants converted to storyboard
    55|- an existing storyboard.json to regenerate assets
    56|
    57|## Output
    58|
    59|Create one workspace per video:
    60|`book-video-studio/YYYY-MM-DD-<book-slug>/<platform>-<duration>/`
    61|
    62|Required assets:
    63|- `source.md` — book metadata, key quotes, chapter references
    64|- `viral-analysis.md` — hook angles, emotional triggers, anti-intuition points
    65|- `script.md` — full approved script with timing markers
    66|- `storyboard.json` — structured storyboard with frame-level specs
    67|- `image-prompts.json` — batch-ready image generation prompts
    68|- `video-prompts.json` — batch-ready video generation prompts
    69|- `srt-output.srt` — synchronized subtitle file
    70|- `seo-metadata.json` — title, description, tags, chapters (YouTube)
    71|- `cover-prompt.md` — thumbnail generation prompt
    72|- `assembly.sh` — FFmpeg assembly script
    73|- `manifest.json` — pipeline state and asset registry
    74|
    75|`manifest.json` must capture:
    76|- `pathMode` (viral-book-video / hook-only / storyboard-only / asset-only)
    77|- `platform` (youtube / shorts / tiktok / bilibili)
    78|- `aspectRatio` (16:9 / 9:16 / 1:1)
    79|- `durationTarget` (60s / 5m / 15m / 30m)
    80|- `styleMode`
    81|- `hookVariant` (selected hook index)
    82|- `draftStatus`
    83|- `assetsGenerated` (list of completed asset files)
    84|
## Script Directory

Determine this SKILL.md directory as `SKILL_DIR`, then use `${SKILL_DIR}/scripts/<name>`.

| Script | Purpose |
|--------|---------|
| `scripts/auto_compose.py` | FFmpeg assembly entrypoint (`render`, `compose`, `info`, `srt`) |
| `scripts/timing_calculator.py` | Duration estimation and SRT generation engine |
| `scripts/tts_long_text.py` | **长文案一次性转语音** — 自动分段 + edge-tts 生成 + ffmpeg 拼接，无长度限制 |
| `scripts/adaptive_storyboard.py` | **自适应分镜生成器** — 读取音频时长 + 按目标节奏（默认 18s/段）拆分文案 + 关键词匹配画面 Prompt |

## Operating Paths (updated)

- `Path A: viral-book-video` — full pipeline from book title/author to multi-platform video matrix.
- `Path B: hook-only` — generate only the 5 hook variants for user to preview.
- `Path C: storyboard-only` — generate storyboard JSON from an approved script.
- `Path D: asset-only` — generate image/video prompts from an existing storyboard.
- **`Path E: script-to-video` — 已有文案 + 音频 → 自适应分镜 → 批量生图 → FFmpeg 合成视频（本次优化新增）**
    93|
    94|## Native Capability Contract
    95|
    96|This skill executes every stage itself:
    97|- viral deconstruction and hook generation via native article/script analysis
    98|- storyboard planning with platform-specific aspect ratio and safe-zone rules
    99|- image/video prompt generation with style lock enforcement
   100|- SRT subtitle sync via timing calculator script
   101|- FFmpeg assembly via auto_compose script
   102|- SEO metadata generation for YouTube algorithm optimization
   103|
   104|## Delivery Ladder
   105|
   106|Resolve video delivery in this order:
   107|1. `L0 local-assembly`: ffmpeg available locally, run `auto_compose.py` to produce final video
   108|2. `L1 cloud-render`: local ffmpeg unavailable, output `assembly.sh` + all assets for cloud rendering
   109|3. `L2 manual-handoff`: stop with exact file paths and asset descriptions when assembly cannot proceed
   110|
   111|## Author Config (EXTEND.md)
   112|
   113|The pipeline reads an optional `EXTEND.md` for author-specific preferences: channel name, CTA style, watermark text, affiliate link templates.
   114|
   115|Lookup order: project dir → `~/.config/book-video-studio/` → `~/.book-video-studio/`
   116|
   117|See [author-config.md](references/author-config.md) for the full format and field reference.
   118|
   119|## Style Resolution
   120|
   121|Resolve visual style in this order:
   122|1. explicit user instruction
   123|2. preset mode from `design.pen`
   124|3. genre-based default (see [style-engine.md](references/style-engine.md))
   125|4. custom brief
   126|
   127|Visual rendering is decided by:
   128|- `styleMode`
   129|- `platform` (drives aspect ratio and composition rules)
   130|- `durationTarget` (drives pacing and cut frequency)
   131|
   132|## Model Routing (接口与模型配置)
   133|
   134|Each pipeline stage requires specific model types. Use this routing table:
   135|
   136|| Stage | Task | Recommended Model Type | Interface / API |
   137||-------|------|----------------------|-----------------|
   138|| Phase 1-2 | 爆款拆解、钩子生成、情绪定位 | **High-Quality LLM** (deep reasoning) | OpenAI GPT-4o / Claude Sonnet / mcxapi `high_quality_general` |
   139|| Phase 3 | 脚本撰写（多平台适配） | **Creative LLM** (long-form, tone control) | mcxapi `creative` / MiniMax-M2.5 / GPT-4o |
   140|| Phase 4 | 分镜 JSON 生成 | **Structured LLM** (JSON output, strict schema) | mcxapi `coding` / qwen3-coder-plus / GPT-4o (json_schema) |
   141|| Phase 5 | 图片 Prompt → 生图 | **Text-to-Image Model** | Midjourney v6 / DALL-E 3 / Flux.1 / Stable Diffusion XL |
   142|| Phase 5b | 视频 Prompt → 生视频 | **Text-to-Video Model** | Kling AI / Runway Gen-3 / Luma Dream Machine / Pika / Sora |
   143|| Phase 6 | TTS 配音（多角色/情感） | **Text-to-Speech** | Azure TTS / ElevenLabs / OpenAI TTS / Edge-TTS |
   144|| Phase 7 | SRT 字幕 + FFmpeg 合成 | **Local Python + FFmpeg** | `scripts/auto_compose.py` + `scripts/timing_calculator.py` |
   145|| Phase 8 | SEO 元数据 + 封面 Prompt | **High-Quality LLM** (SEO knowledge) | mcxapi `high_quality_general` / GPT-4o |
   146|
   147|**Model fallback rules:**
   148|- If the primary image model fails, retry with a different seed + simplify the prompt (remove secondary elements).
   149|- If TTS emotional range is insufficient, split the script into shorter emotional segments and batch-generate.
   150|- For cost-sensitive runs: use open-weight models (Flux.1-dev, Stable Video Diffusion) on local GPU.
   151|
   152|## Path E: script-to-video (已有文案 + 音频 → 视频)

**适用场景**：已有现成文案（如公众号文章、口播稿）+ TTS 音频，需要快速生成视频。

### 流程

1. **音频时长获取** — `ffprobe` 读取精确时长
2. **自适应文案拆分** — `scripts/adaptive_storyboard.py` 按目标节奏（默认 18s/段）自动拆分，优先在句号/感叹号/问号处断句
3. **分镜 JSON 生成** — 输出 `storyboard.json` + `image_prompts.json`
   - 每段自动匹配关键词 → 画面 Prompt（KEYWORD_MAP）
   - 统一风格锁（cinematic, dark moody, 16:9）
4. **批量生图** — 按 `image_prompts.json` 批量生成画面
5. **TTS 配音** — `scripts/tts_long_text.py` 长文案自动分段生成（无长度限制）
6. **FFmpeg 合成** — 图片 Ken Burns 运镜 + SRT 字幕 + 音频 + BGM

### 命令示例

```bash
# Step 1: 生成分镜（自动读取音频时长）
python3 scripts/adaptive_storyboard.py \
    --input script.txt --audio audio.mp3 \
    --segment-duration 18 --output-dir ./output

# Step 2: 长文案转语音（如音频未准备好）
python3 scripts/tts_long_text.py \
    --input script.txt --output audio.mp3 --voice xiaoxiao

# Step 3: 批量生图后，FFmpeg 合成
python3 scripts/auto_compose.py compose \
    --storyboard output/storyboard.json \
    --output final.mp4
```

### 参数建议

| 参数 | 推荐值 | 说明 |
|------|--------|------|
| `segment-duration` | 15-20s | 每图时长，15-20 秒最佳（同类型账号标准） |
| `voice` | xiaoxiao | 女声口播最推荐，yunxi 男声活力 |
| `rate` | +0% ~ +10% | 语速微调，商业认知类推荐 +5% |

### 画面数量计算

```
画面数 = 音频时长(秒) / segment-duration
例: 1054s / 18s ≈ 58 张图
```

---

## Execution
   153|
   154|Run the video through these phases:
   155|
   156|1. **intake and book deconstruction** — extract core thesis, key quotes, chapter structure, controversial/emotional points.
   157|
   158|2. **viral analysis and strategic clarification** — analyze Douban/Goodreads reviews for pain points (差评=争议) and popular highlights (划线=共鸣). Determine emotional positioning.
   159|
   160|3. **hook generation (⛔ BLOCKING)** — generate **5 hook variants** across dimensions:
   161|   - 痛点型 (pain point)
   162|   - 反常识型 (anti-intuition)
   163|   - 利益型 (benefit-driven)
   164|   - 悬念型 (suspense)
   165|   - 数据型 (data/shocking stat)
   166|   
   167|   **STOP here.** Present all 5 hooks with estimated CTR potential. Ask the user to select or combine.
   168|
   169|4. **script writing** — based on selected hook, write the full script with:
   170|   - **Platform-specific pacing**: see [platform-copy.md](references/platform-copy.md)
   171|   - **Safe Zone rules** (9:16): keep text clear of TikTok UI overlays
   172|   - **Word count limits**: 60s ≤ 260 chars, 5min ≤ 1200 chars, 15min ≤ 3500 chars
   173|   - **Hook-Body-CTA structure**: ensure smooth transitions
   174|
   175|5. **storyboard generation** — produce `storyboard.json` with:
   176|   - frame-level breakdown (visual description + audio text + duration)
   177|   - **Style Lock**: append character descriptor + seed to every visual prompt
   178|   - **Platform aspect ratio**: `--ar 16:9` (YouTube) or `--ar 9:16` (Shorts/TikTok)
   179|   - `duration_estimated` per frame based on speech rate (~4.5 Chinese chars/sec)
   180|
   181|7. **asset prompt generation** — produce batch-ready prompts:
   182|   - `image-prompts.json`: one per storyboard frame (for Midjourney/Flux/SDXL)
   183|   - `video-prompts.json`: motion-enhanced variants (for Kling/Runway/Luma)
   184|   - `cover-prompt.md`: 3 thumbnail variants optimized for high CTR
   185|   - **Quality gate**: every prompt passes the two-tier check from [style-engine.md](references/style-engine.md)
   186|
   187|8. **asset generation coordination** — when models are available:
   188|   - batch-generate images from `image-prompts.json`
   189|   - batch-generate video clips from `video-prompts.json` (if video model API keys available)
   190|   - generate TTS audio from script text (`audio_text` per frame)
   191|   - generate SRT subtitles via `scripts/timing_calculator.py`
   192|
   193|9. **assembly and delivery** — run `python3 "${SKILL_DIR}/scripts/auto_compose.py" compose --storyboard storyboard.json`
   194|
   195|   **Pre-assembly compliance gate (BLOCKING):**
   196|   1. **Verify Style Lock consistency**: all image prompts share the same seed + character descriptor. Check with `grep`.
   197|   2. **Verify word count vs duration**: no frame's text exceeds `duration_estimated * 4.5` Chinese chars.
   198|   3. **Verify Safe Zone compliance** (for 9:16): no critical visual elements in bottom 30% or top 20%.
   199|   4. **Verify SRT timecode accuracy**: total subtitle duration ≈ total storyboard duration.
   200|   5. **Verify FFmpeg assets exist**: all referenced image/video/audio files are present.
   201|
   202|   Output a checklist with ✅/❌. Fix any ❌ before running compose.
   203|
   204|   **Known issue: FFmpeg image duration mismatch.**
   205|   If an image's display time doesn't match the TTS audio length, the video will desync. Fix: use `auto_compose.py`'s built-in timing calculator to pad/crop images dynamically. Detection: `python3 scripts/timing_calculator.py verify --storyboard storyboard.json --audio-dir audio/`
   206|
   207|   **Known issue: SRT encoding breaks on special characters.**
   208|   Chinese punctuation (，。！？) and emoji in SRT files can cause rendering issues on some platforms. Fix: run SRT through UTF-8 normalization and replace full-width punctuation with half-width equivalents where needed.
   209|
   210|   **Known issue: Thumbnail CTR drops with cluttered compositions.**
   211|   AI-generated covers tend to be too busy. Fix: enforce the "Rule of 3" — max 3 visual elements (background + subject + text overlay). See [style-engine.md](references/style-engine.md) thumbnail section.
   212|
   213|10. **SEO metadata export and multi-platform adaptation** — generate platform-specific metadata:
   214|
   215|   **YouTube (16:9, 10-15min):**
   216|   - 3 SEO title variants (keyword-optimized, emoji-enhanced)
   217|   - Description with: hook summary + affiliate link placeholder + **Chapters/Timestamps**
   218|   - 20 high-weight tags
   219|   - End Screen markers (last 20s: subscribe + next video)
   220|   
   221|   **Shorts/TikTok (9:16, 60s):**
   222|   - Hook-optimized title (first 3 words must grab attention)
   223|   - Hashtag strategy: 3 broad + 5 niche + 2 branded
   224|   - No chapters needed (too short)
   225|   - CTA: "Follow for more" + comment prompt
   226|   
   227|   **Bilibili (16:9, 5-15min):**
   228|   - Title with B站-native style (「」《》 brackets, emotional keywords)
   229|   - Description with 标签 (tags) + 互动引导
   230|   - No affiliate links (not applicable on B站)
   231|
   232|Phase 9 only executes when the user explicitly requests it.
   233|
   234|Use the execution contract in [execution-contract.md](references/execution-contract.md).
   235|Use the platform copy specs in [platform-copy.md](references/platform-copy.md).
   236|Use the style engine in [style-engine.md](references/style-engine.md).
   237|
   238|## Done Condition
   239|
   240|The skill is complete only when all of these hold:
   241|- Phase 1.5 hook screening was presented and user-approved
   242|- the script's tone matches the book's genre and target audience
   243|- Phase 5 compliance check passed (zero violations in script-clean.md)
- the storyboard JSON is valid and contains all required fields
   244|- every visual prompt passes Style Lock (same seed + character descriptor)
   245|- word count per frame ≤ `duration_estimated * 4.5` Chinese characters
   246|- SRT timecodes align with total audio duration (±2s tolerance)
   247|- FFmpeg assembly completed without errors
   248|- SEO metadata matches the actual video content and platform requirements
   249|- the video reads as informative before it reads as promotional
   250|- the workflow can stop safely at the highest-quality completed artifact if a later handoff fails
   251|- if Phase 9 was triggered, platform copies follow [platform-copy.md](references/platform-copy.md) and manifest includes their entries
   252|