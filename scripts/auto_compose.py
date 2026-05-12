#!/usr/bin/env python3
"""
auto_compose.py — FFmpeg 视频自动化合成脚本 (多功能入口)

Commands:
  render     - 渲染分镜为 FFmpeg 命令列表
  compose    - 执行 FFmpeg 合成（图片+音频+BGM+字幕）
  info       - 查看 storyboard 信息（帧数、总时长、字数统计）
  srt        - 从 storyboard 生成 SRT 字幕文件
  verify     - 验证 storyboard 合规性（Style Lock、字数限制、时长匹配）

Usage:
  python3 auto_compose.py compose --storyboard storyboard.json --output final.mp4
  python3 auto_compose.py info --storyboard storyboard.json
  python3 auto_compose.py verify --storyboard storyboard.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent

SPEECH_RATE = 4.5  # Chinese chars per second


def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def dump_json(data: dict, path: Optional[str] = None) -> None:
    out_path = path or "output.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Output saved to {out_path}")


def estimate_duration(text: str) -> float:
    """Estimate speech duration from Chinese text."""
    char_count = len(re.sub(r'\s+', '', text))
    return max(char_count / SPEECH_RATE, 1.0)


def generate_srt(storyboard: dict, output_path: str) -> None:
    """Generate SRT subtitle file from storyboard."""
    frames = storyboard.get("frames", [])
    if not frames:
        print("❌ No frames in storyboard")
        return

    current_time = 0.0
    srt_lines = []

    for i, frame in enumerate(frames, 1):
        audio_text = frame.get("audio_text", "").strip()
        if not audio_text:
            continue

        duration = frame.get("duration_estimated", estimate_duration(audio_text))
        start = current_time
        end = current_time + duration

        start_str = format_srt_time(start)
        end_str = format_srt_time(end)

        srt_lines.append(f"{i}")
        srt_lines.append(f"{start_str} --> {end_str}")
        srt_lines.append(audio_text)
        srt_lines.append("")

        current_time = end

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt_lines))

    print(f"✅ SRT generated: {output_path} ({len(frames)} entries, {format_srt_time(current_time)} total)")


def format_srt_time(seconds: float) -> str:
    """Format seconds to SRT timecode (00:00:00,000)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def cmd_info(args: argparse.Namespace) -> None:
    """Display storyboard information."""
    storyboard = load_json(args.storyboard)
    frames = storyboard.get("frames", [])

    if not frames:
        print("❌ No frames found in storyboard")
        return

    total_duration = sum(f.get("duration_estimated", 0) for f in frames)
    total_chars = sum(len(re.sub(r'\s+', '', f.get("audio_text", ""))) for f in frames)
    avg_duration = total_duration / len(frames) if frames else 0

    print(f"📊 Storyboard Info")
    print(f"  Frames:        {len(frames)}")
    print(f"  Total duration: {format_srt_time(total_duration)}")
    print(f"  Total chars:    {total_chars}")
    print(f"  Avg per frame:  {avg_duration:.1f}s")
    print(f"  Speech rate:    {total_chars / total_duration:.1f} chars/sec" if total_duration > 0 else "")
    print()

    # Per-frame breakdown
    print("  Frame | Duration | Chars | Audio Preview")
    print("  " + "-" * 70)
    for i, frame in enumerate(frames, 1):
        audio = frame.get("audio_text", "")[:40]
        dur = frame.get("duration_estimated", 0)
        chars = len(re.sub(r'\s+', '', frame.get("audio_text", "")))
        print(f"  {i:5d} | {dur:8.1f}s | {chars:5d} | {audio}")


def cmd_srt(args: argparse.Namespace) -> None:
    """Generate SRT from storyboard."""
    storyboard = load_json(args.storyboard)
    output = args.output or "srt-output.srt"
    generate_srt(storyboard, output)


