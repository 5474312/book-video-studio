#!/usr/bin/env python3
"""
tts_long_text.py — 长文案一次性转语音工具
- 自动按段落/标点切分，无需手动分段
- 支持 edge-tts 8 种中文音色
- ffmpeg 自动拼接成完整 MP3
- 适合视频文案、口播稿等长文本（无长度限制）

Usage:
    python3 tts_long_text.py --input script.txt --output output.mp3 --voice xiaoxiao
    python3 tts_long_text.py --input script.txt --output output.mp3 --voice yunxi --rate "+10%"
    python3 tts_long_text.py --list-voices
"""

import asyncio
import edge_tts
import os
import re
import sys
import subprocess
import tempfile
import argparse
from pathlib import Path


def split_text(text: str, max_chunk_chars: int = 500) -> list:
    """智能切分长文本：优先按段落，段落太长则按句子切"""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    for para in paragraphs:
        if len(para) <= max_chunk_chars:
            chunks.append(para)
        else:
            sentences = re.split(r'([。！？；\n])', para)
            current = ''
            for i in range(0, len(sentences), 2):
                sentence = sentences[i]
                punct = sentences[i + 1] if i + 1 < len(sentences) else ''
                segment = sentence + punct
                if len(current + segment) <= max_chunk_chars:
                    current += segment
                else:
                    if current:
                        chunks.append(current.strip())
                    current = segment
            if current:
                chunks.append(current.strip())
    # 合并过短的相邻 chunk
    merged = []
    for chunk in chunks:
        if merged and len(merged[-1] + chunk) <= max_chunk_chars:
            merged[-1] += '\n' + chunk
        else:
            merged.append(chunk)
    return merged


async def generate_segment(text: str, voice: str, output_path: str) -> bool:
    """生成单个片段的语音"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False


async def process_text(text: str, voice: str, output_path: str, rate: str = "+0%"):
    """处理完整文本，分段生成并拼接"""
    chunks = split_text(text)
    print(f"📝 文案总字数: {len(text)}")
    print(f"🔪 自动切分为 {len(chunks)} 段")
    print(f"🎤 音色: {voice}")
    print()
    
    tmpdir = tempfile.mkdtemp()
    audio_files = []
    
    for i, chunk in enumerate(chunks):
        seg_file = os.path.join(tmpdir, f"seg_{i:03d}.mp3")
        preview = chunk[:30].replace('\n', ' ')
        print(f"  [{i+1}/{len(chunks)}] 生成: {preview}...")
        
        success = await generate_segment(chunk, voice, seg_file)
        if success:
            audio_files.append(seg_file)
        else:
            print(f"  ⚠️  插入静音替代")
            silence_file = os.path.join(tmpdir, f"silence_{i:03d}.mp3")
            subprocess.run([
                'ffmpeg', '-y', '-f', 'lavfi',
                '-i', f'anullsrc=duration=1:sample_rate=44100',
                '-codec:a', 'libmp3lame', silence_file
            ], capture_output=True)
            audio_files.append(silence_file)
    
    if not audio_files:
        print("❌ 没有生成任何音频片段")
        return False
    
    # ffmpeg concat demuxer 拼接
    concat_file = os.path.join(tmpdir, "concat.txt")
    with open(concat_file, 'w') as f:
        for audio_file in audio_files:
            f.write(f"file '{os.path.abspath(audio_file)}'\n")
    
    print(f"\n🔗 正在拼接 {len(audio_files)} 个片段...")
    result = subprocess.run([
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', concat_file,
        '-codec:a', 'libmp3lame', '-q:a', '2',
        '-ar', '44100',
        output_path
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        file_size = os.path.getsize(output_path) / (1024 * 1024)
        duration_result = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', output_path
        ], capture_output=True, text=True)
        duration = float(duration_result.stdout.strip()) if duration_result.stdout else 0
        
        print(f"✅ 完成!")
        print(f"   📁 输出: {output_path}")
        print(f"   📏 大小: {file_size:.1f} MB")
        print(f"   ⏱️  时长: {duration:.0f} 秒 ({duration/60:.1f} 分钟)")
        return True
    else:
        print(f"❌ 拼接失败: {result.stderr}")
        return False


VOICE_PRESETS = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "yunxi": "zh-CN-YunxiNeural",
    "yunyang": "zh-CN-YunyangNeural",
    "xiaoyi": "zh-CN-XiaoyiNeural",
    "yunjian": "zh-CN-YunjianNeural",
    "xiaobei": "zh-CN-liaoning-XiaobeiNeural",
    "xiaoni": "zh-CN-shaanxi-XiaoniNeural",
    "yunxia": "zh-CN-YunxiaNeural",
}


def main():
    parser = argparse.ArgumentParser(description="长文案一次性转语音")
    parser.add_argument("--input", "-i", required=True, help="输入文案文件 (.txt/.md)")
    parser.add_argument("--output", "-o", default="output.mp3", help="输出 MP3 文件路径")
    parser.add_argument("--voice", "-v", default="xiaoxiao", help="音色 (预设名或完整音色名)")
    parser.add_argument("--rate", "-r", default="+0%", help="语速 (如 +10%, -5%)")
    parser.add_argument("--list-voices", action="store_true", help="列出可用音色")
    args = parser.parse_args()
    
    if args.list_voices:
        print("🎤 可用音色:")
        for name, voice_id in VOICE_PRESETS.items():
            desc = {
                "xiaoxiao": "女声 - 通用/口播/推荐",
                "yunxi": "男声 - 年轻/活力",
                "yunyang": "男声 - 沉稳/旁白",
                "xiaoyi": "女声 - 可爱/少女",
                "yunjian": "男声 - 成熟/反派",
                "xiaobei": "东北女声",
                "xiaoni": "陕西女声",
                "yunxia": "童声",
            }.get(name, "")
            print(f"   {name}: {desc}")
        return
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ 文件不存在: {args.input}")
        sys.exit(1)
    
    text = input_path.read_text(encoding='utf-8')
    text = re.sub(r'#{1,6}\s', '', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    voice = args.voice
    if voice in VOICE_PRESETS:
        voice = VOICE_PRESETS[voice]
    
    asyncio.run(process_text(text, voice, args.output, args.rate))


if __name__ == "__main__":
    main()
