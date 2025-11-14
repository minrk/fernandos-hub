#!/bin/bash
set -e

# permanently merge stderr into stdout for single log file
exec 2>&1
export PYTHONUNBUFFERED=1
export PATH=/opt/homebrew/bin:$PATH

cd /opt/jupyterhub/jupyterhub
# make sure pixi envs are up-to-date
pixi install -a
# launch jupyterhub
exec pixi run --as-is --environment=hub jupyterhub