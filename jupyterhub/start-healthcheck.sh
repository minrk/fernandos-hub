#!/bin/bash
set -e

# permanently merge stderr into stdout for single log file
exec 2>&1
export PYTHONUNBUFFERED=1
export PATH=/opt/homebrew/bin:$PATH

cd /opt/jupyterhub
# launch healthcheck
exec pixi run --as-is --environment=healthcheck healthcheck
