# Style Engine — 风格解析与 Prompt 锁定规则

## Style Resolution Order

1. **Explicit user instruction** — user says "用电影风格" → use `cinematic` preset
2. **design.pen preset** — user references a preset name
3. **Genre-based default** — inferred from book genre
4. **Custom brief** — user describes a unique visual direction

## Genre → Style Mapping

| Book Genre | Default Style | Rationale |
|------------|--------------|-----------|
| 商业管理/搞钱 | `cinematic` | 权威感、专业感、深色沉稳 |
| 心理学/情感治愈 | `watercolor` | 温暖、柔和、治愈感 |
| 工具书/方法论 | `minimalist` | 清晰、高效、无干扰 |
| 科技/AI/未来 | `3d_render` | 科技感、现代感、高级感 |
| 爆款话题/争议 | `editorial` | 冲击力强、吸引眼球 |
| 轻小说/年轻化 | `anime` | 年轻受众、情感共鸣 |

## Style Lock — 视觉一致性强制规则

### What is Style Lock?
AI 生图/生视频的最大问题是**风格漂移**（Style Drift）——同一本书的不同帧，画面风格完全不同，像拼凑的。Style Lock 解决这个问题。

### Style Lock = 2 Components

**1. Seed Consistency**
```
生成一个随机 seed，全片通用。
例：--seed 4827193
```

**2. Character Descriptor**
```
定义一个通用主角描述，强制附加到每一帧的 Prompt 后面。
例：[CHAR] a 35-year-old Asian man in a navy blazer, short hair, thoughtful expression, standing in a modern office [END]
```

### Every Prompt Format
```
[Scene description] + [CHAR descriptor] + [Style suffix from design.pen] + --seed [fixed]
```

### Example (Cinematic Preset)
```
Prompt 1: A man looking at a city skyline from a high-rise window at dusk + [CHAR] + cinematic lighting, shallow depth of field, 35mm lens, color graded, film grain, anamorphic bokeh --ar 16:9 --v 6.1 --style raw --seed 4827193

Prompt 2: The same man sitting at a desk with scattered papers and a glowing laptop + [CHAR] + cinematic lighting, shallow depth of field, 35mm lens, color graded, film grain, anamorphic bokeh --ar 16:9 --v 6.1 --style raw --seed 4827193
```

### Verification
Before proceeding to asset generation, verify Style Lock with:
```bash
# Check all prompts share the same seed
grep -o '\-\-seed [0-9]*' image-prompts.json | sort -u | wc -l
# Must return 1

# Check all prompts contain the character descriptor
grep -c '[CHAR]' image-prompts.json
# Must match total number of frames
```

## Thumbnail Style Rules

Thumbnails follow different rules from video frames:

### The Rule of 3
- **Background**: 1 dominant color or gradient (neutral)
- **Subject**: 1 focal point (face, object, concept)
- **Text overlay**: max 5 characters, extra-bold

### CTR Optimization
- **Emotion**: Extreme emotion increases CTR by ~30%
- **Eye contact**: Subject looking at camera increases CTR by ~20%
- **Color pop**: One saturated accent color (#FF3366, #FFD700, #00FF88) against neutral background
- **Negative space**: 40% of frame left free for text

### What NOT to do
- ❌ Don't use video frames as thumbnails (too busy)
- ❌ Don't put more than 3 visual elements
- ❌ Don't use thin fonts (invisible at small sizes)
- ❌ Don't use complex backgrounds (distracts from subject)

## Two-Tier Image Quality Check

Before any image is approved for the storyboard:

### Tier 1: Eliminate Defects
- [ ] No extra fingers/limbs (AI hands problem)
- [ ] No garbled text/characters in the image
- [ ] No distorted faces
- [ ] No impossible geometry
- [ ] No unintended double images

### Tier 2: Verify Content Match
- [ ] Image matches the scene description (subject, setting, mood)
- [ ] Composition follows the platform's safe zone rules
- [ ] Color palette matches the style preset
- [ ] Image supports the script's narrative at this point
- [ ] Image is not repetitive with adjacent frames

## Video Prompt Enhancement

When upgrading from image to video prompts:

### Motion Descriptors
Add one camera movement from `design.pen`'s `camera_movements`:
- `ken_burns`: slow zoom in, cinematic pan right
- `orbit`: slow 360 orbit around subject
- `dolly`: dolly in slowly, reveal scene
- `static`: locked-off tripod shot, subtle atmospheric movement
- `push_in`: gradual push in to subject's face

### Example
```
Image Prompt: A man looking at a city skyline from a high-rise window at dusk + [CHAR] + cinematic lighting...

Video Prompt: A man looking at a city skyline from a high-rise window at dusk + [CHAR] + cinematic lighting... CAMERA: slow ken burns zoom in, subtle atmospheric dust particles in the air, 5s duration
```

### Video Model Tips
| Model | Best For | Tip |
|-------|----------|-----|
| Kling AI | 人物动作、自然场景 | Use `--motion-scale 5` for balanced movement |
| Runway Gen-3 | 电影感、运镜控制 | Specify camera movement explicitly in prompt |
| Luma Dream Machine | 高质量短片段 | Keep prompts concise, under 100 tokens |
| Pika 1.0 | 动漫风格、创意运动 | Add `-motion 2` for subtle movement |
| SVD | 快速测试/低成本 | Use as fallback, expect lower quality |
