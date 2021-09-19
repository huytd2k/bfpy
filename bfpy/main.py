import argparse

from bfpy.executor import Executor
from bfpy.tokenizer import tokenizer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="python brainf*ck interpreter")
    parser.add_argument("filename")

    args = parser.parse_args()

    with open(args.filename, "r") as f:
        text = f.read()
        executor = Executor(100, tokenizer(text))
        executor.exec()
