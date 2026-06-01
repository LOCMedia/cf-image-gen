#!/usr/bin/env python3
"""Generate an image via the Cloudflare Workers AI proxy.

Cross-platform (Windows / Linux / macOS). Stdlib only.

Required env:
  CF_IMAGE_URL       Worker endpoint
  CF_IMAGE_API_KEY   Bearer token
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Generate an image via the Cloudflare Workers AI proxy.",
    )
    p.add_argument("--prompt", required=True, help="Image description")
    p.add_argument("--output", required=True, help="Output file path")
    p.add_argument("--model", help="Workers AI model id (default: @cf/black-forest-labs/flux-1-schnell)")
    p.add_argument("--steps", type=int, help="Sampling steps")
    p.add_argument("--width", type=int, help="Image width (px)")
    p.add_argument("--height", type=int, help="Image height (px)")
    p.add_argument("--seed", type=int, help="RNG seed")
    p.add_argument("--guidance", type=float, help="CFG guidance scale")
    return p.parse_args()


def build_payload(args: argparse.Namespace) -> dict:
    body: dict = {"prompt": args.prompt}
    if args.model:
        body["model"] = args.model
    if args.steps is not None:
        body["num_steps"] = args.steps
    if args.width is not None:
        body["width"] = args.width
    if args.height is not None:
        body["height"] = args.height
    if args.seed is not None:
        body["seed"] = args.seed
    if args.guidance is not None:
        body["guidance"] = args.guidance
    return body


def main() -> int:
    args = parse_args()

    url = os.environ.get("CF_IMAGE_URL")
    key = os.environ.get("CF_IMAGE_API_KEY")
    if not url:
        print("CF_IMAGE_URL not set", file=sys.stderr)
        return 1
    if not key:
        print("CF_IMAGE_API_KEY not set", file=sys.stderr)
        return 1

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(build_payload(args)).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": "cf-image-gen/1.0",
        },
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            model_used = resp.headers.get("X-Model", "default")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code} - error from worker:\n{body}", file=sys.stderr)
        return 1
    except urllib.error.URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        return 1

    output.write_bytes(data)
    print(f"Saved: {output} ({len(data)} bytes, model: {model_used})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
