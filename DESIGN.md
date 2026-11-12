# Design of the self-hosted MemeAssembly compiler

A MemeAssembly compiler written in MemeAssembly. It reads **one** MemeAssembly program from
stdin and writes x86_64 assembly (GNU as, Intel syntax) to stdout — exactly what the reference
compiler writes for `memeasm -S -o out.S in.memeasm` (Linux target, martyrdom on, no `-O`
flags, no `-g`, compile mode noob).

```
./memeasm-self < program.memeasm > program.S
```

On **any** compile error it writes `Compilation error` to stderr, exits with status 1 and writes
nothing to stdout (`libFail` in `src/lib.memeasm`). All errors are found before the first byte of
output is written.

## The reference

The reference compiler is the Rust implementation in `/home/janezrotman.guest/work/MemeAssembly`
(read it, **never modify it**). It is the specification; when this document and the Rust code
disagree, the Rust code wins. The relevant files:

| What | File |
| --- | --- |
| Commands, patterns, parameter types, opcode order | `src/frontend/commands.rs` |
| Line splitting, pattern matching, "or draw 25", pointers | `src/frontend/parser/file_parser.rs` |
| Function structure checks | `src/frontend/parser/function_parser.rs` |
| Parameter classification, combination and encoding checks | `src/frontend/analyser/parameters.rs` |
| Label checks, confused stonks, perfectly balanced | `src/frontend/analyser/mod.rs`, `helper.rs` |
| Code generation | `src/frontend/translator.rs` |
| Text output (`-S` layout, quoting of call targets) | `src/frontend/asm_text.rs` |
| Registers (`Reg::parse`, names) | `src/backend/emitter/regs.rs` |

Ignore everything about bully/obfuscated mode, macOS, Windows, `-O` levels, debug info,
executables and object files. We only produce the `-S` text (output mode "assembly file"): so
**no** "main function must exist" check and **no** "called function must be defined" check
(the reference only does those for executables).

A built reference binary: `/tmp/claude-501/-home-janezrotman-guest-work-MemeAssembly/8b9b7f13-f8fa-429d-86c2-5ec5be99085e/scratchpad/ref-memeasm`
(set `REF_MEMEASM` to override). Command documentation (incomplete, e.g. `it's free real estate`
and editions are missing): `git -C /home/janezrotman.guest/work/MemeAssembly show origin/gh-pages:commands/<file>.md`.

## Building and testing

```
make            # = $REF_MEMEASM -o memeasm-self   (compiles the files listed in the Breakfile)
make test       # tests/run_tests.py: compares ./memeasm-self with the reference on tests/cases
make bootstrap  # self-hosting check, see below
```

The host is aarch64; x86_64 binaries run transparently through qemu-user (binfmt). An assembler
and linker for the output: `x86_64-linux-gnu-gcc -static -o prog prog.S`.

## Files and ownership

| File | Owner | Entry point | Monke prefix | Edition / function prefix |
| --- | --- | --- | --- | --- |
| `src/main.memeasm` | lead | `main` | `au…` | `main` |
| `src/lib.memeasm` | lead | helpers below | `au…` | `lib` |
| `src/parser.memeasm` | parser | `parseProgram` | `uaa…` | `parse` |
| `src/analyser.memeasm` | analyser | `analyseProgram` | `uau…` | `ana` |
| `src/codegen.memeasm` | codegen | `genProgram` | `uua…` | `gen` |
| test drivers (never in `src/`) | anyone | | `aa…` | `test` |

* Every monke label of a file starts with the file's prefix (`uaa`, `uaau`, `uaauuaua`, …). The
  prefixes are prefix-free, so labels never collide across files.
* Every edition name and every function name of a file starts with the file's edition prefix
  (`parseNextLine`, `(parseIsBlank edition)`).
* A module may split its code into more files `src/<module>_<part>.memeasm` (same prefixes,
  monke labels still unique within the module); add them to the `Breakfile` (it must **not** end
  with a newline).

`main` calls, in order: `libReadInput`, `parseProgram`, `analyseProgram`, `genProgram`.

## Self-hosting restrictions (for the compiler's own source)

