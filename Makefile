# The build itself is the Breakfile: `memeasm -o memeasm-self` without input files compiles the
# files listed there. This Makefile only wraps it and the tests.
REF_MEMEASM ?= /tmp/claude-501/-home-janezrotman-guest-work-MemeAssembly/8b9b7f13-f8fa-429d-86c2-5ec5be99085e/scratchpad/ref-memeasm
X86_CC ?= x86_64-linux-gnu-gcc
SOURCES := $(shell sed 's/^the secret ingredient is //' Breakfile)

.PHONY: all test bootstrap clean

all: memeasm-self

memeasm-self: Breakfile $(SOURCES)
	$(REF_MEMEASM) -o memeasm-self

test: memeasm-self
	REF_MEMEASM=$(REF_MEMEASM) python3 tests/run_tests.py

# Self-hosting: the compiler compiles its own source (all files concatenated into one, since it
# reads a single file from stdin). stage2 is assembled from our own output and must produce the
# same output again (a fixed point), which must also equal the reference compiler's output.
bootstrap: memeasm-self
	mkdir -p build
	cat $(SOURCES) > build/self.memeasm
	./memeasm-self < build/self.memeasm > build/stage2.S
	$(REF_MEMEASM) -S -o build/ref.S build/self.memeasm
	cmp build/ref.S build/stage2.S
	$(X86_CC) -static -o build/stage2 build/stage2.S
	./build/stage2 < build/self.memeasm > build/stage3.S
	cmp build/stage2.S build/stage3.S
	@echo "bootstrap OK: the self-hosted compiler reproduces itself"

clean:
	rm -rf memeasm-self build tests/out
