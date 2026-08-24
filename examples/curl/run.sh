#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 || ( $# -eq 3 && "$3" != "--dry-run" ) ]]; then
  echo "Usage: $0 <api-slug> <payload.json> [--dry-run]" >&2
  exit 2
fi

api_slug="$1"
payload_file="$2"
dry_run="${3:-}"
api_base="${NEXSCOPE_PROXY_BASE:-https://api.nexscope.ai}"
script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
catalog_file="${script_directory}/../../api-catalog/creative-apis.json"

if [[ ! "$api_slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Invalid Creative API slug: $api_slug" >&2
  exit 2
fi

if [[ ! -f "$payload_file" ]]; then
  echo "Payload file not found: $payload_file" >&2
  exit 2
fi

if ! grep -Fq "\"slug\": \"${api_slug}\"" "$catalog_file"; then
  echo "API slug is not present in the Creative API catalog: $api_slug" >&2
  exit 2
fi

endpoint="${api_base%/}/api/skill-api/v1/skills/${api_slug}/run"

if [[ "$dry_run" == "--dry-run" ]]; then
  printf 'POST %s\n' "$endpoint"
  python3 -m json.tool "$payload_file"
  exit 0
fi

if [[ -z "${NEXSCOPE_API_KEY:-}" ]]; then
  echo "NEXSCOPE_API_KEY is required unless --dry-run is used" >&2
  exit 2
fi

curl --fail-with-body --silent --show-error \
  --max-time 120 \
  --request POST \
  "$endpoint" \
  --header "Authorization: Bearer ${NEXSCOPE_API_KEY}" \
  --header "Content-Type: application/json" \
  --data-binary "@${payload_file}"
