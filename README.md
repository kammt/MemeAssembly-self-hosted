<p align="center">
 <img src="https://raw.githubusercontent.com/kammt/MemeAssembly/main/images/logo.png">
 <p align="center">or MemeAssembly-in-MemeAssembly, is the long-awaited answer to a question nobody dared to ask.</p>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/made%20with-MemeAssembly-blue" alt="Made with MemeAssembly Badge">
  <img src="https://img.shields.io/badge/self--hosted-stonks-brightgreen" alt="Self-hosted: stonks">
  <img src="https://img.shields.io/badge/readability-not%20stonks-red" alt="Readability: not stonks">
</p>

## What is this?
Every serious programming language eventually compiles itself. C did it. Rust did it. Go did it. \
For years, MemeAssembly was held back by a humiliating dependency on a compiler written in a *real* programming language.
No more. This is a MemeAssembly compiler, written in MemeAssembly, that compiles MemeAssembly. Including itself. \
The tech industry can finally move on.

It reads one MemeAssembly program on stdin and writes x86_64 assembly (GNU as, Intel syntax, Linux) to stdout,
byte for byte the same as the reference compiler's `memeasm -S`. Yes, byte for byte. We checked. 464 times.

## What are the perks of using it?
- **Execution Time: <span style="color:#ff5050">Not Stonks</span>** \
    Compiling itself takes about 0.2 seconds, which makes it roughly 12 times slower than the reference compiler.
    Admittedly, it runs under qemu on our machine. Admittedly, we don't care. Blazingly fast!
- **Fun-Factor: <span style="color:orange">Stonks</span>** \
    5643 lines of memes, 567 `whomst has summoned the almighty one`s, 693 monkes and comparisons,
    and 880 `What the hell happened here?` comments. That last number is not a joke, it is a cry for help.
- **Complexity: <span style="color:#ff5050">Not Stonks</span>** \
    The whole compiler gets by without `upgrade`, `fuck go back`, `banana` or `they're the same picture`.
    Not because we're purists, but because each of those may only appear once per file, and all five source files have to fit into one.
    Every loop is a `monke` and every `if` is a `who would win?` with an edition. You're welcome.
- **Error messages: <span style="color:#ff5050">Not Stonks</span>** \
    Whatever you did wrong, the answer is `Compilation error` and exit code 1. Fancy error messages are a crutch for the weak.
    You know what you did.

## So it is basically the reference compiler?
I'd just like to interject for a moment. What you're referring to as the MemeAssembly compiler is in fact Rust/MemeAssembly,
or as I've recently taken to calling it, Rust plus MemeAssembly. MemeAssembly is not a compiler unto itself, but rather a meme
made useful by a fully functioning Rust toolchain, cargo and 200 megabytes of `target/` directory. This compiler has none of that.
It has `rax is brilliant, but I like 0`, and it is *enough*.

That said, someone has to compile the first copy. Bootstrapping requires the reference compiler exactly once,
after which you can delete it, uninstall Rust, and tell everyone at parties that your toolchain is made of memes.

## Who is it for?
### ...Compiler Engineers :wrench:
Tired of LLVM's "readable" intermediate representation? Our parser stores command patterns as 8-byte immediates with
the text in a comment above them. Our code generator prints the header starting with
`rdi is brilliant, but I like 7308890601425144355`, which is obviously `#\n# Gene`, eight characters at a time.
This is what peak performance looks like.

### ...Security Auditors :lock:
Trusting trust is hard. Reading 5643 lines of MemeAssembly to make sure there is no backdoor in the compiler is harder.
Good luck.

### ...Your Manager :necktie:
"Is the compiler self-hosted?" Yes. "Does it have tests?" 464 of them, plus 27 programs that are run end to end.
"What does it do?" Please stop asking questions.

## Things it intentionally doesn't do
Restraint is a virtue. Compared to the reference compiler:
* **One input file, read from stdin, no command line options.** No `-O-1` through `-O-s`, no bully mode, no obfuscation,
  no debug info, no Breakfile support. Your code is already deoptimised enough by the act of being written in MemeAssembly.
* **Assembly output only**, as with `memeasm -S`. Linking is gcc's problem. Consequently there is no check for a `main` function
  or for called functions existing either, again exactly like `memeasm -S`.
