# Local AI Scout

Automated intel brief on local/on-device AI developments from X (Twitter).

Pulls tweets → sends to LLM via NanoGPT → outputs a structured, opinionated brief. Zero dependencies beyond Python stdlib.

## Quick Start

```bash
# Set your keys
export NANOGPT_API_KEY="..."
export X_BEARER_TOKEN="AAAA..."  # or X_CONSUMER_KEY + X_API_KEY

# Run it
python3 scout.py
```

## Options

```bash
python3 scout.py                          # Print brief to stdout
python3 scout.py --save                   # Save to briefs/YYYY-MM-DD.md
python3 scout.py --save --save-tweets     # Also save raw tweet JSON
python3 scout.py --from-file tweets.json  # Replay without hitting X API
python3 scout.py --topic "robotics"       # Scout a different topic
```

## Custom Topic / Domain

By default the scout tracks local AI developments. You can point it at any topic:

```bash
# Via CLI argument
python3 scout.py --topic "open source robotics"

# Via environment variable
export SCOUT_FOCUS="distributed databases"
python3 scout.py
```

CLI `--topic` takes priority over the `SCOUT_FOCUS` env var. When a custom topic is set, the scout automatically builds relevant search queries and adapts the system prompt.

## Automate with Cron

```bash
# Daily at 8am
0 8 * * * cd /path/to/local-ai-scout && python3 scout.py --save >> scout.log 2>&1
```

Or use the included GitHub Actions workflow (`.github/workflows/daily-scout.yml`) — set `NANOGPT_API_KEY` and `X_BEARER_TOKEN` as repository secrets.

## Customize

| What | Where |
|------|-------|
| Topic / domain focus | `--topic` CLI arg or `SCOUT_FOCUS` env var |
| Search queries | `config.py` → `DEFAULT_QUERIES` |
| Lookback window | `config.py` → `LOOKBACK_HOURS` |
| LLM model | `config.py` → `LLM_MODEL` |
| Brief format & tone | `prompt.py` → `build_system_prompt()` |

## Cost

~$0.001/run with MiniMax M2.5 via NanoGPT.

## License

MIT
