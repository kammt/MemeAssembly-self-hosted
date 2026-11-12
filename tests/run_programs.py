#!/usr/bin/env python3
"""End-to-end check: runs programs compiled by the self-hosted compiler and by the reference.

For every program in PROGRAMS (a runnable case of tests/cases):
* ours:      SELF_MEMEASM < case.memeasm > ours.S, then `X86_CC -static -o ours ours.S [driver.c]`;
* reference: `REF_MEMEASM -o ref case.memeasm`, or for a program with a C driver (no main of
             its own) `REF_MEMEASM -O -o ref.o case.memeasm` and `X86_CC -static -o ref driver.c ref.o`;
then both executables run (x86_64 binaries run directly through qemu binfmt) with the same
arguments and stdin, and their stdout and exit status must be identical.

Environment: REF_MEMEASM (reference), SELF_MEMEASM (default ./memeasm-self), X86_CC (default
x86_64-linux-gnu-gcc), PROGRAMS_OUT (work directory, default $TEST_OUT/programs, TEST_OUT
defaulting to tests/out).

Usage: tests/run_programs.py [-v] [-k] [-l] [name-substring ...]
  -v  show both outputs of every failing run
  -k  keep going quietly (only print failures and the summary)
  -l  list the programs and exit
"""
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "tests", "cases")
OUT = os.environ.get(
    "PROGRAMS_OUT", os.path.join(os.environ.get("TEST_OUT", os.path.join(ROOT, "tests", "out")), "programs")
)
REF = os.environ.get(
    "REF_MEMEASM",
    "/tmp/claude-501/-home-janezrotman-guest-work-MemeAssembly/8b9b7f13-f8fa-429d-86c2-5ec5be99085e/scratchpad/ref-memeasm",
)
SELF = os.environ.get("SELF_MEMEASM", os.path.join(ROOT, "memeasm-self"))
X86_CC = os.environ.get("X86_CC", "x86_64-linux-gnu-gcc")
TIMEOUT = 20

ROT13_DRIVER = r"""
#include <stdio.h>
extern void rot13(char *str);
int main(void) {
    char str[] = "Nu, V frr lbh'er n zna bs phygher nf jryy. ABCXYZ abcxyz 0123 [`{@";
    printf("%s\n", str);
    rot13(str);
    printf("%s\n", str);
    return 0;
}
"""

TOUPPER_DRIVER = r"""
#include <stdio.h>
extern void toupper_str(char *str);
int main(void) {
    char str[] = "The qu1ck BR0wN FoX juMpZ ov3r ThE l4zY dog. Hel1, Y3aH! `az{";
    printf("%s\n", str);
    toupper_str(str);
    printf("%s\n", str);
    return 0;
}
"""

STALINSORT_DRIVER = r"""
#include <stdio.h>
#include <stddef.h>
extern void stalinSort(int array[], size_t *arraySize);
int main(void) {
    int array[] = {1, 5, 2, 8, 9, 3, 4, 12, 14, 69, 420, 0, -5, 421};
    size_t size = sizeof array / sizeof array[0];
    stalinSort(array, &size);
    for (size_t i = 0; i < size; i++) printf("%d,", array[i]);
    printf("\n");
    return 0;
}
"""

BF_HELLO = (
    "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
)

# name: list of runs; a run is a dict with optional "stdin" (bytes) and "args" (list of str).
# "driver": C source of a main that calls the program's function (for cases without main).
PROGRAMS = {
    "ok_example_HelloWorld": {"runs": [{}]},
    "example_hello_world": {"runs": [{}]},
    "ok_example_alphabet": {"runs": [{}]},
    "ok_example_free_real_estate": {"runs": [{}]},
    "ok_example_the_link": {"runs": [{}]},
    "ok_example_is_nice": {"runs": [{"stdin": b"69\n"}, {"stdin": b"420\n"}, {"stdin": b"42\n"}]},
    "ok_example_reverse_string": {"runs": [{"stdin": b"Hello, reversed world!\n"}, {"stdin": b"\n"}]},
    "ok_example_brainfuck": {"runs": [{"args": [BF_HELLO]}, {"args": [",[.,]"], "stdin": b"echo\n"}]},
    "ok_example_rot13": {"runs": [{}], "driver": ROT13_DRIVER},
    "ok_example_toupper": {"runs": [{}], "driver": TOUPPER_DRIVER},
    "ok_example_stalinsort": {"runs": [{}], "driver": STALINSORT_DRIVER},
    "ok_prog_fizzbuzz": {"runs": [{}]},
    "ok_prog_fibonacci": {"runs": [{}]},
    "ok_prog_factorial_recursive": {"runs": [{}]},
    "ok_prog_power_and_bits": {"runs": [{}]},
    "ok_prog_bubble_sort": {"runs": [{}]},
    "ok_prog_echo_upper": {"runs": [{"stdin": b"Hello, World! abc xyz {|}\n\x00 mid-NUL\n"}, {"stdin": b""}]},
    "ok_prog_stack_and_chars": {"runs": [{}]},
    "ok_prog_exit_code": {"runs": [{}]},
    "ok_prog_syscall_exit": {"runs": [{}]},
    "ok_prog_memory_string": {"runs": [{}]},
    "ok_martyrdom_main_code_after_def": {"runs": [{}]},
    "ok_martyrdom_main_only_return": {"runs": [{}]},
    "ok_martyrdom_main_not_first": {"runs": [{}]},
    "ok_confused_stonks_or_draw_25": {"runs": [{}]},
    "ok_lex_crlf": {"runs": [{}]},
    "ok_or_draw_25": {"runs": [{}]},
}


