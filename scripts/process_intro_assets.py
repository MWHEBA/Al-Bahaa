#!/usr/bin/env python3
"""
AL BAHAA CONTRACTING - DYNAMIC INTRO & BRAND ASSET BUILD PIPELINE
Automatically optimizes, fast-starts, extracts posters, and synchronizes assets with WhiteNoise.
"""

import os
import sys
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_cmd(cmd, desc):
    print(f"[*] {desc}...")
    res = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] Error in {desc}:")
        print(res.stderr)
        return False
    return True

def process_assets(source_video="logo animation.mp4"):
    source_path = BASE_DIR / source_video
    if not source_path.exists():
        print(f"[!] Source video not found: {source_path}")
        return False

    video_dest_dir = BASE_DIR / "static" / "video"
    video_dest_dir.mkdir(parents=True, exist_ok=True)

    dest_mp4 = video_dest_dir / "logo-intro.mp4"
    dest_poster = video_dest_dir / "logo-intro-poster.webp"

    # 1. Enforce +faststart to place moov atom at beginning
    faststart_cmd = [
        "ffmpeg", "-y", "-i", str(source_path),
        "-c:v", "copy", "-c:a", "copy",
        "-movflags", "+faststart",
        str(dest_mp4)
    ]
    if not run_cmd(faststart_cmd, "Applying faststart container optimization"):
        return False

    # 2. Extract high-quality poster of the first frame
    poster_cmd = [
        "ffmpeg", "-y", "-ss", "00:00:00.040", "-i", str(dest_mp4),
        "-vframes", "1",
        "-q:v", "90",
        str(dest_poster)
    ]
    if not run_cmd(poster_cmd, "Extracting zero-delay WebP poster"):
        return False

    # 3. Trigger collectstatic to update WhiteNoise hashed manifest
    collectstatic_cmd = [
        sys.executable, "manage.py", "collectstatic", "--noinput"
    ]
    run_cmd(collectstatic_cmd, "Updating WhiteNoise CompressedManifestStaticFilesStorage")

    print("[+] All media assets successfully processed and production-ready!")
    return True

if __name__ == "__main__":
    video_file = sys.argv[1] if len(sys.argv) > 1 else "logo animation.mp4"
    success = process_assets(video_file)
    sys.exit(0 if success else 1)
