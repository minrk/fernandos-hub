#!/bin/bash
set -e

# permanently merge stderr into stdout for single log file
exec 2>&1
export PYTHONUNBUFFERED=1
export PATH=/opt/homebrew/bin:$PATH

# launch ollama
export OLLAMA_MODELS=/opt/ollama
export OLLAMA_NUM_PARALLEL=4
# for private key
export HOME=/opt/ollama
exec pixi run --as-is --environment=user ollama serve