def run(cmd, **kwargs):
    return subprocess.run(cmd, capture_output=True, **kwargs)


def build(name, spec):
    """Builds both executables; returns (ours, ref) paths or raises RuntimeError."""
    src = os.path.join(CASES, name + ".memeasm")
    base = os.path.join(OUT, name)
    with open(src, "rb") as f:
        data = f.read()
    driver = spec.get("driver")
    driver_c = None
    if driver:
        driver_c = base + ".driver.c"
        with open(driver_c, "w") as f:
            f.write(driver)

    # ours
    try:
        ours = run([SELF], input=data, timeout=60)
    except subprocess.TimeoutExpired:
        raise RuntimeError("our compiler timed out")
    with open(base + ".ours.S", "wb") as f:
        f.write(ours.stdout)
    if ours.returncode != 0:
        raise RuntimeError(f"our compiler exited {ours.returncode}: {ours.stderr.decode(errors='replace').strip()}")
    cc = run([X86_CC, "-static", "-o", base + ".ours", base + ".ours.S"] + ([driver_c] if driver_c else []))
    if cc.returncode != 0:
        raise RuntimeError("gcc rejects our output:\n" + cc.stderr.decode(errors="replace"))

    # reference
    if driver_c:
        r = run([REF, "-O", "-o", base + ".ref.o", src])
        if r.returncode == 0:
            r = run([X86_CC, "-static", "-o", base + ".ref", driver_c, base + ".ref.o"])
    else:
        r = run([REF, "-o", base + ".ref", src])
    if r.returncode != 0:
        raise RuntimeError("the reference build failed:\n" + r.stdout.decode(errors="replace") + r.stderr.decode(errors="replace"))
    return base + ".ours", base + ".ref"


def execute(exe, args, stdin):
    try:
        p = run([exe] + args, input=stdin, timeout=TIMEOUT)
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired as e:
        return "timeout", e.stdout or b""


def check(name):
    spec = PROGRAMS[name]
    try:
        ours, ref = build(name, spec)
    except RuntimeError as e:
        return name, False, str(e), []
    details = []
    ok = True
    for i, r in enumerate(spec["runs"]):
        args, stdin = r.get("args", []), r.get("stdin", b"")
        got, want = execute(ours, args, stdin), execute(ref, args, stdin)
        if got != want:
            ok = False
            details.append((i, got, want))
    message = f"{len(spec['runs'])} run(s) identical" if ok else f"{len(details)} of {len(spec['runs'])} run(s) differ"
    return name, ok, message, details


def main():
    args = sys.argv[1:]
    verbose = "-v" in args
    quiet = "-k" in args
    filters = [a for a in args if not a.startswith("-")]
    names = [n for n in PROGRAMS if not filters or any(f in n for f in filters)]
    if "-l" in args:
        print("\n".join(names))
        return
    missing = [n for n in names if not os.path.exists(os.path.join(CASES, n + ".memeasm"))]
    names = [n for n in names if n not in missing]
    os.makedirs(OUT, exist_ok=True)

    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as pool:
        results = list(pool.map(check, names))

    failed = 0
    for n in missing:
        print(f"SKIP {n}: no such case")
    for name, ok, message, details in results:
        if not ok:
            failed += 1
        if not ok or not quiet:
            print(f"{'PASS' if ok else 'FAIL'} {name}: {message}")
        if verbose:
            for i, (status, out), (ref_status, ref_out) in details:
                print(f"  run {i}: ours exited {status}, reference exited {ref_status}")
                print(f"    ours:      {out[:400]!r}")
                print(f"    reference: {ref_out[:400]!r}")
    print(f"\n{len(results) - failed}/{len(results)} programs passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
