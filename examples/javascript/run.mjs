#!/usr/bin/env node

import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

function fail(message, code = 2) {
  console.error(message);
  process.exit(code);
}

const [, , apiSlug, payloadPath, dryRunFlag] = process.argv;
if (!apiSlug || !payloadPath || (dryRunFlag && dryRunFlag !== "--dry-run")) {
  fail(`Usage: ${process.argv[1]} <api-slug> <payload.json> [--dry-run]`);
}

if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(apiSlug)) {
  fail(`Invalid Creative API slug: ${apiSlug}`);
}

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const catalogPath = resolve(scriptDirectory, "../../api-catalog/creative-apis.json");

let catalog;
let payload;
try {
  catalog = JSON.parse(await readFile(catalogPath, "utf8"));
  payload = JSON.parse(await readFile(payloadPath, "utf8"));
} catch (error) {
  fail(`Could not read catalog or payload: ${error.message}`);
}

if (!catalog.apis.some((item) => item.slug === apiSlug)) {
  fail(`API slug is not present in the Creative API catalog: ${apiSlug}`);
}
if (!payload || Array.isArray(payload) || typeof payload !== "object") {
  fail("Payload must be a JSON object");
}

const apiBase = (process.env.NEXSCOPE_PROXY_BASE || "https://api.nexscope.ai").replace(/\/$/, "");
const endpoint = `${apiBase}/api/skill-api/v1/skills/${apiSlug}/run`;

if (dryRunFlag === "--dry-run") {
  console.log(JSON.stringify({ method: "POST", endpoint, payload }, null, 2));
  process.exit(0);
}

const apiKey = (process.env.NEXSCOPE_API_KEY || "").trim();
if (!apiKey) {
  fail("NEXSCOPE_API_KEY is required unless --dry-run is used");
}

let response;
try {
  response = await fetch(endpoint, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(payload),
    signal: AbortSignal.timeout(120_000),
  });
} catch (error) {
  fail(`Connection failed: ${error.message}`, 1);
}

const body = await response.text();
if (!response.ok) {
  console.error(body || `HTTP ${response.status}`);
  process.exit(1);
}

try {
  console.log(JSON.stringify(JSON.parse(body), null, 2));
} catch {
  console.log(body);
}