def cmd_verify(args: argparse.Namespace) -> None:
    """Verify storyboard compliance."""
    storyboard = load_json(args.storyboard)
    frames = storyboard.get("frames", [])
    issues = []

    # 1. Style Lock check: all prompts share same seed
    seeds = set()
    char_desc = None
    for frame in frames:
        prompt = frame.get("image_prompt", "")
        seed_match = re.search(r'--seed\s+(\d+)', prompt)
        if seed_match:
            seeds.add(seed_match.group(1))
        if "[CHAR]" in prompt:
            if char_desc is None:
                char_desc = re.search(r'\[CHAR\](.*?)\[END\]', prompt, re.DOTALL)
                if char_desc:
                    char_desc = char_desc.group(1).strip()

    if len(seeds) > 1:
        issues.append(f"❌ Style Lock: {len(seeds)} different seeds found ({', '.join(seeds)}). Must be 1.")
    elif seeds:
        print(f"✅ Style Lock: seed={seeds.pop()}")
    else:
        issues.append("⚠️ Style Lock: No --seed found in prompts")

    if char_desc:
        print(f"✅ Character Lock: descriptor found ({len(char_desc)} chars)")
    elif frames and any("[CHAR]" in f.get("image_prompt", "") for f in frames):
        issues.append("⚠️ Character Lock: [CHAR] marker found but no descriptor extracted")

    # 2. Word count vs duration check
    speech_rate = SPEECH_RATE
    for i, frame in enumerate(frames, 1):
        audio = frame.get("audio_text", "")
        char_count = len(re.sub(r'\s+', '', audio))
        duration = frame.get("duration_estimated", 0)
        max_chars = duration * speech_rate
        if char_count > max_chars * 1.2:  # 20% tolerance
            issues.append(f"❌ Frame {i}: {char_count} chars exceed max {max_chars:.0f} for {duration:.1f}s duration")

    if not any("Frame" in i for i in issues):
        print("✅ Word count: all frames within duration limits")

    # 3. SRT timecode check
    total_duration = sum(f.get("duration_estimated", 0) for f in frames)
    total_chars = sum(len(re.sub(r'\s+', '', f.get("audio_text", ""))) for f in frames)
    expected_duration = total_chars / speech_rate
    if abs(total_duration - expected_duration) > 5:  # 5s tolerance
        issues.append(f"⚠️ Duration mismatch: storyboard={total_duration:.1f}s, expected={expected_duration:.1f}s")
    else:
        print(f"✅ Duration: {total_duration:.1f}s matches speech rate ({expected_duration:.1f}s)")

    # 4. Total duration check
    print(f"\n📊 Summary: {len(frames)} frames, {format_srt_time(total_duration)} total, {total_chars} chars")

    if issues:
        print(f"\n{'='*50}")
        print(f"⚠️ {len(issues)} issue(s) found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print(f"\n✅ All checks passed!")


def cmd_render(args: argparse.Namespace) -> None:
    """Render storyboard to FFmpeg concat list."""
    storyboard = load_json(args.storyboard)
    frames = storyboard.get("frames", [])
    output = args.output or "ffmpeg_concat.txt"

    lines = []
    for i, frame in enumerate(frames, 1):
        image_file = frame.get("image_file", f"imgs/frame-{i:03d}.png")
        duration = frame.get("duration_estimated", 1.0)
        lines.append(f"file '{image_file}'")
        lines.append(f"duration {duration}")
        # Duplicate last frame to avoid gap
        lines.append(f"file '{image_file}'")
        lines.append(f"duration 0.05")

    with open(output, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✅ FFmpeg concat list: {output}")


def cmd_compose(args: argparse.Namespace) -> None:
    """Execute FFmpeg assembly (images + audio + BGM + subtitles)."""
    storyboard = load_json(args.storyboard)
    frames = storyboard.get("frames", [])
    output = args.output or "final-output.mp4"

    if not shutil.which("ffmpeg"):
        print("❌ ffmpeg not found. Install with: sudo apt install ffmpeg")
        sys.exit(1)

    # Step 1: Generate concat list
    concat_file = "ffmpeg_concat.txt"
    lines = []
    for i, frame in enumerate(frames, 1):
        image_file = frame.get("image_file", f"imgs/frame-{i:03d}.png")
        duration = frame.get("duration_estimated", 1.0)

        if not os.path.exists(image_file):
            print(f"⚠️ Missing image: {image_file}, skipping frame {i}")
            continue

        lines.append(f"file '{image_file}'")
        lines.append(f"duration {duration}")

    with open(concat_file, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✅ Concat list: {concat_file} ({len(lines) // 2} frames)")

    # Step 2: Check for audio and subtitle files
    audio_file = args.audio or None
    srt_file = args.srt or None
    bgm_file = args.bgm or None

    # Build FFmpeg command
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file]

    if audio_file and os.path.exists(audio_file):
        cmd.extend(["-i", audio_file])

    if bgm_file and os.path.exists(bgm_file):
        cmd.extend(["-i", bgm_file])

    # Filter complex for subtitle overlay
    filter_parts = []
    filter_parts.append("[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black[v]")

    if srt_file and os.path.exists(srt_file):
        # Escape single quotes in path for ffmpeg subtitles filter
        srt_escaped = srt_file.replace("'", r"'\''")
        filter_parts.append(f"[v]subtitles='{srt_escaped}':force_style='FontSize=36,FontName=Noto Sans SC,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Shadow=2'[outv]")
    else:
        filter_parts.append("[v]null[outv]")

    cmd.extend(["-filter_complex", ";".join(filter_parts)])
    cmd.extend(["-map", "[outv]"])

    if audio_file and os.path.exists(audio_file):
        cmd.extend(["-map", "1:a:0", "-c:a", "aac", "-b:a", "192k"])

    cmd.extend(["-c:v", "libx264", "-preset", "medium", "-crf", "23", "-pix_fmt", "yuv420p"])
    cmd.extend(["-shortest"])
    cmd.extend([output])

    print(f"🎬 Running FFmpeg assembly...")
    print(f"   Command: {' '.join(cmd[:10])}...")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"✅ Video assembled: {output} ({size_mb:.1f} MB)")
    else:
        print(f"❌ FFmpeg failed:")
        print(result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auto_compose.py",
        description="FFmpeg video assembly toolkit for Book Video Studio"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # info
    p_info = subparsers.add_parser("info", help="Display storyboard information")
    p_info.add_argument("--storyboard", required=True, help="Path to storyboard.json")

    # srt
    p_srt = subparsers.add_parser("srt", help="Generate SRT subtitle file")
    p_srt.add_argument("--storyboard", required=True, help="Path to storyboard.json")
    p_srt.add_argument("-o", "--output", help="Output SRT file path")

    # verify
    p_verify = subparsers.add_parser("verify", help="Verify storyboard compliance")
    p_verify.add_argument("--storyboard", required=True, help="Path to storyboard.json")

    # render
    p_render = subparsers.add_parser("render", help="Render to FFmpeg concat list")
    p_render.add_argument("--storyboard", required=True, help="Path to storyboard.json")
    p_render.add_argument("-o", "--output", help="Output concat file path")

    # compose
    p_compose = subparsers.add_parser("compose", help="Execute full FFmpeg assembly")
    p_compose.add_argument("--storyboard", required=True, help="Path to storyboard.json")
    p_compose.add_argument("-o", "--output", default="final-output.mp4", help="Output video path")
    p_compose.add_argument("--audio", help="Path to merged audio file (optional)")
    p_compose.add_argument("--srt", help="Path to SRT subtitle file (optional)")
    p_compose.add_argument("--bgm", help="Path to background music file (optional)")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    commands = {
        "info": cmd_info,
        "srt": cmd_srt,
        "verify": cmd_verify,
        "render": cmd_render,
        "compose": cmd_compose,
    }

    commands[args.command](args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