`make bootstrap` concatenates all source files into one file and compiles it with our own
compiler. So the compiler source only uses jump markers that are unique across *all* files:

* allowed: monke labels, `who would win? a or b (e edition)` + `e: a wins`, function calls;
* **not allowed** in `src/`: `upgrade`/`fuck go back`, `banana`/`where banana`, `who would win`
  without an edition and `… wins` without one, `corporate needs you to find the difference` /
  `they're the same picture`, `confused stonks`, `perfectly balanced as all things should be`,
  `or draw 25`.
* Characters in `what can I say except` / immediates: write **letters** as themselves, everything
  else as its decimal ASCII code (`48` for `0`, `44` for `,`) or as `\n`, `\s`, `\t`. A digit
  written as itself is a decimal number: `what can I say except 0` prints a NUL byte!

## MemeAssembly cheat sheet (and its traps)

| Meaning | MemeAssembly |
| --- | --- |
| `mov a, b` | `a is brilliant, but I like b` |
| `add a, b` | `a units are ready, with b more well on the way` |
| `sub b, a` | `parry a you filthy casual b` |
| `imul a, b` | `a is getting out of hand, now there are b of them` (64/32 bit only) |
| `b = b / a` (signed, rax/rdx are preserved) | `look at what a needs to mimic a fraction of b` (64 bit) |
| `and a, b` | `bitconneeeeeeect a b` |
| `not a` | `a \s` |
| `xor a, a` | `sneak 100 a` |
| `a += 1` / `a -= 1` | `upvote a` / `downvote a` |
| `shl a, 1` / `shr a, 1` (logical) | `upgrades, people. Upgrades a` / `they had us in the first half, not gonna lie a` |
| `push a` / `pop a` | `stonks a` / `not stonks a` |
| `call f` | `f: whomst has summoned the almighty one` |
| `ret` / `rax = 0; ret` / `rax = 1; ret` | `right back at ya, buckaroo` / `I see this as an absolute win` / `no, I don't think I will` |
| print byte | `what can I say except al` (preserves all registers) |
| `syscall` | `we need air support` (clobbers rcx, r11) |
| `r = mmap(r bytes)`, zeroed | `it's free real estate r` (preserves all other registers) |
| random number | `it's dangerous to go alone, take rax` |
| comment | a line starting with `What the hell happened here?` |
| `[reg]` | `reg do you know de wey` right after the parameter: `al is brilliant, but I like rsi do you know de wey` = `mov al, [rsi]`; `rdi do you know de wey is brilliant, but I like rax` = `mov [rdi], rax` |

Traps (all hit while writing `lib.memeasm`):

1. **A function ends at its last return statement.** Every command after the last
   `right back at ya, buckaroo` / `I see this…` / `no, I don't…` of a function (before the next
   definition) is an error. Structure every function so that its *last line* is a return.
   Earlier returns in the middle are fine.
2. **`who would win? a or b (e edition)` falls through when `a == b`**: it jumps to `e: a wins`
   if a > b (signed), to `e: b wins` if a < b, and otherwise continues with the *next line*. If
   that next line is one of the `wins` labels, the equal case runs into that branch. Put the
   equal case's code (often a `return to monke …`) directly after the comparison.
3. Both labels `e: a wins` and `e: b wins` must exist (in the same file), named by the exact
   parameter text (`e: 0 wins` for `0`). One edition can serve several comparisons with the same
   parameter texts. A label of an edition with the same parameter text may only exist once.
4. A pointer must be a 64 or 32 bit register; only one parameter per command may be a pointer;
   the other operand must be a register (its size is the access size). `who would win` and most
   one-operand commands cannot take a pointer: load the value into a register first.
5. Two-register commands need registers of the same size. An immediate must fit the register
   (`al` takes -128..255). For 64 bit registers, every command except `mov` needs an immediate
   that is a sign-extended 32 bit value: to compare with a big constant, `mov` it into a register.
6. `ah`, `bh`, `ch`, `dh` cannot be combined with registers that need a REX prefix (`r8`–`r15`,
   `sil`, `dil`, `spl`, `bpl`). Avoid the high byte registers.
7. Loading a byte does not clear the rest of the register: `sneak 100 rax` first, then
   `al is brilliant, but I like rsi do you know de wey`.
