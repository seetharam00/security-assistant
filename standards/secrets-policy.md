# Secrets policy

- Never commit API keys, passwords, or tokens to source control.
- Store secrets in environment variables or a .env file excluded from Git.
- If a secret is committed, rotate it immediately, then remove it from history.
- Critical secret findings must be fixed within 24 hours.
