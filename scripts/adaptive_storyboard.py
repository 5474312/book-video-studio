#!/usr/bin/env python3
"""
adaptive_storyboard.py — 基于音频时长的自适应分镜生成器
- 读取音频精确时长（ffprobe）
- 按目标节奏（默认 18 秒/段）自动拆分成画面段数
- 优先在句号、感叹号、问号、分段处断句，保证语义完整
- 自动从文案提取关键词匹配画面 Prompt
- 输出 storyboard.json + image_prompts.json 供批量生图和 FFmpeg 合成

Usage:
    python3 adaptive_storyboard.py --input script.txt --audio audio.mp3 --output-dir ./output
    python3 adaptive_storyboard.py --input script.txt --audio audio.mp3 --segment-duration 15 --output-dir ./output
"""

import re
import json
import os
import subprocess
import argparse
from pathlib import Path


def get_audio_duration(audio_path: str) -> float:
    """获取音频精确时长（秒）"""
    result = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', audio_path
    ], capture_output=True, text=True)
    return float(result.stdout.strip())


def split_sentences(text: str) -> list:
    """将文本拆分成句子列表，保留标点"""
    sentences = re.split(r'([。！？；\n]+)', text)
    result = []
    for i in range(0, len(sentences), 2):
        sentence = sentences[i].strip()
        punct = sentences[i + 1] if i + 1 < len(sentences) else ''
        if sentence:
            result.append(sentence + punct.replace('\n', ' '))
    return result


def split_text_adaptive(text: str, target_segments: int) -> list:
    """自适应拆分文本，确保每段语义完整"""
    sentences = split_sentences(text)
    chars_per_segment = sum(len(s) for s in sentences) / target_segments
    
    segments = []
    current = ''
    for s in sentences:
        if len(current) + len(s) > chars_per_segment and len(current) > 40:
            segments.append(current.strip())
            current = s
        else:
            current += s
    
    if current.strip():
        # 如果最后一段太短，合并到上一段
        if segments and len(current) < 50:
            segments[-1] += current
        else:
            segments.append(current.strip())
    
    return segments


# 关键词 → 画面 Prompt 映射
KEYWORD_MAP = {
    '丁元英': 'lone mastermind sitting alone in ancient room',
    '刘冰': 'lost man wandering in dark alley',
    '肖亚文': 'confident young woman walking through modern office',
    '叶晓明': 'hesitating businessman at crossroads',
    '冯世杰': 'cautious craftsman working at desk',
    '芮小丹': 'elegant woman in uniform looking into distance',
    '韩楚风': 'respected elder at tea table',
    '格律诗': 'vintage camera lens on wooden table',
    '乐圣': 'corporate glass tower at dusk',
    '内卷': 'crowd of people running endlessly in hamster wheel',
    '阶层': 'stone staircase ascending into fog',
    '认知': 'glowing lightbulb illuminating dark room',
    '规则': 'ancient chess board with scattered pieces',
    '博弈': 'go stones balancing on scale',
    '人性': 'mask reflecting two faces',
    '利益': 'golden scales tipping',
    '破局': 'hand breaking through cracked glass',
    '救赎': 'hand reaching down from light',
    '救世主': 'silhouette standing on mountain peak',
    '底层': 'shadowy figure hunched under bridge',
    '中层': 'office worker trapped in glass box',
    '高层': 'person overlooking city from penthouse',
    '寄生': 'ivy vine wrapping around dead tree',
    '自救': 'person climbing rope out of dark pit',
    '强势': 'eagle soaring above storm clouds',
    '弱势': 'small bird sheltering under leaf in rain',
    '情绪': 'storm clouds gathering over calm lake',
    '清醒': 'clear mirror reflecting sunrise',
    '格局': 'wide landscape viewed from mountain top',
    '命运': 'clock hands casting long shadow',
    '商业': 'stock market ticker board at night',
    '职场': 'empty conference room with one spotlight',
    '丛林': 'dense forest with single path',
    '洗牌': 'playing cards falling in slow motion',
    '降维': '3D cube flattening to 2D plane',
    '价值交换': 'two hands exchanging glowing orbs',
    '边界感': 'invisible barrier between two people',
    '长期思维': 'hourglass with sand flowing upward',
    '短期红利': 'hand grabbing falling coins',
    '实力': 'tree with deep roots in storm',
    '天赋': 'spark igniting in darkness',
    '努力': 'sweat drops falling on concrete',
    '运气': 'dice rolling on green felt',
    '公平': 'blindfolded statue of justice',
    '温柔': 'soft morning light through window',
    '恶人': 'shadow stretching long at sunset',
    '强大': 'mountain standing firm against wind',
}

