#!/usr/bin/env python3
"""Run one Nexscope Creative API request with Python's standard library."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "api-catalog" / "creative-apis.json"


def fail(message: str, code: int = 2) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def main() -> None:
    if len(sys.argv) not in {3, 4} or (len(sys.argv) == 4 and sys.argv[3] != "--dry-run"):
        fail(f"Usage: {sys.argv[0]} <api-slug> <payload.json> [--dry-run]")

    api_slug = sys.argv[1]
    payload_path = Path(sys.argv[2])
    dry_run = len(sys.argv) == 4
    api_base = os.environ.get("NEXSCOPE_PROXY_BASE", "https://api.nexscope.ai").rstrip("/")

    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", api_slug):
        fail(f"Invalid Creative API slug: {api_slug}")
    if not payload_path.is_file():
        fail(f"Payload file not found: {payload_path}")

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    allowed_slugs = {item["slug"] for item in catalog["apis"]}
    if api_slug not in allowed_slugs:
        fail(f"API slug is not present in the Creative API catalog: {api_slug}")

    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        fail(f"Could not read payload: {error}")
    if not isinstance(payload, dict):
        fail("Payload must be a JSON object")

    endpoint = f"{api_base}/api/skill-api/v1/skills/{api_slug}/run"
    if dry_run:
        print(
            json.dumps(
                {"method": "POST", "endpoint": endpoint, "payload": payload},
                indent=2,
                ensure_ascii=False,
            )
        )
        return

    api_key = os.environ.get("NEXSCOPE_API_KEY", "").strip()
    if not api_key:
        fail("NEXSCOPE_API_KEY is required unless --dry-run is used")

    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=120) as response:
            body = response.read().decode("utf-8", errors="replace")
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        print(body or f"HTTP {error.code}: {error.reason}", file=sys.stderr)
        raise SystemExit(1) from error
    except URLError as error:
        fail(f"Connection failed: {error.reason}", 1)

    try:
        print(json.dumps(json.loads(body), indent=2, ensure_ascii=False))
    except json.JSONDecodeError:
        print(body)


if __name__ == "__main__":
    main()