* **Martyrdom is always on.** You don't get to turn it off. Nobody asked you.
* **Programs larger than 16,711,680 bytes (16 MiB minus 64 KiB) are rejected** with the usual `Compilation error`.
  The input buffer is allocated once, at a size we consider generous, and it is not going to grow for you.
  The reference compiles larger files without complaint, so yes, this is the one place we know of where we are not byte for byte the same.
  If your MemeAssembly program is over 16 megabytes, the compiler is not your biggest problem.

Every command is supported, though. All of them. Even `perfectly balanced as all things should be`, which deletes random lines of your program,
and `confused stonks`, which jumps to a random one. Both are random, which is the only reason the tests don't compare them byte for byte.

## Getting started
### Building
The compiler is a multi-file MemeAssembly project listed in the `Breakfile`. The very first copy has to be built by the
reference `memeasm` (v2.0, the Rust rewrite). We are not proud of it either. By default it is whatever `memeasm` is on your `PATH`.

```sh
make memeasm-self                                # runs `memeasm -o memeasm-self`, which reads the Breakfile
make memeasm-self REF_MEMEASM=/path/to/memeasm   # if your reference lives somewhere less respectable
```

### Usage
```sh
./memeasm-self < program.memeasm > program.S
x86_64-linux-gnu-gcc -static -o program program.S
```

### Achieving enlightenment (self-hosting)
```sh
make bootstrap
```
1. Concatenates all sources into one file and compiles them with `./memeasm-self` (stage 2).
2. Checks that the result is identical to the reference's `-S` output.
3. Links stage 2 and lets it compile itself again (stage 3).
4. Checks that stage 3 equals stage 2. The compiler now reproduces itself exactly, like a meme should.

## Tests
Because "it compiles, ship it" was deemed insufficiently rigorous:
* `make test` (`tests/run_tests.py [-v] [-k] [filter…]`): runs the 464 cases in `tests/cases`.
  * `ok_*` cases must give output identical to `memeasm -S`, ignoring the line holding the random confused-stonks label.
  * `err_*` cases must be rejected. Rejection is the one thing this compiler does with real passion.
  * Perfectly-balanced cases only need to assemble, since Thanos doesn't take requests.
* `tests/run_programs.py`: assembles and runs 27 programs, built by both compilers, and compares their stdout and exit status.
* `tests/gen_cases.py tests/cases`: regenerates the corpus. Edit cases there, not by hand.
  It copies the reference's examples from `MEMEASM_EXAMPLES` (default: `../MemeAssembly/examples`, next to this repository).

Environment: `REF_MEMEASM` (reference compiler, default `memeasm` from `PATH`), `SELF_MEMEASM` (default `./memeasm-self`),
`TEST_OUT`, `X86_CC` (default `x86_64-linux-gnu-gcc`).

## Layout
| File | Contents |
|---|---|
| `src/main.memeasm` | driver: read stdin → parse → analyse → generate. 17 lines, the only readable file |
| `src/lib.memeasm` | allocation, input, output helpers, text comparison, `libFail`, random numbers |
| `src/parser.memeasm` | lines, comments, command patterns, pointers, function structure |
| `src/analyser.memeasm` | parameter types, operand checks, labels, random choices |
| `src/codegen.memeasm` | assembly text output |

`DESIGN.md` describes the data layout, the calling convention and the MemeAssembly traps worth knowing before you
edit anything. Read it. The traps are real, and each of them has cost someone an infinite loop.

## Badge of honor
Whoever dares to read this compiler's source code shall be rewarded with this badge of honor:\
![Made with MemeAssembly Badge](https://img.shields.io/badge/made%20with-MemeAssembly-blue)\
Whoever understands it gets nothing, because nobody has managed it yet.

## Contributing
Same spirit as [MemeAssembly](https://github.com/kammt/MemeAssembly): contributions are welcome, especially ones that make
it even more cursed. Pull requests must keep `make test` and `make bootstrap` green. The compiler has to be able to read your code,
which is more than can be said for the reviewers.

## License
MIT, see [LICENSE](LICENSE). Use it, fork it, ship it to production. Especially that last one; we'd love to hear how it went.
