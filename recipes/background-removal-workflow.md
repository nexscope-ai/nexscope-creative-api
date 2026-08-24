# Background Removal Workflow

Use [Background Remover API](https://www.nexscope.ai/api-docs/background-remover?co-from=githubcreative) to create a reusable product cutout before a separate creative step.

1. Provide a public product-image URL that satisfies the documented image constraints.
2. Select the documented cutout type that matches the subject.
3. Send one create request and save the returned `taskId`.
4. Retrieve the completed cutout before starting any second API call.
5. Inspect edges, transparent regions, hair, shadows, and product details.

Each additional creative step is a separate request and may consume additional credits.
