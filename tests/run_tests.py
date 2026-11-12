#!/usr/bin/env python3
"""Compares the self-hosted compiler with the reference compiler on tests/cases/*.memeasm.

For every case, the reference runs as `memeasm -S -o expected.S case.memeasm`:
* if it fails, ./memeasm-self must fail too: exit status 1 and no output on stdout;
* otherwise ./memeasm-self < case.memeasm must exit with 0 and print exactly expected.S.

Randomness: the line of the `.LConfusedStonks_0:` label is removed from both outputs before
comparing (its position is random), but both must contain it or neither. Cases using
`perfectly balanced as all things should be` delete random commands, so for them the output
is only checked to assemble with gas.

Environment: REF_MEMEASM (reference, default memeasm from PATH), SELF_MEMEASM (default ./memeasm-self), TEST_OUT (default tests/out).

Usage: tests/run_tests.py [-v] [-k] [name-substring ...]
  -v  show the diff of every failing case
  -k  keep going quietly (only print failures and the summary)
"""
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "tests", "cases")
OUT = os.environ.get("TEST_OUT", os.path.join(ROOT, "tests", "out"))
REF = os.environ.get("REF_MEMEASM", "memeasm")
SELF = os.environ.get("SELF_MEMEASM", os.path.join(ROOT, "memeasm-self"))
X86_CC = os.environ.get("X86_CC", "x86_64-linux-gnu-gcc")
CONFUSED = re.compile(rb"^\t\.LConfusedStonks_0:\n", re.M)
BALANCED = re.compile(rb"^[ \t]*perfectly balanced as all things should be[ \t]*\r?$", re.M)


def run_case(name):
    src = os.path.join(CASES, name)
    base = os.path.join(OUT, name[: -len(".memeasm")])
    with open(src, "rb") as f:
        data = f.read()

    exp_path = base + ".expected.S"
    if os.path.exists(exp_path):
        os.remove(exp_path)
    ref = subprocess.run([REF, "-S", "-o", exp_path, src], capture_output=True)
    try:
        ours = subprocess.run([SELF], input=data, capture_output=True, timeout=60)
    except subprocess.TimeoutExpired:
        return name, False, "timeout"
    with open(base + ".actual.S", "wb") as f:
        f.write(ours.stdout)

    if ref.returncode != 0:
        if ours.returncode == 1 and ours.stdout == b"":
            return name, True, "rejected as expected"
        return name, False, f"reference rejects it, but ours exited {ours.returncode} with {len(ours.stdout)} bytes of output"

    if ours.returncode != 0:
        return name, False, f"reference accepts it, but ours exited {ours.returncode}"

    with open(exp_path, "rb") as f:
        expected = f.read()
    actual = ours.stdout

    if BALANCED.search(data):
        obj = base + ".o"
        asm = subprocess.run([X86_CC, "-c", "-x", "assembler", "-o", obj, "-"], input=actual, capture_output=True)
        if asm.returncode != 0:
            return name, False, "perfectly balanced: gas rejects our output:\n" + asm.stderr.decode(errors="replace")
        return name, True, "perfectly balanced: assembles"

    if bool(CONFUSED.search(expected)) != bool(CONFUSED.search(actual)):
        return name, False, "the confused stonks label is missing or superfluous"
    if CONFUSED.sub(b"", expected) != CONFUSED.sub(b"", actual):
        return name, False, "output differs"
    return name, True, "identical"


def main():
    args = sys.argv[1:]
    verbose = "-v" in args
    quiet = "-k" in args
    filters = [a for a in args if not a.startswith("-")]
    os.makedirs(OUT, exist_ok=True)
    names = sorted(n for n in os.listdir(CASES) if n.endswith(".memeasm"))
    if filters:
        names = [n for n in names if any(f in n for f in filters)]

    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        results = list(pool.map(run_case, names))

    failed = 0
    for name, ok, message in results:
        if not ok:
            failed += 1
        if not ok or not quiet:
            print(f"{'PASS' if ok else 'FAIL'} {name}: {message}")
        if not ok and verbose and message == "output differs":
            base = os.path.join(OUT, name[: -len(".memeasm")])
            subprocess.run(["diff", base + ".expected.S", base + ".actual.S"])
    print(f"\n{len(results) - failed}/{len(results)} passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
