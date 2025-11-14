#!/bin/bash -l
set -e

# merge stdout/stderr for single log file
exec 2>&1

export PYTHONUNBUFFERED=1
# activate with shell-hook to avoid creating subprocesses that don't get killed signaled properly
# don't use pixi shell-hook activation, which sets environment variables we don't want the user to inherit
eval $(mamba shell hook)
mamba activate /opt/jupyterhub/.pixi/envs/user
exec jupyterhub-singleuser "$@"
