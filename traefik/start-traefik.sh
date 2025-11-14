#!/bin/bash
set -e

# merge stdout/stderr for single log file
exec 2>&1

export PATH=/opt/homebrew/bin:$PATH
# launch traefik
exec pixi run --as-is --environment=hub proxy