8. There is no `or`/`xor`/shift-by-n: use `add` for disjoint bits, repeated shifts, `imul`, the
   division.
9. Monke labels consist of `a` and `u` only and need both letters. They are global across files.

## Calling convention

* Arguments in `rdi`, `rsi`, `rdx`, `rcx`; result in `rax`.
* A function may clobber `rax rcx rdx rsi rdi r8 r9 r10 r11`; it must preserve
  `rbx rbp r12 r13 r14` (push/pop them).
* **`r15` always points to the global block** and is never changed.

## The global block (`r15`, 4096 zeroed bytes)

| Offset | Name | Contents |
| --- | --- | --- |
| 0 | INPUT | pointer to the input text (set by `libReadInput`) |
| 8 | INPUT_LEN | length of the input |
| 16 | CMDS | pointer to the command records (set by `parseProgram`) |
| 24 | CMD_COUNT | number of command records |
| 32 | CONFUSED_INDEX | the command index before which the `confused stonks` label goes (set by `analyseProgram`) |
| 40–511 | | reserved for main/lib |
| 512–1023 | | private to the parser |
| 1024–1535 | | private to the analyser |
| 1536–2047 | | private to codegen |
| 2048–4095 | | reserved |

## Command records

One record per *line of interest* (non-blank, non-comment line), in source order, 256 bytes
each, at `CMDS + index * 256`. Allocate room for at least `INPUT_LEN / 2 + 2` records (each line of
interest has at least one character and a line end).

| Offset | Field | Set by | Contents |
| --- | --- | --- | --- |
| 0 | OPCODE | parser | opcode (table below) |
| 8 | LINE | parser | line number, counted from 1 |
| 16 | POINTER | parser | index (0, 1, 2) of the parameter followed by `do you know de wey`, or -1 |
| 24 | TRANSLATE | parser = 1, analyser | 0 if deleted by `perfectly balanced as all things should be` |
| 32–63 | | | reserved |
| 64 | PARAM 0 | | 64 bytes, layout below |
| 128 | PARAM 1 | | |
| 192 | PARAM 2 | | |

Parameter (unused parameters stay all zero):

| Offset | Field | Set by | Contents |
| --- | --- | --- | --- |
| 0 | TEXT | parser | pointer to the parameter text (inside the input buffer) |
| 8 | LEN | parser | length of the text |
| 16 | TYPE | analyser | the `PARAM_*` bit of the classified type (0 before classification) |
| 24 | VALUE | analyser | register: register number (below); decimal: its value; character: its byte value; else 0 |
| 32 | VERBATIM | analyser | characters: 1 if `Param::Char.verbatim` (gas reads the literal as the value), else 0 |
| 40 | ESCAPE | analyser | characters: 0, or 1–10 = index+1 into `ESCAPE_SEQUENCES` (`\n`=1, `\s`=2, `space`=3, `\t`=4, `\f`=5, `\b`=6, `\v`=7, `\"`=8, `\?`=9, `\\`=10) |
| 48–63 | | | reserved |

The text of a character for gas (`Param::Char.text`): for ESCAPE ≠ 0 the escape's literal
(`'\n'`, `' '`, …); for a single byte `c` the three bytes `'c'`; for an ASCII code (`65`) the
source text. In a symbol or an operand a character is written as that text if VERBATIM, else as
its decimal VALUE.

`PARAM_*` types: REG64 = 1, REG32 = 2, REG16 = 4, REG8 = 8, DECIMAL = 16, CHAR = 32,
MONKE_LABEL = 64, FUNC_NAME = 128, COMPARISON_LABEL = 256.

