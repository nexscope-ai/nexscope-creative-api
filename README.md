<div align="center">

# Nexscope Creative API

**Generate and edit ecommerce images and videos through one API key.**

[![Validate examples](https://github.com/nexscope-ai/nexscope-creative-api/actions/workflows/validate.yml/badge.svg)](https://github.com/nexscope-ai/nexscope-creative-api/actions/workflows/validate.yml)
[![Creative API docs](https://img.shields.io/badge/Creative_API-docs-7c3aed)](https://www.nexscope.ai/api-docs?tab=creative&co-from=githubcreative)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

[Get an API key](https://www.nexscope.ai/seller/api-access?co-from=githubcreative) · [Browse the 51-API snapshot](./api-catalog/README.md) · [Open the Creative API directory](https://www.nexscope.ai/apis/creatives?co-from=githubcreative)

[Explore MCP tools →](https://www.nexscope.ai/mcp?co-from=githubcreative&utm_source=github&utm_medium=referral&utm_campaign=github_mcp_launch&utm_content=nexscope-creative-api_readme_mcp) · [View API docs →](https://www.nexscope.ai/api-docs?co-from=githubcreative&utm_source=github&utm_medium=referral&utm_campaign=github_mcp_launch&utm_content=nexscope-creative-api_readme_api)

</div>

---

Nexscope Creative APIs let developers add ecommerce image generation, video generation, image editing, background removal, virtual try-on, product photography, and marketing-asset workflows to their applications. This repository contains a machine-readable catalog, copy-ready request payloads, dependency-free clients, and integration recipes for the 51 Creative APIs in the published Nexscope catalog snapshot.

## Quick start

### 1. Create an API key

Create or copy a key from [Nexscope API Access](https://www.nexscope.ai/seller/api-access?co-from=githubcreative), keep it private, and export it from your shell.

```bash
export NEXSCOPE_API_KEY="YOUR_API_KEY"
```

### 2. Prepare a request

Start with the included Nano Banana 2 request and replace the placeholder image URL with a public JPG, PNG, or WEBP file that meets the current API requirements.

```json
{
  "imageUrls": ["https://example.com/product.jpg"],
  "prompt": "Keep the product consistent and generate a clean white-background ecommerce hero image.",
  "outputNum": 1,
  "extraParams": {
    "resolution": "2K",
    "aspectRatio": "1:1"
  }
}
```

### 3. Send one request

```bash
python3 examples/python/run.py banana-2-image-generation \
  examples/payloads/banana-2-image-generation.json
```

The response is the direct API payload. Generation APIs may return a task ID instead of a completed asset. Follow the API-specific task-result contract before treating the job as complete.

Try the same payload with Node.js 18+ or cURL:

```bash
node examples/javascript/run.mjs banana-2-image-generation \
  examples/payloads/banana-2-image-generation.json

bash examples/curl/run.sh banana-2-image-generation \
  examples/payloads/banana-2-image-generation.json
```

Each client makes one request and does not retry automatically. Use `--dry-run` as the final argument to validate a request locally without sending it.

## API coverage

**Documentation availability checked November 11, 2026:** The historical public docs for `seedream-5-image-generation` and `ai-draw-edit-image-generation` returned HTTP 404. Their entries and payloads are retained as snapshot references, not verified live integrations. Browse the [current Creative API catalog](https://www.nexscope.ai/api-docs?tab=creative&co-from=githubcreative) for documented options; a missing documentation page does not establish whether an execution endpoint is available.

The current snapshot contains 9 image-generation models, 9 video-generation models, and 33 multimodal creative APIs. Each linked API page is the source of truth for current request fields, response fields, supported options, file limits, credit behavior, and availability.

### Image Generation Models (9)

| API | What it does |
|---|---|
| [Nano Banana Image Generation](https://www.nexscope.ai/api-docs/banana-image-generation?co-from=githubcreative) | Generate ecommerce images with the fixed Nano Banana model from reference images and a prompt, with documented task-result and MCP workflows. |
| [Nano Banana Pro Image Generation](https://www.nexscope.ai/api-docs/banana-pro-image-generation?co-from=githubcreative) | Generate higher-resolution ecommerce images with the fixed Nano Banana Pro model, reference images, prompts, and asynchronous task results. |
| [Nano Banana 2 Image Generation](https://www.nexscope.ai/api-docs/banana-2-image-generation?co-from=githubcreative) | Generate ecommerce images with the fixed Nano Banana 2 model from reference assets and prompts, with documented asynchronous result retrieval. |
| [Nano Banana 2 Lite Image Generation](https://www.nexscope.ai/api-docs/banana-2-lite-image-generation?co-from=githubcreative) | Generate ecommerce images with the fixed Nano Banana 2 Lite model from reference assets and prompts, then retrieve completed task results. |
| [Wan 2.7 Image Generation](https://www.nexscope.ai/api-docs/wan-2-7-image-generation?co-from=githubcreative) | Generate ecommerce images with the fixed Wan 2.7 model using reference images and prompts, with asynchronous task-result retrieval. |
| [Seedream 5 Image Generation — historical snapshot; browse current catalog](https://www.nexscope.ai/api-docs?tab=creative&co-from=githubcreative) | Generate ecommerce images with the fixed Seedream 5 model using references and prompts, with API-key authentication and task results. |
| [Seedream 5 Pro Image Generation](https://www.nexscope.ai/api-docs/seedream-5-pro-image-generation?co-from=githubcreative) | Generate ecommerce images with the fixed Seedream 5 Pro model at supported resolutions, then retrieve Nexscope-hosted task outputs. |
| [GPT Image 2 Generation](https://www.nexscope.ai/api-docs/gpt-image-2-generation?co-from=githubcreative) | Generate ecommerce images with the fixed GPT Image 2 model, selectable quality and resolution, and asynchronous task results. |
| [AI Draw Edit Image Generation — historical snapshot; browse current catalog](https://www.nexscope.ai/api-docs?tab=creative&co-from=githubcreative) | Generate or edit ecommerce images with the fixed AI Draw Edit model, reference assets, prompts, and asynchronous Nexscope task-result retrieval. |

### Video Generation Models (9)

| API | What it does |
|---|---|
| [Seedance 2.0 Video Generation](https://www.nexscope.ai/api-docs/seedance-2-0-video-generation?co-from=githubcreative) | Generate ecommerce videos with Seedance 2.0 from a primary image or multi-image references, then retrieve completed Nexscope-hosted task results. |
| [Seedance 2.0 Fast Video Generation](https://www.nexscope.ai/api-docs/seedance-2-0-fast-video-generation?co-from=githubcreative) | Generate ecommerce videos faster with Seedance 2.0 Fast using primary or multi-image references, then retrieve the completed Nexscope-hosted result. |
| [Seedance 2.0 Mini Video Generation](https://www.nexscope.ai/api-docs/seedance-2-0-mini-video-generation?co-from=githubcreative) | Generate compact ecommerce videos with Seedance 2.0 Mini from primary or multi-image references and retrieve the completed Nexscope-hosted result. |
| [Seedance 2.5 Video Generation](https://www.nexscope.ai/api-docs/seedance-2-5-video-generation?co-from=githubcreative) | Generate ecommerce videos with Seedance 2.5 from primary or multi-image references, including up to 30 images and supported 30-second outputs. |
| [Kling 2.6 Video Generation](https://www.nexscope.ai/api-docs/kling-2-6-video-generation?co-from=githubcreative) | Generate ecommerce videos with Kling 2.6 using first-frame, first-and-last-frame, or multi-image references and retrieve task results. |
| [Kling 3 Omni Video Generation](https://www.nexscope.ai/api-docs/kling-3-omni-video-generation?co-from=githubcreative) | Generate ecommerce videos with Kling 3 Omni from first-and-last-frame or multi-image references and retrieve completed Nexscope task outputs. |
| [Wan 2.6 Video Generation](https://www.nexscope.ai/api-docs/wan-2-6-video-generation?co-from=githubcreative) | Generate ecommerce videos with Wan 2.6 from a required primary image, supported duration and resolution settings, and single or multi camera control. |
| [Hailuo 2.3 Video Generation](https://www.nexscope.ai/api-docs/hailuo-2-3-video-generation?co-from=githubcreative) | Generate adaptive-aspect-ratio ecommerce videos with Hailuo 2.3 from a required primary image at supported durations and resolutions. |
| [Happy Horse 2 Video Generation](https://www.nexscope.ai/api-docs/happy-horse-2-video-generation?co-from=githubcreative) | Generate ecommerce videos with Happy Horse 2 from one to nine required reference images, then retrieve the completed Nexscope-hosted result. |

### Multimodal AI (33)

| API | What it does |
|---|---|
| [AI Model Swap API](https://www.nexscope.ai/api-docs/ai-model-swap?co-from=githubcreative) | Place an ecommerce product image onto a target model. |
| [AI Model Swap API 2.0](https://www.nexscope.ai/api-docs/ai-model-swap-2-0?co-from=githubcreative) | Swap a product image onto a fixed model reference with the version 2.0 workflow. |
| [AI Model Scene & Background Replacement API](https://www.nexscope.ai/api-docs/ai-model-scene-background-replacement?co-from=githubcreative) | Place a model image into a new scene or background. |
| [AI Clothes Changer API for Tops & Bottoms](https://www.nexscope.ai/api-docs/ai-clothes-changer-for-tops-bottoms?co-from=githubcreative) | Generate virtual try-on images for separate upper and lower garments. |
| [AI Suit Virtual Try-On API](https://www.nexscope.ai/api-docs/ai-suit-virtual-try-on?co-from=githubcreative) | Generate virtual try-on images for one-piece outfits. |
| [Virtual Try-On API](https://www.nexscope.ai/api-docs/virtual-try-on?co-from=githubcreative) | Place a product naturally onto a person or model image. |
| [Product Replacement API](https://www.nexscope.ai/api-docs/product-replacement?co-from=githubcreative) | Replace a selected product region in an ecommerce image. |
| [Product Scene Variations API](https://www.nexscope.ai/api-docs/product-scene-variations?co-from=githubcreative) | Create multiple product-scene variations from an input image. |
| [AI Background Generator API](https://www.nexscope.ai/api-docs/ai-background-generator?co-from=githubcreative) | Generate an ecommerce scene image from a text prompt. |
| [Similar Image Variations API](https://www.nexscope.ai/api-docs/similar-image-variations?co-from=githubcreative) | Create visually similar image variations from an input image. |
| [Background Remover API](https://www.nexscope.ai/api-docs/background-remover?co-from=githubcreative) | Automatically remove an image background for clean product cutouts. |
| [Fine Cutout Image Segmentation API](https://www.nexscope.ai/api-docs/fine-cutout-image-segmentation?co-from=githubcreative) | Create a precision image cutout and return the completed result. |
| [Image Upscale API](https://www.nexscope.ai/api-docs/image-upscale?co-from=githubcreative) | Upscale and enhance image resolution for clearer ecommerce visuals. |
| [Smart Image Outpainting API](https://www.nexscope.ai/api-docs/smart-image-outpainting?co-from=githubcreative) | Expand an image canvas with AI-generated surrounding content. |
| [Image Translation API](https://www.nexscope.ai/api-docs/image-translation?co-from=githubcreative) | Translate text contained inside an image. |
| [AI Hand Repair API](https://www.nexscope.ai/api-docs/ai-hand-repair?co-from=githubcreative) | Repair distorted or malformed hands in an image. |
| [Image Inpainting API](https://www.nexscope.ai/api-docs/image-inpainting?co-from=githubcreative) | Redraw a masked area of an image with AI inpainting. |
| [Print & Pattern Extraction API](https://www.nexscope.ai/api-docs/print-pattern-extraction?co-from=githubcreative) | Extract printed artwork or patterns from an input image. |
| [Object Eraser & Image Object Removal API](https://www.nexscope.ai/api-docs/object-eraser-image-object-removal?co-from=githubcreative) | Remove masked objects from an image and reconstruct the cleared area. |
| [Jewelry Text Design API](https://www.nexscope.ai/api-docs/jewelry-text-design?co-from=githubcreative) | Generate linked text designs for jewelry or accessory products. |
| [Handheld Product Mockup API](https://www.nexscope.ai/api-docs/handheld-product-mockup?co-from=githubcreative) | Place a product naturally into a handheld scene or mockup. |
| [Image Captioning API](https://www.nexscope.ai/api-docs/image-captioning?co-from=githubcreative) | Extract a reusable text prompt from an input image. |
| [Product Image Enhancement API](https://www.nexscope.ai/api-docs/product-image-enhancement?co-from=githubcreative) | Retouch and enhance a product image for cleaner ecommerce presentation. |
| [Image Text Editing API](https://www.nexscope.ai/api-docs/image-text-editing?co-from=githubcreative) | Remove or edit text inside an image. |
| [Smart Image Edit & Manipulation API v3](https://www.nexscope.ai/api-docs/smart-image-edit-manipulation-v3?co-from=githubcreative) | Edit and manipulate an image from a natural-language instruction prompt. |
| [Smart Multi-Image Editing API v3](https://www.nexscope.ai/api-docs/smart-multi-image-editing-v3?co-from=githubcreative) | Fuse and edit multiple images with a natural-language instruction prompt. Review authentication, request parameters, and response fields. |
| [AI Video Reclone API](https://www.nexscope.ai/api-docs/ai-video-reclone?co-from=githubcreative) | Recreate a product marketing video from reference assets. |
| [AI Product Marketing Image Set API v4](https://www.nexscope.ai/api-docs/ai-product-marketing-image-set-v4?co-from=githubcreative) | Generate coordinated product marketing image sets with the version 4 workflow. Review authentication, request parameters, and response fields. |
| [AI Apparel Image Set & Photography API v3](https://www.nexscope.ai/api-docs/ai-apparel-image-set-photography-v3?co-from=githubcreative) | Generate coordinated apparel marketing and product-photography image sets. Review authentication, request parameters, and response fields. |
| [AI Model Pose Generation API](https://www.nexscope.ai/api-docs/ai-model-pose-generation?co-from=githubcreative) | Generate new pose variations from an existing model image. |
| [Sales Talking Video API](https://www.nexscope.ai/api-docs/sales-talking-video?co-from=githubcreative) | Generate a talking sales video for ecommerce promotion. |
| [Product Logo Detection & Removal API](https://www.nexscope.ai/api-docs/product-logo-detection-removal?co-from=githubcreative) | Detect and remove logos from product images. |
| [One-Click Image Recoloring API v2](https://www.nexscope.ai/api-docs/one-click-image-recoloring-v2?co-from=githubcreative) | Change product colors in an image with the version 2 workflow. |

## Asynchronous generation jobs

All 51 APIs in this snapshot use a create-and-query flow. A successful create request does not mean the generated asset is ready.

1. Send the API-specific create request once.
2. Save the returned `taskId`.
3. Wait at least five seconds before the first result query.
4. Query the API-specific task-result endpoint with progressive backoff while the task is `PENDING` or `RUNNING`.
5. Use an output only after the result reports `SUCCESS`.
6. Stop and surface the documented error when the task reports `FAILED` or `TIMEOUT`.

Do not create a second generation request merely because the first task is still processing. Additional requests may consume additional credits.

The common task-result path is:

```text
GET https://api.nexscope.ai/api/skill-api/v1/skills/{api-slug}/tasks/{taskId}
```

## Repository layout

```text
nexscope-creative-api/
├── api-catalog/             # Human- and machine-readable Creative API directory
├── examples/
│   ├── curl/                # Generic cURL runner
│   ├── javascript/          # Dependency-free Node.js client
│   ├── python/              # Dependency-free Python client
│   ├── payloads/            # One sample request per published API
│   └── requests.json        # Machine-readable payload index
├── recipes/                 # Multi-step ecommerce integration patterns
└── scripts/                 # Repository validation
```

## Authentication and errors

Send the API key as a bearer token:

```text
Authorization: Bearer YOUR_API_KEY
```

Handle the status classes documented by the selected API:

| Status | Meaning |
|---|---|
| `200` | The request reached the API. Inspect the direct response payload and task state. |
| `400` | The request JSON or required API parameters are invalid. |
| `401` | The API key is missing or invalid. |
| `403` | The account is authenticated but does not have access to the API or resource. |
| `429` | The request was rate limited. Back off before retrying. |
| `5xx` | Nexscope or an upstream dependency failed. |

Do not log API keys, paste them into issues, commit them to a repository, expose them in browser-delivered JavaScript, or include them in screenshots.

## Media inputs

Supported formats, file counts, dimensions, sizes, durations, aspect ratios, and reference-image requirements differ by API. Use the individual API documentation instead of applying one API's limits to another. The sample payloads use placeholder public URLs and do not upload customer assets.

## Credits and production use

- Calls may consume account credits.
- The final charged amount may be available only after an asynchronous result completes.
- This repository does not promise free access, pricing, throughput, latency, availability, or generated-output quality.
- Production integrations should use secure secret storage, request validation, timeouts, explicit task-state handling, observability, and controlled retry policies.
- The example clients are integration aids, not a production SDK.

## Source of truth

This repository is an integration aid. The individual Nexscope API documentation page is the source of truth for current request fields, response fields, supported options, file limits, credits, and availability. The catalog and examples in this repository are versioned snapshots and may require updates when the hosted API changes.

## Contributing

Bug reports and example improvements are welcome. Read [CONTRIBUTING.md](./CONTRIBUTING.md) before opening a pull request. For security-sensitive reports, follow [SECURITY.md](./SECURITY.md).

## License

The documentation and example code in this repository are available under the [MIT License](./LICENSE). Access to the hosted Nexscope APIs is governed separately by Nexscope's service terms and account rules.

---

Built by [Nexscope](https://www.nexscope.ai/?co-from=githubcreative) — ecommerce data-to-action and creative APIs for product images and videos.

Historical documentation URL (404 on November 11, 2026): `https://www.nexscope.ai/api-docs/seedream-5-image-generation?co-from=githubcreative`.

Historical documentation URL (404 on November 11, 2026): `https://www.nexscope.ai/api-docs/ai-draw-edit-image-generation?co-from=githubcreative`.
