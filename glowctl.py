#!/usr/bin/env python3
from __future__ import annotations
import argparse
from workflows.engine import generate_media_pack, save_pack

def main():
    parser = argparse.ArgumentParser(prog="glowctl", description="GlowMiniAI - offline workflow demo (no API key needed).")
    parser.add_argument("topic", help="Topic / keyword for the demo pack")
    parser.add_argument("--lang", default="vi", help="Language: vi or en (default: vi)")
    parser.add_argument("--out", default="output", help="Output directory (default: output)")
    args = parser.parse_args()

    res = generate_media_pack(args.topic, args.lang)
    path = save_pack(res, args.out)

    print("✅ Generated pack:", path)
    print("— Outline preview —")
    print(res.outline)

if __name__ == "__main__":
    main()