DEFAULT_PROMPTS = [
    'cinematic wide landscape with dramatic lighting',
    'close up of thoughtful expression in dim light',
    'abstract geometric shapes floating in dark space',
    'vintage desk with scattered papers and coffee',
    'city skyline at twilight with warm amber glow',
    'empty road stretching into misty horizon',
    'open book with pages turning in breeze',
    'lone figure walking on beach at sunset',
    'close up of hands holding compass',
    'staircase spiraling upward into light',
]


def generate_storyboard(text: str, audio_duration: float, segment_duration: float = 18.0) -> list:
    """生成分镜列表"""
    target_segments = max(10, int(audio_duration / segment_duration))
    segments_text = split_text_adaptive(text, target_segments)
    
    num_segments = len(segments_text)
    actual_segment_duration = audio_duration / num_segments
    
    storyboard = []
    prompts_list = []
    
    for i, seg_text in enumerate(segments_text):
        start_time = i * actual_segment_duration
        end_time = (i + 1) * actual_segment_duration
        
        # 匹配关键词
        matched_keywords = []
        for kw, visual in KEYWORD_MAP.items():
            if kw in seg_text:
                matched_keywords.append(visual)
        
        # 去重并限制关键词数量
        matched_keywords = list(dict.fromkeys(matched_keywords))[:2]
        
        if matched_keywords:
            subject = ', '.join(matched_keywords)
        else:
            subject = DEFAULT_PROMPTS[i % len(DEFAULT_PROMPTS)]
        
        # 统一风格锁定
        style = (
            "cinematic shot, dark moody atmosphere, "
            "warm amber and cool blue lighting contrast, "
            "film grain, shallow depth of field, "
            "dramatic shadows, photorealistic, "
            "16:9 aspect ratio, --v 6.0 --ar 16:9"
        )
        
        prompt = f"{subject}, {style}"
        
        seg = {
            "index": i + 1,
            "text": seg_text,
            "start_time": round(start_time, 2),
            "end_time": round(end_time, 2),
            "duration": round(actual_segment_duration, 2),
            "image_prompt": prompt,
            "image_file": f"img_{i+1:03d}.png",
            "srt_index": i + 1
        }
        storyboard.append(seg)
        
        prompts_list.append({
            "index": i + 1,
            "filename": seg["image_file"],
            "prompt": prompt,
            "text_preview": seg_text[:40] + "..."
        })
    
    return storyboard, prompts_list


def main():
    parser = argparse.ArgumentParser(description="基于音频时长的自适应分镜生成器")
    parser.add_argument("--input", "-i", required=True, help="输入文案文件 (.txt/.md)")
    parser.add_argument("--audio", "-a", required=True, help="音频文件 (.mp3/.wav)")
    parser.add_argument("--output-dir", "-o", required=True, help="输出目录")
    parser.add_argument("--segment-duration", "-d", type=float, default=18.0, help="每段目标时长 (秒)")
    args = parser.parse_args()
    
    # 读取音频时长
    print("🎵 读取音频时长...")
    duration = get_audio_duration(args.audio)
    print(f"   时长: {duration:.1f} 秒 ({duration/60:.1f} 分钟)")
    
    # 读取文案
    text = Path(args.input).read_text(encoding='utf-8')
    text = re.sub(r'#{1,6}\s', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # 生成分镜
    storyboard, prompts = generate_storyboard(text, duration, args.segment_duration)
    
    # 保存
    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, "storyboard.json"), 'w', encoding='utf-8') as f:
        json.dump(storyboard, f, ensure_ascii=False, indent=2)
    with open(os.path.join(args.output_dir, "image_prompts.json"), 'w', encoding='utf-8') as f:
        json.dump(prompts, f, ensure_ascii=False, indent=2)
    
    # 打印摘要
    lens = [len(s['text']) for s in storyboard]
    print(f"📋 分镜生成完成!")
    print(f"   总段数: {len(storyboard)}")
    print(f"   每段时长: {storyboard[0]['duration']:.1f} 秒")
    print(f"   最短段: {min(lens)} 字, 最长段: {max(lens)} 字, 平均: {sum(lens)/len(lens):.0f} 字")
    print(f"\n📁 文件已保存:")
    print(f"   {args.output_dir}/storyboard.json")
    print(f"   {args.output_dir}/image_prompts.json")


if __name__ == "__main__":
    main()
