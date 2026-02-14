# Search queries — each targets a different slice of local AI.
# Edit these as your interests evolve.
QUERIES = [
    # Core local inference ecosystem
    '"llama.cpp" OR "llamacpp" OR "gguf" OR "mlx" OR "ollama" -is:retweet',

    # New local model releases
    '("local model" OR "local llm" OR "on-device" OR "edge ai" OR "run locally")'
    ' ("release" OR "launch" OR "open source" OR "weights") -is:retweet',

    # Quantization and optimization
    '("quantized" OR "quantization" OR "Q4_K" OR "Q5_K" OR "AWQ" OR "GPTQ")'
    ' ("model" OR "llm") -is:retweet',

    # Small / efficient models
    '("small language model" OR "SLM" OR "tiny model" OR "efficient model") -is:retweet',
]

# ─── TUNING ───────────────────────────────────────────────────────────────────

LOOKBACK_HOURS = 24          # How far back to search (max 168 for recent search)
MAX_RESULTS_PER_QUERY = 20   # Per query, max 100

# LLM API settings (NanoGPT — OpenAI-compatible)
LLM_MODEL = "minimax/minimax-m2.5"  # Open source, ~$0.001/run
MAX_TOKENS = 4096
