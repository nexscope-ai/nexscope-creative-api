# Ecommerce Hero Image

Use [Nano Banana 2 Image Generation](https://www.nexscope.ai/api-docs/banana-2-image-generation?co-from=githubcreative) to create a product-focused hero image from public reference assets.

1. Confirm that every reference image satisfies the API's current format, size, and count requirements.
2. Describe the product details that must remain unchanged, the target background, composition, and aspect ratio.
3. Send the create request once and save the returned `taskId`.
4. Query the documented task-result endpoint with progressive backoff.
5. Review product identity, text, proportions, and visible defects before using the result.

The included request is [`banana-2-image-generation.json`](../examples/payloads/banana-2-image-generation.json).
