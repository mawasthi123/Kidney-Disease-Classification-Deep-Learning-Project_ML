"""
Run the full pipeline by executing each stage in a separate process.
Use this if main.py crashes with "mutex lock failed" / Abort trap: 6 on macOS.
Optional: --from-stage N (1-4) to start from stage N (e.g. 2 to skip data download).
"""
import argparse
import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
STAGES = [
    "src/cnnClassifier/pipeline/stage_01_data_ingestion.py",
    "src/cnnClassifier/pipeline/stage_02_prepare_base_model.py",
    "src/cnnClassifier/pipeline/stage_03_model_training.py",
    "src/cnnClassifier/pipeline/stage_04_model_evaluation.py",
]


def main():
    parser = argparse.ArgumentParser(description="Run pipeline stages in subprocesses")
    parser.add_argument("--from-stage", type=int, default=1, choices=(1, 2, 3, 4), help="Start from stage N (default 1)")
    args = parser.parse_args()
    start = args.from_stage - 1
    to_run = STAGES[start:]
    env = os.environ.copy()
    env["TF_NUM_INTEROP_THREADS"] = "1"
    env["TF_NUM_INTRAOP_THREADS"] = "1"
    env["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
    for i, script in enumerate(to_run, start + 1):
        path = os.path.join(REPO_ROOT, script)
        if not os.path.isfile(path):
            print(f"Missing: {path}", file=sys.stderr)
            sys.exit(1)
        print(f">>>>>> Stage {i}/4: {script}")
        r = subprocess.run([sys.executable, path], cwd=REPO_ROOT, env=env)
        if r.returncode != 0:
            print(f"Stage failed with exit code {r.returncode}", file=sys.stderr)
            sys.exit(r.returncode)
    print("All stages completed. Run: cp artifacts/training/model.h5 model/model.h5")


if __name__ == "__main__":
    main()
