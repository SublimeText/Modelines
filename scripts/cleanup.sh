#!/bin/bash
set -euo pipefail


cd "$(dirname "$0")/.."
# Note: Though not strictly equivalent, this could also be `git clean -xffd`…
find . \( -name "*.pyc" -o -name "build" -o -name "dist" \) -exec rm -frv {} +
