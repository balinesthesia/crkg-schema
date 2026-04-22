# Developer setup

## One-time install

1. Install Python 3.13 and [uv](https://docs.astral.sh/uv/)
2. Clone the repo:
   ```bash
   git clone https://github.com/SHA888/crkg-schema.git
   cd crkg-schema
   ```
3. Sync dependencies:
   ```bash
   uv sync --extra dev
   ```

## Daily workflow

```bash
make check   # fmt + lint + type-check + test
make emit    # regenerate emitted/ artifacts
make test    # pytest only
```

## Expected first-run time

On a modern Linux or macOS machine with a warm PyPI cache, `make check`
should pass within **5 minutes** of cloning.

Windows is best-effort; WSL is recommended.
