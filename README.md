# MemeAssembly, self-hosted

A [MemeAssembly](https://github.com/kammt/MemeAssembly) compiler written in MemeAssembly.

It reads one MemeAssembly program on stdin and writes the x86_64 assembly (GNU as, Intel syntax,
Linux) to stdout: byte-for-byte the same text as the reference compiler's `memeasm -S` output.
It implements every command and quirk of the reference, including:
* editions, `or draw 25`, and `it's free real estate`;
* `confused stonks` and `perfectly balanced as all things should be`, both random;
* martyrdom, which is always on.

```sh
./memeasm-self < program.memeasm > program.S
x86_64-linux-gnu-gcc -static -o program program.S
```

Simplifications compared to the reference:
* one input file, read from stdin, and no command line options (no `-O`, bully mode,
  obfuscation, Breakfiles or debug info);
* it only writes assembly, so there is no implicit `main` or call-target check, the same as `memeasm -S`;
* every error prints just `Compilation error` to stderr and exits with status 1, with nothing written to stdout.

## Building

The compiler is a multi-file MemeAssembly project listed in the `Breakfile`. A first,
reference-built compiler comes from the reference `memeasm` (v1.6, the Rust rewrite):

```sh
make memeasm-self REF_MEMEASM=/path/to/memeasm   # runs `memeasm -o memeasm-self` with the Breakfile
```

## Self-hosting

```sh
make bootstrap
```
1. Concatenates the sources and compiles them with `./memeasm-self` (stage 2).
2. Checks the result is identical to the reference's `-S` output.
3. Links stage 2 and lets it compile itself again (stage 3).
4. Checks that stage 3 equals stage 2, which shows the compiler reproduces itself exactly.

## Tests

* `make test` (`tests/run_tests.py [-v] [-k] [filter…]`): runs the 464 cases in `tests/cases`.
  * `ok_*` cases must give output identical to `memeasm -S`, ignoring the line holding the random confused-stonks label.
  * `err_*` cases must be rejected.
  * Perfectly-balanced cases only need to assemble.
* `tests/run_programs.py`: assembles and runs 27 programs, built by both compilers, and compares their stdout and exit status.
* `tests/gen_cases.py tests/cases`: regenerates the corpus. Edit cases there, not by hand.

Environment: `REF_MEMEASM` (reference compiler), `SELF_MEMEASM` (default `./memeasm-self`),
`TEST_OUT`, `X86_CC` (default `x86_64-linux-gnu-gcc`).

## Layout

| File | Contents |
|---|---|
| `src/main.memeasm` | driver: read stdin → parse → analyse → generate |
| `src/lib.memeasm` | allocation, input, output helpers, text comparison, `libFail`, random numbers |
| `src/parser.memeasm` | lines, comments, command patterns, pointers, function structure |
| `src/analyser.memeasm` | parameter types, operand checks, labels, random choices |
| `src/codegen.memeasm` | assembly text output |

`DESIGN.md` describes the data layout, the calling convention and the MemeAssembly traps worth
knowing before you edit anything.
