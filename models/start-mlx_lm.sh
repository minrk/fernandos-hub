#!/bin/bash
set -e

# permanently merge stderr into stdout for single log file
exec 2>&1
export PYTHONUNBUFFERED=1
export PATH=/opt/homebrew/bin:$PATH

# launch mlx_lm.server
export HF_HOME=/opt/huggingface
exec pixi run --as-is --environment=user mlx_lm.server