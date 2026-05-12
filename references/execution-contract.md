# Execution Contract — 执行契约与避坑指南

## Contract Overview

This document defines the rules, constraints, and quality gates that every execution of the Book Video Studio pipeline must follow. It exists to prevent common failure modes in AI video production.

## Phase-by-Phase Gates

### Phase 1-2: Book Deconstruction
- [ ] Source is verified (book title, author, edition)
- [ ] At least 3 key quotes identified with chapter references
- [ ] Emotional positioning determined (搞钱焦虑/认知觉醒/治愈系)
- [ ] At least 2 anti-intuition points extracted

### Phase 3: Hook Generation (⛔ BLOCKING)
- [ ] 5 hook variants generated across all 5 dimensions
- [ ] Each hook ≤ 15 Chinese characters (for the critical first 3 seconds)
- [ ] CTR potential estimated for each hook
- [ ] **User has selected a hook before Phase 4 begins**

### Phase 4: Script Writing
- [ ] Script matches the approved hook exactly (no deviation)
- [ ] Word count within platform limits (see platform-copy.md)
- [ ] CTA included at the end
- [ ] Every claim is traceable to the book
- [ ] Tone matches the book's genre
- [ ] No fabricated quotes or misrepresented concepts

### Phase 5: Storyboard Generation
- [ ] storyboard.json is valid JSON
- [ ] Every frame has: `visual_description`, `audio_text`, `duration_estimated`, `image_prompt`
- [ ] Total duration ≈ sum of all frame durations
- [ ] Style Lock applied (same seed + character descriptor across all prompts)
- [ ] Platform aspect ratio correct for target platform

### Phase 6: Asset Prompt Generation
- [ ] image-prompts.json has one entry per frame
- [ ] video-prompts.json has motion descriptors added
- [ ] Cover prompts follow Rule of 3 (≤ 3 visual elements)
- [ ] All prompts pass two-tier quality check (style-engine.md)

### Phase 7: Asset Generation Coordination
- [ ] Images generated and reviewed
- [ ] TTS audio generated for each frame
- [ ] SRT file generated and timecode-verified
- [ ] BGM selected per genre-mood mapping

### Phase 8: Assembly
- [ ] Pre-assembly compliance gate passed (all ✅)
- [ ] FFmpeg assembly completed without errors
- [ ] Final video plays back with synced audio/subtitles
- [ ] Video duration matches target

### Phase 9: SEO & Multi-Platform (optional)
- [ ] SEO metadata generated for requested platforms
- [ ] Platform-specific adaptations applied
- [ ] Chapters/Timestamps accurate (YouTube)

## Known Pitfalls & Solutions

### Pitfall 1: Word Count Explosion
**Problem**: AI writes scripts way too long for the target duration.
**Symptom**: 60s video has 600+ characters of script.
**Fix**: Enforce strict limits: 60s ≤ 260 chars, 5min ≤ 1200 chars, 15min ≤ 3500 chars. Calculate at ~4.5 Chinese chars/sec.
**Detection**: `echo "$script" | wc -c`

### Pitfall 2: Style Drift in Image Generation
**Problem**: Each frame looks like it's from a different movie.
**Fix**: Enforce Style Lock — same seed + character descriptor in every prompt.
**Detection**: `grep -o '\-\-seed [0-9]*' image-prompts.json | sort -u | wc -l` (must be 1)

### Pitfall 3: Thumbnail CTR Disaster
**Problem**: AI generates busy, cluttered covers that nobody clicks.
**Fix**: Rule of 3 — max 3 elements. One dominant saturated color. Max 5 text characters.
**Detection**: Visual review against thumbnail rules in style-engine.md.

### Pitfall 4: Audio-Video Desync
**Problem**: Image displays too long/short for the spoken text.
**Fix**: Use timing calculator to dynamically pad/crop image display time.
**Detection**: `python3 scripts/timing_calculator.py verify --storyboard storyboard.json --audio-dir audio/`

### Pitfall 5: SRT Encoding Issues
**Problem**: Chinese punctuation or emoji breaks SRT rendering.
**Fix**: UTF-8 normalization. Replace full-width punctuation where needed.
**Detection**: Play the video with subtitles enabled on the target platform.

### Pitfall 6: Safe Zone Violation (9:16)
**Problem**: Text/subjects hidden behind TikTok UI (likes, comments, description).
**Fix**: Bottom 30% = subtitle zone only. Top 20% = TikTok logo zone. Keep critical content in the middle 50%.
**Detection**: Overlay platform safe zone template on storyboard frames.

### Pitfall 7: BGM Overpowering Voice
**Problem**: Background music drowns out the TTS voice.
**Fix**: BGM at -18dB, TTS at +3dB. Enable ducking (BGM drops when voice is detected).
**Detection**: Listen to final mix. Voice should be clearly audible without adjusting volume.

### Pitfall 8: Chapter Timestamp Mismatch (YouTube)
**Problem**: Generated chapters don't match actual video content timestamps.
**Fix**: Chapters must be generated AFTER the final video is assembled, based on actual frame durations.
**Detection**: Play video and verify each chapter marker matches content change.

### Pitfall 9: Overclaiming in Script
**Problem**: Script says "我亲自测试了..." or "我们团队调研发现..." when it's AI-generated.
**Fix**: Use honest framing: "书中提到...", "作者认为...", "根据书中的观点...". Never fabricate personal experience.

### Pitfall 10: Platform Mismatch
**Problem**: A 16:9 YouTube-style video uploaded to TikTok.
**Fix**: Always generate platform-specific versions. Never upload a horizontal video to a vertical-first platform.

## File Organization

```
book-video-studio/YYYY-MM-DD-<book-slug>/<platform>-<duration>/
├── source.md                 # Book metadata, quotes, references
├── viral-analysis.md         # Hook analysis, emotional positioning
├── script.md                 # Approved full script with timing
├── storyboard.json           # Structured storyboard (frame-level)
├── image-prompts.json        # Batch image generation prompts
├── video-prompts.json        # Batch video generation prompts
├── srt-output.srt            # Synchronized subtitles
├── seo-metadata.json         # Platform SEO metadata
├── cover-prompt.md           # Thumbnail generation prompts
├── assembly.sh               # FFmpeg assembly script
├── manifest.json             # Pipeline state & asset registry
├── imgs/                     # Generated images
│   ├── frame-001.png
│   ├── frame-002.png
│   └── cover-v1.png
├── audio/                    # TTS audio segments
│   ├── tts-001.mp3
│   └── bgm-track.mp3
└── video/                    # Final output
    └── final-output.mp4
```

## Abort Conditions

The pipeline should STOP (not auto-continue) when:
1. Phase 3 hook not yet approved by user
2. Image generation fails after 3 retries on same frame
3. TTS voice model unavailable and no fallback exists
4. FFmpeg not installed (cannot assemble)
5. User says "停下来" or "暂停"

When aborting, save all completed artifacts and report exactly which phase failed and why.