Register numbers (the order of `REGISTERS` in `parameters.rs`; a register's text is its name):

| Numbers | Registers |
| --- | --- |
| 0–15 | rax rbx rcx rdx rdi rsi rsp rbp r8 r9 r10 r11 r12 r13 r14 r15 |
| 16–31 | eax ebx ecx edx edi esi esp ebp r8d … r15d |
| 32–47 | ax bx cx dx di si sp bp r8w … r15w |
| 48–67 | al ah bl bh cl ch dl dh dil sil spl bpl r8b r9b r10b r11b r12b r13b r14b r15b |

Opcodes (the order of `COMMAND_LIST`):

| # | Command | # | Command | # | Command |
| --- | --- | --- | --- | --- | --- |
| 0 | FuncDef | 17 | Imul | 34 | FreeRealEstate |
| 1 | Return | 18 | Divide | 35 | Die |
| 2 | ReturnOne | 19 | Power | 36 | ConfusedStonks |
| 3 | ReturnZero | 20 | Upgrade | 37 | PerfectlyBalanced |
| 4 | Call | 21 | FuckGoBack | 38 | Illegal |
| 5 | Push | 22 | Banana | 39 | OhNo |
| 6 | Pop | 23 | WhereBanana | 40 | Over9000 |
| 7 | And | 24 | Monke | 41 | RefusesToElaborate |
| 8 | Not | 25 | ReturnToMonke | 42 | ShallNotPass |
| 9 | Zero | 26 | WhoWouldWin | 43 | Houston |
| 10 | Mov | 27 | Wins | 44 | Rdrand |
| 11 | Upvote | 28 | WhoWouldWinEdition | 45 | AirSupport |
| 12 | Downvote | 29 | EditionWins | 46 | Trap |
| 13 | Parry | 30 | FindDifference | 47 | OrDraw25 |
| 14 | Add | 31 | SamePicture | 48 | Invalid (never survives parsing) |
| 15 | Shl | 32 | WriteChar | | |
| 16 | Shr | 33 | ReadChar | | |

## Stages

1. **`libReadInput`** (lib): stdin → INPUT, INPUT_LEN.
2. **`parseProgram`** (parser): `file_parser.rs` + `function_parser.rs`. Splits the input into
   lines exactly like `lines_of_interest`/`line_text` (CRLF, the CR quirk, NUL bytes, comments,
   trailing blanks), matches each line against the command patterns in `COMMAND_LIST` order
   exactly like `match_command` (token rules, `{p}`/`({p}`/`{p}:` words, `do you know de wey`,
   `or draw 25`), fills OPCODE, LINE, POINTER, TRANSLATE = 1 and each used parameter's TEXT/LEN,
   sets CMDS and CMD_COUNT. Errors: invalid line, two pointers, no commands at all. Then the
   function structure checks of `function_parser.rs` (commands outside of functions, missing
   return before the next definition, function without return).
3. **`analyseProgram`** (analyser): `parameters.rs` (classify every used parameter in the order
   of the allowed types, not-a-pointer errors, too-large decimals, combination checks,
   encodability checks, push too large) and `analyser/mod.rs` + `helper.rs` (duplicate and
   companion checks for upgrade/banana, monke, who would win (with and without edition), same
   picture; function names defined twice). Then the random choices: CONFUSED_INDEX
   (`libRandomBelow(CMD_COUNT)`), and the `perfectly balanced` deletions (TRANSLATE = 0).
4. **`genProgram`** (codegen): `translator.rs` + `asm_text.rs` for the Linux target with
   martyrdom: the header, `.global` lines, `.data`, `killParent`, the commands with the martyrdom
   prologue after the first command of `main`, the `.LConfusedStonks_0` label (only if a
   translated `confused stonks` exists), the per-command code. Everything is printed with
   `what can I say except` (directly to stdout). The file index is always 0.

## Shared helpers (`src/lib.memeasm`)

| Function | Arguments → result |
| --- | --- |
| `libAllocate` | rdi = size → rax = pointer to zeroed memory |
| `libFail` | prints `Compilation error`, exits with status 1; never returns |
| `libReadInput` | reads stdin into INPUT / INPUT_LEN |
| `libEmitText` | rdi = pointer, rsi = length; prints the bytes |
| `libEmitHex` | rdi = value; prints `0x` + upper-case hex of the unsigned value (Rust `0x{:X}` of `v as u64`) |
| `libEmitDec` | rdi = value ≥ 0; prints it in decimal |
| `libTextEqual` | rdi = text1, rsi = len1, rdx = text2, rcx = len2 → rax = 1 if equal, else 0 |
| `libRandomBelow` | rdi = n > 0 → rax = random number in 0..n-1 |
