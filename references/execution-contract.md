     1|# Execution Contract — 执行契约与避坑指南
     2|
     3|## Contract Overview
     4|
     5|This document defines the rules, constraints, and quality gates that every execution of the Book Video Studio pipeline must follow. It exists to prevent common failure modes in AI video production.
     6|
     7|## Phase-by-Phase Gates
     8|
     9|### Phase 1-2: Book Deconstruction
    10|- [ ] Source is verified (book title, author, edition)
    11|- [ ] At least 3 key quotes identified with chapter references
    12|- [ ] Emotional positioning determined (搞钱焦虑/认知觉醒/治愈系)
    13|- [ ] At least 2 anti-intuition points extracted
    14|
    15|### Phase 3: Hook Generation (⛔ BLOCKING)
    16|- [ ] 5 hook variants generated across all 5 dimensions
    17|- [ ] Each hook ≤ 15 Chinese characters (for the critical first 3 seconds)
    18|- [ ] CTR potential estimated for each hook
    19|- [ ] **User has selected a hook before Phase 4 begins**
    20|
    21|### Phase 4: Script Writing
    22|- [ ] Script matches the approved hook exactly (no deviation)
    23|- [ ] Word count within platform limits (see platform-copy.md)
    24|- [ ] CTA included at the end
    25|- [ ] Every claim is traceable to the book
    26|- [ ] Tone matches the book's genre
    27|- [ ] No fabricated quotes or misrepresented concepts
    28|
    29|### Phase 5: Storyboard Generation
    30|- [ ] storyboard.json is valid JSON
    31|- [ ] Every frame has: `visual_description`, `audio_text`, `duration_estimated`, `image_prompt`
    32|- [ ] Total duration ≈ sum of all frame durations
    33|- [ ] Style Lock applied (same seed + character descriptor across all prompts)
    34|- [ ] Platform aspect ratio correct for target platform
    35|
    36|### Phase 7: Asset Prompt Generation
    37|- [ ] image-prompts.json has one entry per frame
    38|- [ ] video-prompts.json has motion descriptors added
    39|- [ ] Cover prompts follow Rule of 3 (≤ 3 visual elements)
    40|- [ ] All prompts pass two-tier quality check (style-engine.md)
    41|
    42|### Phase 8: Asset Generation Coordination
    43|- [ ] Images generated and reviewed
    44|- [ ] TTS audio generated for each frame
    45|- [ ] SRT file generated and timecode-verified
    46|- [ ] BGM selected per genre-mood mapping
    47|
    48|### Phase 9: Assembly
    49|- [ ] Pre-assembly compliance gate passed (all ✅)
    50|- [ ] FFmpeg assembly completed without errors
    51|- [ ] Final video plays back with synced audio/subtitles
    52|- [ ] Video duration matches target
    53|
    54|### Phase 10: SEO & Multi-Platform (optional)
    55|- [ ] SEO metadata generated for requested platforms
    56|- [ ] Platform-specific adaptations applied
    57|- [ ] Chapters/Timestamps accurate (YouTube)
    58|
    59|## Known Pitfalls & Solutions
    60|
    61|### Pitfall 0: Compliance Violation (Limit Traffic/Ban Risk)
**Problem**: Video content triggers platform censorship (shadowban or ban).
**Symptom**: Views stuck at ~200-500, or video set to "Private/Review".
**Fix**: Strictly enforce Phase 5 Compliance Check. Use `compliance-rules.md` for auto-rewriting.
**Detection**: Pre-upload scan using AI agent + `compliance-rules.md` checklist.

