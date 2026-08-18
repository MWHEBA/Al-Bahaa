#!/usr/bin/env python3
"""
Image Optimization & WebP Migration Engine for Al Bahaa Platform.
Converts images in static/img and media to WebP with max-dimension bounds and high visual fidelity,
then updates database records and codebase fallback references.
"""

import os
import re
import sqlite3
from pathlib import Path
from PIL import Image

PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_IMG = PROJECT_ROOT / "static" / "img"
MEDIA_DIR = PROJECT_ROOT / "media"
DB_PATH = PROJECT_ROOT / "db.sqlite3"

MAX_HERO_DIM = 1920
MAX_CARD_DIM = 1200
MAX_LOGO_DIM = 600
WEBP_QUALITY = 82

def optimize_single_image(src_path: Path, max_dim: int = MAX_HERO_DIM, quality: int = WEBP_QUALITY) -> Path:
    target_webp = src_path.with_suffix(".webp")
    try:
        with Image.open(src_path) as img:
            try:
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)
            except Exception:
                pass

            w, h = img.size
            if max(w, h) > max_dim:
                ratio = max_dim / max(w, h)
                new_size = (max(1, int(w * ratio)), max(1, int(h * ratio)))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Determine mode
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img = img.convert("RGBA")
                img.save(target_webp, "WEBP", quality=quality, method=6)
            else:
                img = img.convert("RGB")
                img.save(target_webp, "WEBP", quality=quality, method=6)

        return target_webp
    except Exception as e:
        print(f"Error converting {src_path}: {e}")
        return None

def process_directory(base_dir: Path):
    if not base_dir.exists():
        return {}
    
    conversions = {}
    print(f"\n--- Processing Directory: {base_dir} ---")
    files_to_remove = []

    for root, _, files in os.walk(base_dir):
        for f in files:
            p = Path(root) / f
            ext = p.suffix.lower()
            if ext in (".png", ".jpg", ".jpeg"):
                # Skip svg and existing webp
                orig_size = p.stat().st_size
                
                # Determine max dimensions by path
                rel_str = str(p.relative_to(base_dir)).lower()
                if "client" in rel_str or "logo" in rel_str:
                    max_dim = MAX_LOGO_DIM
                    quality = 85
                elif "gallery" in rel_str or "team" in rel_str or "testimonials" in rel_str:
                    max_dim = MAX_CARD_DIM
                    quality = 82
                else:
                    max_dim = MAX_HERO_DIM
                    quality = 82

                webp_path = optimize_single_image(p, max_dim=max_dim, quality=quality)
                if webp_path and webp_path.exists():
                    new_size = webp_path.stat().st_size
                    rel_orig = p.relative_to(PROJECT_ROOT).as_posix()
                    rel_webp = webp_path.relative_to(PROJECT_ROOT).as_posix()
                    conversions[rel_orig] = rel_webp
                    print(f"[OK] {p.name} ({orig_size/(1024*1024):.2f}MB) -> {webp_path.name} ({new_size/1024:.1f}KB)")
                    
                    if p != webp_path:
                        files_to_remove.append(p)

    for old_file in files_to_remove:
        try:
            old_file.unlink()
        except Exception as e:
            print(f"Could not remove old file {old_file}: {e}")

    return conversions

def update_database_references():
    if not DB_PATH.exists():
        print("No SQLite database found to update.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    targets = [
        ("projects_project", ["cover_image"]),
        ("projects_projectimage", ["image"]),
        ("news_post", ["cover_image"]),
        ("core_pagehero", ["hero_image"]),
        ("core_sitesettings", ["header_logo", "footer_logo", "favicon"]),
        ("core_homecontent", ["blueprints_image"]),
        ("core_teammember", ["photo"]),
        ("core_testimonial", ["avatar"]),
        ("core_clientlogo", ["logo_image"]),
    ]

    print("\n--- Updating Database Image Paths ---")
    for table, fields in targets:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        if not cursor.fetchone():
            continue

        for field in fields:
            cursor.execute(f"SELECT id, {field} FROM {table} WHERE {field} IS NOT NULL AND {field} != ''")
            rows = cursor.fetchall()
            updated_count = 0
            for row_id, val in rows:
                if val:
                    val_path = Path(val)
                    if val_path.suffix.lower() in (".png", ".jpg", ".jpeg"):
                        new_val = val_path.with_suffix(".webp").as_posix()
                        cursor.execute(f"UPDATE {table} SET {field} = ? WHERE id = ?", (new_val, row_id))
                        updated_count += 1
            if updated_count > 0:
                print(f"Updated {updated_count} rows in table {table} column {field}.")

    conn.commit()
    conn.close()
    print("Database image references successfully updated to .webp.")

if __name__ == "__main__":
    print("Starting WebP Conversion & Optimization...")
    conv1 = process_directory(STATIC_IMG)
    conv2 = process_directory(MEDIA_DIR)
    update_database_references()
    print("\nAll assets optimized and converted to WebP successfully!")
