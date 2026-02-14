# CLAUDE.md

## What this project does

Automated local AI intel scout. Pulls tweets about local/on-device AI from the X API, sends them to an LLM via NanoGPT, and generates a structured intel brief.

## How to run

```bash
# Daily brief (prints to stdout)
python3 scout.py

# Save brief + raw tweets
python3 scout.py --save --save-tweets

# Replay from saved tweets (no X API call)
python3 scout.py --from-file briefs/2026-02-14-tweets.json
```

## Required env vars

- `NANOGPT_API_KEY` — NanoGPT API key
- `X_BEARER_TOKEN` — X API bearer token

OR instead of X_BEARER_TOKEN:
- `X_CONSUMER_KEY` + `X_API_KEY` — will auto-exchange for bearer token

## Optional env vars

- `SCOUT_FOCUS` — Custom topic/domain to scout (default: local AI / local LLMs)

## Project structure

- `scout.py` — Main pipeline script (pull → brief → output)
- `config.py` — Search queries, lookback window, model settings
- `prompt.py` — System prompt for the LLM call
- `briefs/` — Saved briefs and raw tweet JSON (gitignored except .gitkeep)

## Editing guide

- **Add/remove search queries** → edit `config.py` QUERIES list
- **Change model or token budget** → edit `config.py` LLM_MODEL / MAX_TOKENS
- **Change topic/focus** → `--topic` CLI arg or `SCOUT_FOCUS` env var
- **Change brief format or tone** → edit `prompt.py` `build_system_prompt()`
- **Change lookback window** → edit `config.py` LOOKBACK_HOURS (max 168)

## No external dependencies

Stdlib only. No pip install needed.
