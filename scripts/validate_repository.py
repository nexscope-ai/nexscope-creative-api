#!/usr/bin/env python3
"""Validate catalog coverage, examples, links, language, and secret hygiene."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUESTS_PATH = ROOT / "examples" / "requests.json"
CATALOG_JSON_PATH = ROOT / "api-catalog" / "creative-apis.json"
CATALOG_MD_PATH = ROOT / "api-catalog" / "README.md"
README_PATH = ROOT / "README.md"
CHANNEL_CODE = "githubcreative"
EXPECTED_COUNTS = {
    "image-generation-models": 9,
    "video-generation-models": 9,
    "multimodal-ai": 33,
}
TEXT_SUFFIXES = {".md", ".json", ".py", ".mjs", ".sh", ".example", ".yml", ".yaml"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
SECRET_PATTERNS = {
    "GitHub token": re.compile(r"\b(?:ghp|gho|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "Nexscope key": re.compile(r"\bnk[-_][A-Za-z0-9]{12,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}
FORBIDDEN_PUBLIC_PATTERNS = {
    "Disallowed installer command": re.compile(r"\bnpx\s+" + r"skills\s+add\b", re.I),
    "Disallowed channel code": re.compile(r"co-from=" + r"skill(?:\b|&)", re.I),
    "Disallowed repository topic": re.compile(r"\bagent-" + r"skills\b", re.I),
    "Outdated brand name": re.compile(r"\bNexscope " + r"Agent\b", re.I),
    "Outdated brand sentence": re.compile(r"\bNexscope is an " + r"AI agent\b", re.I),
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def validate_relative_links(path: Path, text: str) -> int:
    errors = 0
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if not target.startswith(("./", "../")):
            continue
        relative_target = target.split("#", 1)[0].split("?", 1)[0]
        resolved = (path.parent / relative_target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            fail(f"Relative link leaves repository in {path.relative_to(ROOT)}: {target}")
            errors += 1
            continue
        if not resolved.exists():
            fail(f"Broken relative link in {path.relative_to(ROOT)}: {target}")
            errors += 1
    return errors


def main() -> int:
    errors = 0
    requests = json.loads(REQUESTS_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_JSON_PATH.read_text(encoding="utf-8"))
    catalog_md = CATALOG_MD_PATH.read_text(encoding="utf-8")
    readme = README_PATH.read_text(encoding="utf-8")

    if catalog.get("count") != 51 or len(catalog.get("apis", [])) != 51:
        fail("The machine-readable catalog must contain exactly 51 APIs")
        errors += 1
    if not isinstance(requests, dict) or len(requests) != 51:
        fail("examples/requests.json must contain exactly 51 payloads")
        errors += 1

    entries = catalog.get("apis", [])
    slugs = [item.get("slug") for item in entries]
    names = [item.get("name") for item in entries]
    docs_urls = [item.get("docsUrl") for item in entries]
    if len(set(slugs)) != len(slugs):
        fail("Catalog API slugs must be unique")
        errors += 1
    if len(set(names)) != len(names):
        fail("Catalog API names must be unique")
        errors += 1
    if len(set(docs_urls)) != len(docs_urls):
        fail("Catalog documentation URLs must be unique")
        errors += 1

    counts = Counter(item.get("category") for item in entries)
    if counts != Counter(EXPECTED_COUNTS):
        fail(f"Category counts are wrong: {dict(counts)}")
        errors += 1

    for item in entries:
        slug = item.get("slug")
        if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
            fail(f"Invalid API slug: {slug}")
            errors += 1
            continue
        if item.get("method") != "POST":
            fail(f"Unexpected method for {slug}")
            errors += 1
        if item.get("execution") != "async" or "taskResultEndpoint" not in item:
            fail(f"Async task contract is missing for {slug}")
            errors += 1
        expected_docs = f"https://www.nexscope.ai/api-docs/{slug}?co-from={CHANNEL_CODE}"
        if item.get("docsUrl") != expected_docs:
            fail(f"Wrong documentation URL for {slug}")
            errors += 1
        if expected_docs not in readme or expected_docs not in catalog_md:
            fail(f"README or catalog table is missing {slug}")
            errors += 1

        payload = requests.get(slug)
        if not isinstance(payload, dict):
            fail(f"Payload for {slug} must be a JSON object")
            errors += 1
        payload_path = ROOT / "examples" / "payloads" / f"{slug}.json"
        if not payload_path.is_file():
            fail(f"Missing payload file for {slug}")
            errors += 1
        else:
            on_disk = json.loads(payload_path.read_text(encoding="utf-8"))
            if on_disk != payload:
                fail(f"Payload file does not match requests.json for {slug}")
                errors += 1

    unexpected_payloads = {
        path.stem for path in (ROOT / "examples" / "payloads").glob("*.json")
    } - set(slugs)
    for slug in sorted(unexpected_payloads):
        fail(f"Unexpected payload file: {slug}.json")
        errors += 1

    # Historical entries may link to the current catalog when their public docs are unavailable.
    if len(re.findall(r"^\| \[[^]]+\]\(https://www\.nexscope\.ai/api-docs(?:/|\?)", readme, re.M)) != 51:
        fail("The root README must list all 51 API names and documentation links")
        errors += 1

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts or path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8")
        if CJK_RE.search(text):
            fail(f"CJK character found in public file: {path.relative_to(ROOT)}")
            errors += 1
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                fail(f"Possible {label} found in {path.relative_to(ROOT)}")
                errors += 1
        if path != Path(__file__).resolve():
            for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
                if pattern.search(text):
                    fail(f"{label} found in {path.relative_to(ROOT)}")
                    errors += 1
        if path.suffix == ".md":
            for url in re.findall(r"https://www\.nexscope\.ai/[^\s)>`]*", text):
                if f"co-from={CHANNEL_CODE}" not in url:
                    fail(
                        f"Nexscope website URL is missing co-from={CHANNEL_CODE} "
                        f"in {path.relative_to(ROOT)}: {url}"
                    )
                    errors += 1
            errors += validate_relative_links(path, text)

    if errors:
        print(f"Validation failed with {errors} error(s).", file=sys.stderr)
        return 1

    print("Validation passed for 51 Creative APIs (9 image, 9 video, 33 multimodal).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
