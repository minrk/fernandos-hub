#!/bin/bash -l
set -e

# merge stdout/stderr for single log file
exec 2>&1

export PYTHONUNBUFFERED=1
# activate with shell hook
# don't use pixi shell-hook activation, which sets environment variables we don't want the user to inherit
source /opt/conda/etc/profile.d/conda.sh
source /opt/conda/etc/profile.d/mamba.sh
# use conda activation because mamba 2 activation is broken
conda activate /opt/jupyterhub/.pixi/envs/user
exec jupyterhub-singleuser "$@"
