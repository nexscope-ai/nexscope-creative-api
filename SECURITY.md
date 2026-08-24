# Security Policy

## Reporting a vulnerability

Do not disclose security vulnerabilities, API keys, account details, customer assets, or sensitive response data in a public GitHub issue.

Report security-sensitive problems to [Nexscope Support](mailto:service@nexscope.ai) with enough information to reproduce the issue safely. Remove secrets and personal data from logs or screenshots before sending them.

## API key handling

- Store API keys in environment variables or a managed secret store.
- Never commit `.env` files or hard-coded credentials.
- Do not expose API keys in browser-delivered JavaScript.
- Rotate a key immediately if it may have been disclosed.
- Use separate keys and least-privilege environments where account controls allow it.

The validation workflow checks public text files for common secret patterns, but automated scanning does not replace careful review.
