# Examples

The example clients send one API-specific JSON payload to the Nexscope public API gateway. They use only standard language features and do not install third-party dependencies.

## Run without sending

Append `--dry-run` to inspect the method, endpoint, and payload without requiring an API key or making a network request.

```bash
python3 examples/python/run.py background-remover \
  examples/payloads/background-remover.json --dry-run
```

## Send one request

Set `NEXSCOPE_API_KEY`, then choose one client:

```bash
python3 examples/python/run.py <api-slug> <payload.json>
node examples/javascript/run.mjs <api-slug> <payload.json>
bash examples/curl/run.sh <api-slug> <payload.json>
```

The clients do not retry automatically. They print the direct API response and return a non-zero exit code for transport or HTTP failures.
