#!/usr/bin/env bash
# Run pipeline with env vars; use main_subprocess.py to avoid TF in main process (fixes mutex/Abort on macOS).
# From project root: bash scripts/run_main.sh
cd "$(dirname "$0")/.."
export TF_NUM_INTEROP_THREADS=1
export TF_NUM_INTRAOP_THREADS=1
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
# main_subprocess.py runs each stage in a separate process so the runner never imports TensorFlow
exec python main_subprocess.py "$@"
