#!/usr/bin/env python3
"""
Book Video Studio - Auto Compose Helper
根据 storyboard.json 生成 FFmpeg 合成命令脚本
"""

import json
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_compose.py <storyboard.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        storyboard = json.load(f)

    output_dir = os.path.dirname(sys.argv[1]) or '.'
    concat_file = os.path.join(output_dir, 'file_list.txt')
    
    print("# 🎬 FFmpeg 合成脚本生成完毕")
    print("# 请确保 images 和 audio 已就绪")
    print(f"cd {output_dir}")
    
    # 1. 生成 concat list for images
    print("\n# 1. 生成图片拼接列表")
    with open(concat_file, 'w') as out:
        for i, scene in enumerate(storyboard):
            img_name = f"scene_{i:03d}.png"
            print(f"file '{img_name}'")
            print(f"duration {calculate_duration(scene.get('time', '0:00'))}")
            out.write(f"file '{img_name}'\n")
            out.write(f"duration {calculate_duration(scene.get('time', '0:00'))}\n")
        out.write(f"file '{os.path.basename(storyboard[-1].get('image_prompt', '').split(' --')[0]) or 'scene_last.png'}'\n")

    # 2. 合成图片为视频 (带 Ken Burns 效果模拟)
    print("\n# 2. 合成图片为视频流")
    print("ffmpeg -f concat -safe 0 -i file_list.txt -vf 'scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2' -c:v libx264 -pix_fmt yuv4j2p -r 30 video_only.mp4")

    # 3. 拼接音频
    print("\n# 3. 拼接 TTS 音频")
    audio_concat = os.path.join(output_dir, 'audio_list.txt')
    with open(audio_concat, 'w') as out:
        for i in range(len(storyboard)):
            out.write(f"file 'tts_{i:03d}.mp3'\n")
    print(f"ffmpeg -f concat -safe 0 -i audio_list.txt -c copy audio_track.mp3")

    # 4. 最终合成 (视频 + 音频 + BGM + 字幕)
    print("\n# 4. 最终合成")
    print("ffmpeg -i video_only.mp4 -i audio_track.mp4 -i bgm.mp3 -filter_complex '[1:a]volume=1.0[a1];[2:a]volume=0.3[a2];[a1][a2]amix=inputs=2:duration=first[outa]' -map 0:v -map '[outa]' -c:v copy -shortest final_output.mp4")

def calculate_duration(time_str):
    # 简化版：解析 "00:00-00:03" -> 3
    try:
        parts = time_str.split('-')
        if len(parts) == 2:
            s = parts[1].split(':')
            return int(s[0])*60 + int(s[1])
        return 3
    except:
        return 3

if __name__ == '__main__':
    main()
