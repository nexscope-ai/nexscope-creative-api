# Product Video Workflow

Choose a model from the [Video Generation Models](../api-catalog/README.md#video-generation-models-9) section, then follow its documented input contract.

1. Prepare public reference images and a motion-focused prompt.
2. Select only supported duration, resolution, aspect-ratio, and camera options.
3. Send the generation request once and save the returned `taskId`.
4. Wait at least five seconds before the first result query.
5. Use progressive backoff while the task remains `PENDING` or `RUNNING`.
6. Review product consistency, motion, framing, duration, artifacts, and audio when present.

Do not submit another generation request merely because the first task is still processing.
