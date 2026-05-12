#!/usr/bin/env python3
"""
Book Video Studio - Auto Compose Helper v2
根据 storyboard.json 生成 FFmpeg 合成命令、SRT 字幕和时长估算修正。
"""

import json
import sys
import os
import re

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_compose.py <storyboard.json> [--platform youtube/tiktok]")
        sys.exit(1)

    sb_path = sys.argv[1]
    with open(sb_path, 'r', encoding='utf-8') as f:
        storyboard = json.load(f)

    output_dir = os.path.dirname(sb_path) or '.'
    platform = 'youtube'
    if '--platform' in sys.argv:
        idx = sys.argv.index('--platform')
        if idx + 1 < len(sys.argv):
            platform = sys.argv[idx+1]

    print("# 🎬 Book Video Studio Compose Helper v2")
    print(f"# Platform: {platform.upper()}")
    print(f"cd {output_dir}")
    
    # 1. Generate SRT
    srt_path = os.path.join(output_dir, 'subtitle.srt')
    generate_srt(storyboard, srt_path)
    print(f"\n# ✅ SRT Subtitle generated: subtitle.srt")

    # 2. FFmpeg Concat List for Images (with duration correction)
    concat_file = os.path.join(output_dir, 'file_list.txt')
    current_time = 0.0
    
    print("\n# 🎞️ Generating Image Concat List")
    with open(concat_file, 'w') as out:
        for i, scene in enumerate(storyboard):
            img_name = f"scene_{i:03d}.png"
            # Estimate duration from audio_text if not provided (Chinese ~4.5 chars/sec)
            audio_len = len(scene.get('audio_text', '').replace(' ', ''))
            est_duration = audio_len / 4.5
            final_duration = max(est_duration, 3.0) # Minimum 3s per shot
            
            # Check for pause
            pause = scene.get('pause', 0)
            final_duration += pause
            
            print(f"  Scene {i}: {final_duration:.2f}s ({audio_len} chars)")
            
            out.write(f"file '{img_name}'\n")
            out.write(f"duration {final_duration:.2f}\n")
    
    # 3. FFmpeg Command to Create Video with Zoom Effect
    # This is a complex command. We generate a bash script for better readability.
    compose_script = os.path.join(output_dir, 'compose.sh')
    generate_compose_script(platform, compose_script, concat_file, srt_path, storyboard)
    print(f"\n# 🚀 Composition script generated: compose.sh")
    print(f"bash compose.sh")

def generate_srt(storyboard, path):
    """Generate SRT content from storyboard"""
    with open(path, 'w', encoding='utf-8') as f:
        current_time = 0.0
        for i, scene in enumerate(storyboard):
            audio_text = scene.get('audio_text', '')
            if not audio_text.strip():
                continue
                
            audio_len = len(audio_text.replace(' ', ''))
            duration = audio_len / 4.5
            
            start_str = format_time(current_time)
            end_str = format_time(current_time + duration)
            
            f.write(f"{i+1}\n")
            f.write(f"{start_str} --> {end_str}\n")
            f.write(f"{audio_text}\n\n")
            
            current_time += duration

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def generate_compose_script(platform, script_path, concat_file, srt_path, storyboard):
    """Generate a bash script for FFmpeg"""
    # Determine resolution based on platform
    if platform in ['tiktok', 'shorts']:
        res = "1080x1920"
        vf_extra = ",scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2"
    else:
        res = "1920x1080"
        vf_extra = ",scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2"

    with open(script_path, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("echo '🎬 Starting FFmpeg Composition...'\n")
        
        # 1. Images to Video
        f.write(f"ffmpeg -y -f concat -safe 0 -i file_list.txt \\\n")
        f.write(f"  -vf 'fps=30{vf_extra},zoompan=z='min(zoom+0.0015,1.5)':x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):d={len(storyboard)*90}:s={res}:fps=30' \\\n")
        f.write(f"  -c:v libx264 -pix_fmt yuvj420p -r 30 video_base.mp4\n")
        
        # 2. Burn Subtitles (Requires libass)
        # Escape the path for ffmpeg filter
        srt_escaped = srt_path.replace(':', '\\:').replace('\'', '')
        f.write(f"\necho '📝 Burning Subtitles...'\n")
        f.write(f"ffmpeg -y -i video_base.mp4 \\\n")
        f.write(f"  -vf \"subtitles='{srt_escaped}':force_style='FontSize=24,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=2,Shadow=1'\" \\\n")
        f.write(f"  -c:v libx264 -preset fast final_video.mp4\n")
        
        f.write("\necho '✅ Done! Check final_video.mp4'\n")

if __name__ == '__main__':
    main()