### Pitfall 1: Word Count Explosion
    62|**Problem**: AI writes scripts way too long for the target duration.
    63|**Symptom**: 60s video has 600+ characters of script.
    64|**Fix**: Enforce strict limits: 60s ≤ 260 chars, 5min ≤ 1200 chars, 15min ≤ 3500 chars. Calculate at ~4.5 Chinese chars/sec.
    65|**Detection**: `echo "$script" | wc -c`
    66|
    67|### Pitfall 2: Style Drift in Image Generation
    68|**Problem**: Each frame looks like it's from a different movie.
    69|**Fix**: Enforce Style Lock — same seed + character descriptor in every prompt.
    70|**Detection**: `grep -o '\-\-seed [0-9]*' image-prompts.json | sort -u | wc -l` (must be 1)
    71|
    72|### Pitfall 3: Thumbnail CTR Disaster
    73|**Problem**: AI generates busy, cluttered covers that nobody clicks.
    74|**Fix**: Rule of 3 — max 3 elements. One dominant saturated color. Max 5 text characters.
    75|**Detection**: Visual review against thumbnail rules in style-engine.md.
    76|
    77|### Pitfall 4: Audio-Video Desync
    78|**Problem**: Image displays too long/short for the spoken text.
    79|**Fix**: Use timing calculator to dynamically pad/crop image display time.
    80|**Detection**: `python3 scripts/timing_calculator.py verify --storyboard storyboard.json --audio-dir audio/`
    81|
    82|### Pitfall 5: SRT Encoding Issues
    83|**Problem**: Chinese punctuation or emoji breaks SRT rendering.
    84|**Fix**: UTF-8 normalization. Replace full-width punctuation where needed.
    85|**Detection**: Play the video with subtitles enabled on the target platform.
    86|
    87|### Pitfall 6: Safe Zone Violation (9:16)
    88|**Problem**: Text/subjects hidden behind TikTok UI (likes, comments, description).
    89|**Fix**: Bottom 30% = subtitle zone only. Top 20% = TikTok logo zone. Keep critical content in the middle 50%.
    90|**Detection**: Overlay platform safe zone template on storyboard frames.
    91|
    92|### Pitfall 7: BGM Overpowering Voice
    93|**Problem**: Background music drowns out the TTS voice.
    94|**Fix**: BGM at -18dB, TTS at +3dB. Enable ducking (BGM drops when voice is detected).
    95|**Detection**: Listen to final mix. Voice should be clearly audible without adjusting volume.
    96|
    97|### Pitfall 8: Chapter Timestamp Mismatch (YouTube)
    98|**Problem**: Generated chapters don't match actual video content timestamps.
    99|**Fix**: Chapters must be generated AFTER the final video is assembled, based on actual frame durations.
   100|**Detection**: Play video and verify each chapter marker matches content change.
   101|
   102|### Pitfall 9: Overclaiming in Script
   103|**Problem**: Script says "我亲自测试了..." or "我们团队调研发现..." when it's AI-generated.
   104|**Fix**: Use honest framing: "书中提到...", "作者认为...", "根据书中的观点...". Never fabricate personal experience.
   105|
   106|### Pitfall 10: Platform Mismatch
   107|**Problem**: A 16:9 YouTube-style video uploaded to TikTok.
   108|**Fix**: Always generate platform-specific versions. Never upload a horizontal video to a vertical-first platform.
   109|
   110|## File Organization
   111|
   112|```
   113|book-video-studio/YYYY-MM-DD-<book-slug>/<platform>-<duration>/
   114|├── source.md                 # Book metadata, quotes, references
   115|├── viral-analysis.md         # Hook analysis, emotional positioning
   116|├── script.md                 # Approved full script with timing
   117|├── storyboard.json           # Structured storyboard (frame-level)
   118|├── image-prompts.json        # Batch image generation prompts
   119|├── video-prompts.json        # Batch video generation prompts
   120|├── srt-output.srt            # Synchronized subtitles
   121|├── seo-metadata.json         # Platform SEO metadata
   122|├── cover-prompt.md           # Thumbnail generation prompts
   123|├── assembly.sh               # FFmpeg assembly script
   124|├── manifest.json             # Pipeline state & asset registry
   125|├── imgs/                     # Generated images
   126|│   ├── frame-001.png
   127|│   ├── frame-002.png
   128|│   └── cover-v1.png
   129|├── audio/                    # TTS audio segments
   130|│   ├── tts-001.mp3
   131|│   └── bgm-track.mp3
   132|└── video/                    # Final output
   133|    └── final-output.mp4
   134|```
   135|
   136|## Abort Conditions
   137|
   138|The pipeline should STOP (not auto-continue) when:
   139|1. Phase 3 hook not yet approved by user
   140|2. Image generation fails after 3 retries on same frame
   141|3. TTS voice model unavailable and no fallback exists
   142|4. FFmpeg not installed (cannot assemble)
   143|5. User says "停下来" or "暂停"
   144|
   145|When aborting, save all completed artifacts and report exactly which phase failed and why.

**Additional abort condition:**
- Compliance check fails and cannot be auto-rewritten safely (e.g., core topic is banned). STOP and ask user to change topic.
   146|