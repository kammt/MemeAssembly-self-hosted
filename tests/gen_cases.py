#!/usr/bin/env python3
"""Generates tests/cases/{ok,err}_*.memeasm of the self-hosted MemeAssembly compiler.

Usage: tests/gen_cases.py tests/cases   (overwrites the generated cases; edit this file, not the cases)
"""
import os
import sys

DEF = "I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun "
RET = "right back at ya, buckaroo"
WIN = "I see this as an absolute win"
LOSE = "no, I don't think I will"
PTR = " do you know de wey"

R64 = "rax rbx rcx rdx rdi rsi rsp rbp r8 r9 r10 r11 r12 r13 r14 r15".split()
R32 = "eax ebx ecx edx edi esi esp ebp r8d r9d r10d r11d r12d r13d r14d r15d".split()
R16 = "ax bx cx dx di si sp bp r8w r9w r10w r11w r12w r13w r14w r15w".split()
R8 = "al ah bl bh cl ch dl dh dil sil spl bpl r8b r9b r10b r11b r12b r13b r14b r15b".split()
R8_LOW = [r for r in R8 if not r.endswith("h")]
SIZES = {"r64": R64, "r32": R32, "r16": R16, "r8": R8}

CASES = {}


def case(name, data):
    assert name not in CASES, name
    if isinstance(data, str):
        try:
            data = data.encode("latin-1")
        except UnicodeEncodeError:
            data = data.encode("utf-8")
    CASES[name] = data


def lines(*ls):
    return "\n".join(ls) + "\n"


def fn(name, body, ret=RET, indent="    "):
    return [DEF + name] + [indent + l if l else "" for l in body] + [indent + ret]


def main(*body, ret=WIN):
    return lines(*fn("main", list(body), ret))


def func(*body, name="f", ret=RET):
    """A function that is not main (no martyrdom prologue)."""
    return lines(*fn(name, list(body), ret))


def pairs(regs):
    """Each register with the next one (same size)."""
    return [(a, regs[(i + 1) % len(regs)]) for i, a in enumerate(regs)]


# ---------------------------------------------------------------------------------------------
# functions and returns
case("ok_func_three_returns", lines(
    *fn("f", ["upvote rax"], RET), "",
    *fn("g", ["upvote rbx"], WIN), "",
    *fn("h", ["upvote rcx"], LOSE)))
case("ok_func_only_return", lines(DEF + "f", RET))
case("ok_func_returns_in_middle", lines(
    DEF + "f", "upvote rax", RET, "downvote rax", WIN, "sneak 100 rax", LOSE, "upvote rbx", RET))
case("ok_func_names", lines(
    *fn("_f", [], RET), *fn("a.b", [], RET), *fn("$x", [], RET), *fn("f$1", [], RET),
    *fn("F", [], RET), *fn("CamelCase_9", [], RET), *fn(".", [], RET), *fn("$", [], RET),
    *fn("_", [], RET), *fn("x.y.z$", [], RET)))
case("ok_func_names_gas_would_misread", lines(
    *fn("rax", [], RET), *fn("byte", [], RET), *fn("RAX", [], RET), *fn("Byte", [], RET),
    *fn("xmm0", [], RET), *fn("r16", [], RET), *fn("r31b", [], RET), *fn("and", [], RET),
    *fn("flat", [], RET), *fn("near", [], RET), *fn("st", [], RET), *fn("k7", [], RET),
    *fn("cr15", [], RET), *fn("mm7", [], RET), *fn("ah", [], RET), *fn("fs", [], RET),
    *fn("rip", [], RET), *fn("offset", [], RET), *fn("ZMMWORD", [], RET), *fn("dr0", [], RET),
    *fn("tmm7", [], RET), *fn("ymm31", [], RET), *fn("r8d", [], RET), *fn("eq", [], RET)))
case("ok_call_quoted_targets", func(
    "rax: whomst has summoned the almighty one",
    "byte: whomst has summoned the almighty one",
    "RAX: whomst has summoned the almighty one",
    "$: whomst has summoned the almighty one",
    ".: whomst has summoned the almighty one",
    "xmm0: whomst has summoned the almighty one",
    "xmm15: whomst has summoned the almighty one",
    "xmm31: whomst has summoned the almighty one",
    "r16: whomst has summoned the almighty one",
    "r31w: whomst has summoned the almighty one",
    "r20d: whomst has summoned the almighty one",
    "and: whomst has summoned the almighty one",
    "NOT: whomst has summoned the almighty one",
    "flat: whomst has summoned the almighty one",
    "near: whomst has summoned the almighty one",
    "short: whomst has summoned the almighty one",
    "st: whomst has summoned the almighty one",
    "k0: whomst has summoned the almighty one",
    "cr8: whomst has summoned the almighty one",
    "dr15: whomst has summoned the almighty one",
    "mm0: whomst has summoned the almighty one",
    "tmm0: whomst has summoned the almighty one",
    "ah: whomst has summoned the almighty one",
    "spl: whomst has summoned the almighty one",
    "eip: whomst has summoned the almighty one",
    "gs: whomst has summoned the almighty one",
    "mod: whomst has summoned the almighty one",
    "xmmword: whomst has summoned the almighty one",
    "tbyte: whomst has summoned the almighty one",
    "fword: whomst has summoned the almighty one"))
case("ok_call_unquoted_targets", func(
    "f: whomst has summoned the almighty one",
    "main: whomst has summoned the almighty one",
    "r32: whomst has summoned the almighty one",
    "r08: whomst has summoned the almighty one",
    "r: whomst has summoned the almighty one",
    "xmm32: whomst has summoned the almighty one",
    "xmm01: whomst has summoned the almighty one",
    "rax1: whomst has summoned the almighty one",
    "st0: whomst has summoned the almighty one",
    "_and: whomst has summoned the almighty one",
    "bytes: whomst has summoned the almighty one",
    "foo$bar: whomst has summoned the almighty one",
    "k8: whomst has summoned the almighty one",
    "cr16: whomst has summoned the almighty one",
    "mm8: whomst has summoned the almighty one",
    "r15x: whomst has summoned the almighty one",
    "a.b: whomst has summoned the almighty one",
    "$x: whomst has summoned the almighty one",
    "r15b.x: whomst has summoned the almighty one",
    "undefinedFunction: whomst has summoned the almighty one"))
case("ok_call_defined_function", lines(
    *fn("helper", ["upvote rax"], RET), "",
    *fn("main", ["helper: whomst has summoned the almighty one",
                 "rax: whomst has summoned the almighty one"], WIN), "",
    *fn("rax", [], RET)))
case("err_func_name_starts_with_digit", lines(DEF + "1f", RET))
case("err_func_name_dash", lines(DEF + "f-g", RET))
case("err_func_name_parens", lines(DEF + "main()", RET))
case("err_func_name_umlaut", lines(DEF + "f\xe4", RET))
case("err_call_name_starts_with_digit", func("9lives: whomst has summoned the almighty one"))
case("err_call_without_colon", func("f whomst has summoned the almighty one"))
case("err_func_def_pointer", lines(DEF + "main" + PTR, WIN))
case("err_call_pointer", func("f:" + PTR + " whomst has summoned the almighty one"))
case("err_call_pointer_before_colon", func("f" + PTR + ": whomst has summoned the almighty one"))
case("err_func_defined_twice", lines(*fn("f", [], RET), *fn("g", [], RET), *fn("f", [], WIN)))
case("err_main_defined_twice", lines(*fn("main", [], WIN), *fn("main", [], WIN)))
case("err_func_without_return", lines(DEF + "f", "upvote rax"))
case("err_func_def_only", lines(DEF + "f"))
case("err_missing_return_before_next_def", lines(DEF + "f", "upvote rax", *fn("g", [], RET)))
case("err_two_defs_in_a_row", lines(DEF + "f", *fn("g", [], RET)))
case("err_command_before_first_function", lines("upvote rax", *fn("f", [], RET)))
case("err_command_after_last_return", lines(*fn("f", [], RET), "upvote rax"))
case("err_command_between_functions", lines(*fn("f", [], RET), "upvote rax", *fn("g", [], RET)))
case("err_only_commands", lines("upvote rax", RET))
case("err_return_outside_function", lines(RET, *fn("f", [], RET)))
case("err_def_too_few_funs", lines("I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun main", WIN))
case("err_def_too_many_funs", lines("I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun, fun main", WIN))
case("err_def_without_name", lines(DEF.rstrip(), WIN))
case("err_def_two_names", lines(DEF + "main extra", WIN))
case("err_return_with_parameter", lines(DEF + "f", RET + " rax"))

# martyrdom: the prologue after the first command of main
case("ok_martyrdom_main_only_return", lines(DEF + "main", WIN))
case("ok_martyrdom_main_code_after_def", main("upvote rax", "downvote rax"))
case("ok_martyrdom_main_not_first", lines(
    *fn("f", ["upvote rax"], RET), *fn("main", ["f: whomst has summoned the almighty one"], WIN),
    *fn("g", ["upvote rbx"], RET)))
case("ok_martyrdom_main_last", lines(*fn("f", [], RET), *fn("g", [], LOSE), *fn("main", ["upvote rax"], WIN)))
case("ok_martyrdom_no_main", lines(*fn("f", ["upvote rax"], RET), *fn("g", ["upvote rbx"], RET)))
case("ok_martyrdom_main_capitalised", lines(*fn("Main", ["upvote rax"], WIN), *fn("MAIN", [], RET), *fn("main_", [], RET), *fn("_main", [], RET)))
case("ok_martyrdom_main_label_first", main("monke au", "return to monke au"))
case("ok_martyrdom_main_returns_twice", lines(DEF + "main", RET, "upvote rax", WIN))

# ---------------------------------------------------------------------------------------------
# stack
case("ok_cmd_push_r64", func(*["stonks " + r for r in R64]))
case("ok_cmd_push_imm", func(
    "stonks 0", "stonks 1", "stonks -1", "stonks +5", "stonks 2147483647", "stonks -2147483648",
    "stonks 007", "stonks -0", "stonks a", "stonks Z", "stonks \\n", "stonks space", "stonks \\s",
    "stonks \\v", "stonks \\\\", "stonks \\", "stonks !", "stonks '", "stonks \"", "stonks 69", "stonks 420"))
case("ok_cmd_push_pointer", func("stonks rax" + PTR, "stonks r15" + PTR, "stonks rsp" + PTR))
case("err_push_pointer_r32", func("stonks eax" + PTR))
case("err_push_too_large", func("stonks 2147483648"))
case("err_push_too_small", func("stonks -2147483649"))
case("err_push_u32_max", func("stonks 4294967295"))
case("err_push_i64_max", func("stonks 9223372036854775807"))
case("err_push_beyond_i64", func("stonks 9223372036854775808"))
case("err_push_r32", func("stonks eax"))
case("err_push_r16", func("stonks ax"))
case("err_push_r8", func("stonks al"))
case("err_push_pointer_r16", func("stonks ax" + PTR))
case("err_push_decimal_pointer", func("stonks 5" + PTR))
case("err_push_char_pointer", func("stonks a" + PTR))
case("ok_cmd_pop_r64", func(*["not stonks " + r for r in R64]))
case("ok_cmd_pop_pointer", func("not stonks rax" + PTR, "not stonks r12" + PTR))
case("err_pop_pointer_r32", func("not stonks r12d" + PTR))
case("err_pop_r32", func("not stonks eax"))
case("err_pop_decimal", func("not stonks 5"))
case("err_pop_char", func("not stonks a"))
case("err_pop_pointer_r8", func("not stonks al" + PTR))

# ---------------------------------------------------------------------------------------------
# two-operand commands: and, mov, add, parry, find the difference, who would win
TWO = {
    "and": "bitconneeeeeeect {0} {1}",
    "mov": "{0} is brilliant, but I like {1}",
    "add": "{0} units are ready, with {1} more well on the way",
}
for cmd, pat in TWO.items():
    for size, regs in SIZES.items():
        body = [pat.format(a, b) for a, b in pairs(regs if size != "r8" else R8_LOW)]
        if size == "r8":
            body += [pat.format(a, b) for a, b in [("ah", "al"), ("al", "ah"), ("bh", "ch"), ("dh", "dl"), ("ah", "ah")]]
        body += [pat.format(r, r) for r in regs[:3]]
        case(f"ok_cmd_{cmd}_{size}_reg", func(*body))
    case(f"ok_cmd_{cmd}_imm", func(
        pat.format("rax", "5"), pat.format("eax", "-5"), pat.format("ax", "+5"), pat.format("al", "255"),
        pat.format("ah", "-128"), pat.format("r15", "a"), pat.format("r8d", "\\n"), pat.format("r9w", "space"),
        pat.format("sil", "\\v"), pat.format("r10", "\\\\"), pat.format("r11", "\\"), pat.format("ebx", "0"),
        pat.format("rcx", "-1"), pat.format("ecx", "4294967295"), pat.format("cx", "65535"),
        pat.format("dx", "-32768"), pat.format("dl", "'"), pat.format("bl", "\""), pat.format("bh", "\\t"),
        pat.format("rdx", "2147483647"), pat.format("rdi", "-2147483648"), pat.format("edi", "-2147483648"),
        pat.format("spl", "\\b"), pat.format("bpl", "\\f"), pat.format("r12b", "\\?"), pat.format("r13b", "\\\""),
        pat.format("r14", "007"), pat.format("r14", "-0"), pat.format("r14", "-"), pat.format("r14", "+")))
    case(f"ok_cmd_{cmd}_pointer", func(
        pat.format("rax" + PTR, "rbx"), pat.format("rax" + PTR, "ebx"), pat.format("rax" + PTR, "bx"),
        pat.format("rax" + PTR, "bl"), pat.format("eax" + PTR, "rbx"), pat.format("r8" + PTR, "r9b"),
        pat.format("rbx", "rax" + PTR), pat.format("bl", "rax" + PTR), pat.format("r10w", "esp" + PTR),
        pat.format("rax" + PTR, "ah"), pat.format("ah", "rbx" + PTR), pat.format("rsp" + PTR, "rsp"),
        pat.format("r15d" + PTR, "r15d")))
    case(f"err_{cmd}_size_mismatch", func(pat.format("rax", "eax")))
    case(f"err_{cmd}_two_pointers", func(pat.format("rax" + PTR, "rbx" + PTR)))
    case(f"err_{cmd}_pointer_with_imm", func(pat.format("rax" + PTR, "5")))
    case(f"err_{cmd}_pointer_r16", func(pat.format("ax" + PTR, "bx")))
    case(f"err_{cmd}_high_byte_rex", func(pat.format("ah", "r8b")))
    case(f"err_{cmd}_imm_destination", func(pat.format("5", "rax")))
    if cmd != "mov":
        case(f"err_{cmd}_64bit_imm_not_sign_extendable", func(pat.format("rax", "2147483648")))

# mov: decimal boundaries per register size
case("ok_mov_boundaries", func(
    "al is brilliant, but I like 255", "al is brilliant, but I like -128", "ah is brilliant, but I like 128",
    "ax is brilliant, but I like 65535", "ax is brilliant, but I like -32768", "ax is brilliant, but I like 256",
    "eax is brilliant, but I like 4294967295", "eax is brilliant, but I like -2147483648",
    "eax is brilliant, but I like 2147483648", "eax is brilliant, but I like 65536",
    "rax is brilliant, but I like 9223372036854775807", "rax is brilliant, but I like -9223372036854775808",
    "rax is brilliant, but I like 2147483648", "rax is brilliant, but I like 4294967296",
    "rax is brilliant, but I like -2147483649", "rax is brilliant, but I like 0000000000000000000000001",
    "r8b is brilliant, but I like -1", "r8w is brilliant, but I like -1", "r8d is brilliant, but I like -1",
    "r8 is brilliant, but I like -1"))
case("err_mov_r8_256", func("al is brilliant, but I like 256"))
case("err_mov_r8_minus_129", func("al is brilliant, but I like -129"))
case("err_mov_r16_65536", func("ax is brilliant, but I like 65536"))
case("err_mov_r16_minus_32769", func("ax is brilliant, but I like -32769"))
case("err_mov_r32_4294967296", func("eax is brilliant, but I like 4294967296"))
case("err_mov_r32_minus_2147483649", func("eax is brilliant, but I like -2147483649"))
case("err_mov_r64_i64_max_plus_1", func("rax is brilliant, but I like 9223372036854775808"))
case("err_mov_r64_i64_min_minus_1", func("rax is brilliant, but I like -9223372036854775809"))
case("err_mov_huge_number", func("rax is brilliant, but I like 99999999999999999999999999"))
case("err_mov_hex_number", func("rax is brilliant, but I like 0x10"))
case("err_mov_double_sign", func("rax is brilliant, but I like --5"))
case("err_mov_plus_minus", func("rax is brilliant, but I like +-5"))
case("err_mov_number_with_letters", func("rax is brilliant, but I like 12x"))
case("err_mov_two_chars", func("rax is brilliant, but I like ab"))
case("err_mov_uppercase_register", func("RAX is brilliant, but I like 5"))
case("err_mov_xmm_register", func("xmm0 is brilliant, but I like xmm1"))
case("err_mov_pointer_r8", func("al" + PTR + " is brilliant, but I like bl"))
case("err_mov_high_byte_rex_pointer_base", func("r8" + PTR + " is brilliant, but I like ah"))
case("err_mov_high_byte_rex_pointer_base32", func("r8d" + PTR + " is brilliant, but I like bh"))
case("err_mov_high_byte_sil", func("ah is brilliant, but I like sil"))
case("err_mov_high_byte_dil_reverse", func("dil is brilliant, but I like ch"))
case("err_mov_high_byte_spl", func("spl is brilliant, but I like dh"))
case("err_mov_high_byte_r15b", func("bh is brilliant, but I like r15b"))
case("ok_mov_high_byte_with_rax_pointer", func("ah is brilliant, but I like rax" + PTR, "rbp" + PTR + " is brilliant, but I like dh", "ah is brilliant, but I like 1", "ah is brilliant, but I like a"))
case("err_and_64bit_imm_minus_2147483649", func("bitconneeeeeeect rax -2147483649"))
case("ok_and_64bit_imm_negative", func("bitconneeeeeeect rax -2147483648", "bitconneeeeeeect rax -16", "bitconneeeeeeect eax 4294967290"))
case("err_add_r8_256", func("al units are ready, with 256 more well on the way"))
case("err_add_r32_too_large", func("eax units are ready, with 4294967296 more well on the way"))

# not, zero, upvote, downvote, shl, shr, over 9000
ONE = {
    "not": "{0} \\s",
    "zero": "sneak 100 {0}",
    "upvote": "upvote {0}",
    "downvote": "downvote {0}",
    "shl": "upgrades, people. Upgrades {0}",
    "shr": "they had us in the first half, not gonna lie {0}",
    "over9000": "it's over 9000 {0}",
}
for cmd, pat in ONE.items():
    for size, regs in SIZES.items():
        case(f"ok_cmd_{cmd}_{size}", func(*[pat.format(r) for r in regs]))
    case(f"err_{cmd}_pointer", func(pat.format("rax" + PTR)))
    case(f"err_{cmd}_decimal", func(pat.format("5")))
    case(f"err_{cmd}_char", func(pat.format("a")))
case("err_not_missing_param", func("\\s"))
case("err_not_space_word", func("rax space"))
case("err_zero_pointer_r32", func("sneak 100 eax" + PTR))
case("err_upvote_pointer_r8", func("upvote al" + PTR))
case("err_over9000_pointer_r32", func("it's over 9000 eax" + PTR))
case("err_upvote_two_params", func("upvote rax rbx"))
case("err_upvote_no_param", func("upvote"))

# parry
case("ok_cmd_parry", func(
    "parry rax you filthy casual rbx", "parry eax you filthy casual r8d", "parry ax you filthy casual r9w",
    "parry ah you filthy casual al", "parry r10b you filthy casual sil", "parry 5 you filthy casual rax",
    "parry -2147483648 you filthy casual rax", "parry 255 you filthy casual al", "parry a you filthy casual al",
    "parry \\n you filthy casual r15", "parry 4294967295 you filthy casual ecx",
    "parry rax" + PTR + " you filthy casual rbx", "parry rbx you filthy casual rax" + PTR,
    "parry ebx" + PTR + " you filthy casual dl", "parry cl you filthy casual r8" + PTR,
    "parry 10000 you filthy casual rsp"))
case("err_parry_64bit_imm", func("parry 2147483648 you filthy casual rax"))
case("err_parry_imm_destination", func("parry rax you filthy casual 5"))
case("err_parry_size_mismatch", func("parry rax you filthy casual eax"))
case("err_parry_pointer_with_imm", func("parry 5 you filthy casual rax" + PTR))
case("err_parry_two_pointers", func("parry rax" + PTR + " you filthy casual rbx" + PTR))
case("err_parry_high_byte_rex", func("parry ah you filthy casual r9b"))
case("err_parry_r8_too_large", func("parry 256 you filthy casual al"))

# imul
case("ok_cmd_imul", func(*(
    [f"{a} is getting out of hand, now there are {b} of them" for a, b in pairs(R64) + pairs(R32)] + [
        "rax is getting out of hand, now there are 5 of them",
        "eax is getting out of hand, now there are -5 of them",
        "r8 is getting out of hand, now there are 2147483647 of them",
        "r8d is getting out of hand, now there are 4294967295 of them",
        "rcx is getting out of hand, now there are a of them",
        "rcx is getting out of hand, now there are \\v of them",
        "rax is getting out of hand, now there are rbx" + PTR + " of them",
        "eax is getting out of hand, now there are rbx" + PTR + " of them",
        "r12 is getting out of hand, now there are r13d" + PTR + " of them",
    ])))
case("err_imul_r16", func("ax is getting out of hand, now there are bx of them"))
case("err_imul_r8", func("al is getting out of hand, now there are 5 of them"))
case("err_imul_size_mismatch", func("rax is getting out of hand, now there are ebx of them"))
case("err_imul_pointer_destination", func("rax" + PTR + " is getting out of hand, now there are rbx of them"))
case("err_imul_64bit_imm", func("rax is getting out of hand, now there are 2147483648 of them"))
case("err_imul_r32_too_large", func("eax is getting out of hand, now there are 4294967296 of them"))

# divide
case("ok_cmd_divide", func(*(
    [f"look at what {a} needs to mimic a fraction of {b}" for a, b in pairs(R64)] + [
        "look at what 10 needs to mimic a fraction of rax",
        "look at what -3 needs to mimic a fraction of rdx",
        "look at what 2147483647 needs to mimic a fraction of rsp",
        "look at what a needs to mimic a fraction of rcx",
        "look at what rax needs to mimic a fraction of rax",
        "look at what rbx needs to mimic a fraction of rax" + PTR,
    ])))
case("err_divide_pointer_r32", func("look at what rbx needs to mimic a fraction of eax" + PTR))
case("err_divide_r32", func("look at what ebx needs to mimic a fraction of eax"))
case("err_divide_imm_dividend", func("look at what rbx needs to mimic a fraction of 5"))
case("err_divide_64bit_imm", func("look at what 2147483648 needs to mimic a fraction of rax"))
case("err_divide_pointer_divisor", func("look at what rbx" + PTR + " needs to mimic a fraction of rax"))
case("err_divide_two_pointers", func("look at what rbx" + PTR + " needs to mimic a fraction of rax" + PTR))

# power
case("ok_cmd_power", func(
    "rax UNLIMITED POWER rbx", "rbx UNLIMITED POWER 3", "rcx UNLIMITED POWER -1", "r15 UNLIMITED POWER rax",
    "rax UNLIMITED POWER rax", "rsp UNLIMITED POWER 2147483647", "rdx UNLIMITED POWER a", "r8 UNLIMITED POWER rsp"))
case("err_power_r32", func("eax UNLIMITED POWER ebx"))
case("err_power_64bit_imm", func("rax UNLIMITED POWER 2147483648"))
case("err_power_pointer_base", func("rax" + PTR + " UNLIMITED POWER rbx"))
case("err_power_pointer_base_imm", func("rax" + PTR + " UNLIMITED POWER 2"))
case("err_power_pointer_exponent", func("rax UNLIMITED POWER rbx" + PTR))
case("err_power_lowercase", func("rax unlimited power rbx"))

# ---------------------------------------------------------------------------------------------
# jump markers
case("ok_upgrade", func("upgrade", "upvote rax", "fuck go back"))
case("ok_upgrade_jump_before_marker", func("fuck go back", "upgrade", "fuck go back", "fuck go back"))
case("ok_upgrade_without_jump", func("upgrade"))
case("ok_banana", func("banana", "upvote rax", "where banana", "where banana"))
case("ok_banana_and_upgrade", func("upgrade", "banana", "where banana", "fuck go back"))
case("ok_markers_in_other_function", lines(*fn("f", ["upgrade", "banana"], RET), *fn("g", ["fuck go back", "where banana"], RET)))
case("err_upgrade_twice", func("upgrade", "upgrade", "fuck go back"))
case("err_upgrade_twice_in_two_functions", lines(*fn("f", ["upgrade"], RET), *fn("g", ["upgrade"], RET)))
case("err_fuck_go_back_without_upgrade", func("fuck go back"))
case("err_banana_twice", func("banana", "banana"))
case("err_where_banana_without_banana", func("where banana", "upgrade"))
case("err_upgrade_with_param", func("upgrade rax"))
case("err_banana_capitalised", func("Banana"))

case("ok_monke", func("monke au", "monke ua", "monke aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaau", "monke uuuuuuuuuuuuuuuuuuua",
                      "return to monke au", "return to monke ua", "return to monke uuuuuuuuuuuuuuuuuuua",
                      "return to monke aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaau"))
case("ok_monke_unused_and_across_functions", lines(*fn("f", ["monke uau", "monke aua"], RET), *fn("g", ["return to monke uau"], RET)))
case("ok_monke_jump_before_marker", func("return to monke uuaa", "upvote rax", "monke uuaa"))
case("err_monke_duplicate", func("monke au", "monke au"))
case("err_monke_duplicate_across_functions", lines(*fn("f", ["monke au"], RET), *fn("g", ["monke au"], RET)))
case("err_monke_undefined", func("return to monke au"))
case("err_monke_only_a", func("monke aa"))
case("err_monke_only_u", func("monke uu"))
case("err_monke_single_letter", func("monke a"))
case("err_monke_uppercase", func("monke AU"))
case("err_monke_other_letter", func("monke aub"))
case("err_monke_digit", func("monke au1"))
case("err_monke_pointer", func("monke au" + PTR))
case("err_return_to_monke_pointer", func("monke au", "return to monke au" + PTR))
case("err_return_to_monke_invalid", func("monke au", "return to monke ab"))
case("err_return_to_monke_other_label", func("monke au", "return to monke aau"))

# who would win (without edition)
case("ok_who_would_win_regs", func("who would win? rax or rbx", "rax wins", "rbx wins",
                                   "who would win? ecx or edx", "ecx wins", "edx wins",
                                   "who would win? si or r8w", "si wins", "r8w wins",
                                   "who would win? ah or bh", "ah wins", "bh wins",
                                   "who would win? r9b or sil", "r9b wins", "sil wins"))
case("ok_who_would_win_same_register", func("who would win? rax or rax", "rax wins"))
case("ok_who_would_win_labels_shared", func("who would win? rax or rbx", "who would win? rbx or rax", "rbx wins", "rax wins",
                                            "who would win? rax or 5", "5 wins"))
case("ok_who_would_win_decimals", func("who would win? rax or 5", "rax wins", "5 wins",
                                       "who would win? rbx or -1", "rbx wins", "-1 wins",
                                       "who would win? al or 255", "al wins", "255 wins",
                                       "who would win? rcx or +7", "+7 wins", "rcx wins",
                                       "who would win? rdx or 007", "007 wins", "rdx wins",
                                       "who would win? rsi or -2147483648", "-2147483648 wins", "rsi wins",
                                       "who would win? rdi or 0", "0 wins", "rdi wins",
                                       "who would win? ecx or 4294967295", "4294967295 wins", "ecx wins"))
case("ok_who_would_win_same_value_different_text", func("who would win? rax or 5", "rax wins", "5 wins",
                                                        "who would win? rbx or 05", "rbx wins", "05 wins",
                                                        "who would win? rcx or +5", "rcx wins", "+5 wins"))
case("ok_who_would_win_chars", func("who would win? al or a", "al wins", "a wins",
                                    "who would win? bl or \\n", "bl wins", "\\n wins",
                                    "who would win? cl or \\v", "cl wins", "\\v wins",
                                    "who would win? dl or \\\\", "dl wins", "\\\\ wins",
                                    "who would win? sil or \\", "sil wins", "\\ wins",
                                    "who would win? dil or space", "dil wins", "space wins",
                                    "who would win? r8b or \\t", "r8b wins", "\\t wins",
                                    "who would win? r9b or \\\"", "r9b wins", "\\\" wins",
                                    "who would win? r10b or \\?", "r10b wins", "\\? wins",
                                    "who would win? r11b or \\f", "r11b wins", "\\f wins",
                                    "who would win? r12b or \\b", "r12b wins", "\\b wins",
                                    "who would win? r13b or '", "r13b wins", "' wins",
                                    "who would win? r14b or -", "r14b wins", "- wins",
                                    "who would win? r15b or :", "r15b wins", ": wins",
                                    "who would win? rax or Z", "rax wins", "Z wins"))
case("ok_who_would_win_space_aliases", func("who would win? al or \\s", "al wins", "space wins"))
case("err_who_would_win_space_duplicate", func("who would win? al or \\s", "al wins", "space wins", "\\s wins"))
case("err_who_would_win_missing_second", func("who would win? rax or rbx", "rax wins"))
case("err_who_would_win_missing_first", func("who would win? rax or rbx", "rbx wins"))
case("err_who_would_win_missing_both", func("who would win? rax or rbx"))
case("err_who_would_win_label_text_differs", func("who would win? rax or 5", "rax wins", "05 wins"))
case("err_wins_duplicate", func("who would win? rax or rbx", "rax wins", "rbx wins", "rax wins"))
case("err_wins_duplicate_unused", func("rax wins", "rax wins"))
case("ok_wins_unused", func("rax wins", "5 wins", "a wins"))
case("err_who_would_win_imm_first", func("who would win? 5 or rax", "5 wins", "rax wins"))
case("err_who_would_win_size_mismatch", func("who would win? rax or ebx", "rax wins", "ebx wins"))
case("err_who_would_win_pointer", func("who would win? rax" + PTR + " or rbx", "rax wins", "rbx wins"))
case("err_who_would_win_pointer_second", func("who would win? rax or rbx" + PTR, "rax wins", "rbx wins"))
case("err_who_would_win_64bit_imm", func("who would win? rax or 2147483648", "rax wins", "2147483648 wins"))
case("err_who_would_win_r8_too_large", func("who would win? al or 256", "al wins", "256 wins"))
case("err_who_would_win_high_byte_rex", func("who would win? ah or r8b", "ah wins", "r8b wins"))
case("err_wins_pointer", func("who would win? rax or rbx", "rax" + PTR + " wins", "rbx wins"))
case("err_wins_invalid", func("xyz wins"))
case("err_wins_too_large", func("99999999999999999999 wins"))

# who would win with an edition
case("ok_edition_basic", func("who would win? rax or rbx (2026 edition)", "2026: rax wins", "2026: rbx wins"))
case("ok_edition_reused", func(
    "who would win? rax or rbx (2026 edition)", "2026: rax wins", "2026: rbx wins",
    "who would win? rax or rbx (2027 edition)", "2027: rax wins", "2027: rbx wins",
    "who would win? rax or rbx", "rax wins", "rbx wins",
    "who would win? rbx or rax (2026 edition)"))
case("ok_edition_same_register", func("who would win? rax or rax (x edition)", "x: rax wins"))
case("ok_edition_names", func(
    "who would win? rax or rbx (a.b$_1 edition)", "a.b$_1: rax wins", "a.b$_1: rbx wins",
    "who would win? rax or rbx (1 edition)", "1: rax wins", "1: rbx wins",
    "who would win? rax or rbx (Rax edition)", "Rax: rax wins", "Rax: rbx wins",
    "who would win? rax or rbx (rax edition)", "rax: rax wins", "rax: rbx wins",
    "who would win? rax or rbx ($ edition)", "$: rax wins", "$: rbx wins",
    "who would win? rax or rbx (. edition)", ".: rax wins", ".: rbx wins",
    "who would win? rax or rbx (007 edition)", "007: rax wins", "007: rbx wins",
    "who would win? rax or rbx (7 edition)", "7: rax wins", "7: rbx wins",
    "who would win? rax or rbx (edition edition)", "edition: rax wins", "edition: rbx wins"))
case("ok_edition_imm_and_chars", func(
    "who would win? al or 5 (e edition)", "e: al wins", "e: 5 wins",
    "who would win? al or a (e edition)", "e: a wins",
    "who would win? al or \\v (e edition)", "e: \\v wins",
    "who would win? al or \\s (e edition)", "e: space wins",
    "who would win? rax or -1 (e edition)", "e: -1 wins", "e: rax wins",
    "who would win? r8d or 4294967295 (e edition)", "e: r8d wins", "e: 4294967295 wins",
    "who would win? ah or \\ (e edition)", "e: ah wins", "e: \\ wins"))
case("ok_edition_labels_before_comparison", func("2026: rbx wins", "2026: rax wins", "who would win? rax or rbx (2026 edition)"))
case("ok_edition_unused_labels", func("e: rax wins", "f: rax wins", "rax wins"))
case("ok_edition_extra_spaces", func("who would win?   rax  or   rbx   (2026    edition)", "2026:   rax   wins", "2026:  rbx wins"))
case("err_edition_missing_label", func("who would win? rax or rbx (2026 edition)", "2026: rax wins"))
case("err_edition_wrong_edition", func("who would win? rax or rbx (2026 edition)", "2027: rax wins", "rbx wins"))
case("err_edition_labels_without_edition", func("who would win? rax or rbx (2026 edition)", "rax wins", "rbx wins"))
case("err_edition_labels_only_with_edition", func("who would win? rax or rbx", "2026: rax wins", "2026: rbx wins"))
case("err_edition_duplicate_label", func("who would win? rax or rbx (2026 edition)", "2026: rax wins", "2026: rbx wins", "2026: rax wins"))
case("err_edition_dash", func("who would win? rax or rbx (a-b edition)", "a-b: rax wins", "a-b: rbx wins"))
case("err_edition_umlaut", func("who would win? rax or rbx (\xe4 edition)", "\xe4: rax wins", "\xe4: rbx wins"))
case("err_edition_parens", func("who would win? rax or rbx (() edition)", "(): rax wins", "(): rbx wins"))
case("err_edition_empty", func("who would win? rax or rbx ( edition)", ": rax wins", ": rbx wins"))
case("err_edition_colon_label", func("who would win? rax or rbx (2026 edition)", "2026: rax wins", "2026: rbx wins", ":: rax wins"))
case("err_edition_double_colon", func("2026:: rax wins"))
case("err_edition_without_parens", func("who would win? rax or rbx 2026 edition"))
case("err_edition_unclosed", func("who would win? rax or rbx (2026 edition"))
case("err_edition_space_before_colon", func("2026 : rax wins"))
case("err_edition_pointer", func("who would win? rax or rbx (2026" + PTR + " edition)", "2026: rax wins", "2026: rbx wins"))
case("err_edition_wins_pointer", func("2026: rax" + PTR + " wins"))
case("err_edition_label_pointer", func("2026:" + PTR + " rax wins"))
case("err_edition_comparison_pointer", func("who would win? rax" + PTR + " or rbx (e edition)", "e: rax wins", "e: rbx wins"))
case("err_edition_wins_invalid_param", func("e: xyz wins"))
case("err_edition_size_mismatch", func("who would win? rax or bl (e edition)", "e: rax wins", "e: bl wins"))

# they're the same picture
case("ok_same_picture", func(
    "corporate needs you to find the difference between rax and rbx",
    "corporate needs you to find the difference between eax and 5",
    "corporate needs you to find the difference between al and a",
    "corporate needs you to find the difference between al and \\n",
    "corporate needs you to find the difference between r8w and -1",
    "corporate needs you to find the difference between ah and bh",
    "corporate needs you to find the difference between rax" + PTR + " and rbx",
    "corporate needs you to find the difference between rbx and rax" + PTR,
    "corporate needs you to find the difference between cl and esi" + PTR,
    "they're the same picture"))
case("ok_same_picture_label_only", func("they're the same picture"))
case("err_same_picture_missing", func("corporate needs you to find the difference between rax and rbx"))
case("err_same_picture_twice", func("they're the same picture", "they're the same picture"))
case("err_same_picture_size_mismatch", func("corporate needs you to find the difference between rax and bl", "they're the same picture"))
case("err_same_picture_pointer_imm", func("corporate needs you to find the difference between rax" + PTR + " and 5", "they're the same picture"))
case("err_same_picture_64bit_imm", func("corporate needs you to find the difference between rax and 2147483648", "they're the same picture"))
case("err_same_picture_high_byte_rex", func("corporate needs you to find the difference between ah and dil", "they're the same picture"))

# ---------------------------------------------------------------------------------------------
# I/O
case("ok_write_char_registers", func(*["what can I say except " + r for r in R8]))
case("ok_write_char_letters", func(*["what can I say except " + c for c in "aZzA!?.,:;#'\"`~^%&*()[]{}<>|/@+-=_"]))
case("ok_write_char_digits", func(*["what can I say except " + c for c in "0123456789"]))
case("ok_write_char_escapes", func(*["what can I say except " + e for e in
                                     ["\\n", "\\s", "space", "\\t", "\\f", "\\b", "\\v", "\\\"", "\\?", "\\\\", "\\"]]))
case("ok_write_char_ascii_codes", func(*["what can I say except " + c for c in
                                         ["10", "32", "65", "065", "0065", "00", "000", "01", "08", "09", "010",
                                          "255", "0255", "128", "+65", "-0", "+0", "+010", "-00", "99", "100",
                                          "200", "000000000000000000000000000065"]]))
case("ok_write_char_special_bytes", func(*["what can I say except " + chr(b) for b in
                                           [0x01, 0x07, 0x0B, 0x0C, 0x1B, 0x7F, 0x80, 0xC3, 0xFF]]))
case("ok_write_char_cr_before_crlf", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\r\n"
                                     b"what can I say except \r\r\n" + RET.encode() + b"\r\n")
case("err_write_char_256", func("what can I say except 256"))
case("err_write_char_minus_1", func("what can I say except -1"))
case("err_write_char_two_letters", func("what can I say except ab"))
case("err_write_char_r64", func("what can I say except rax"))
case("err_write_char_r32", func("what can I say except eax"))
case("err_write_char_pointer", func("what can I say except rax" + PTR))
case("err_write_char_pointer_r8", func("what can I say except al" + PTR))
case("err_write_char_char_pointer", func("what can I say except a" + PTR))
case("err_write_char_unknown_escape", func("what can I say except \\x"))
case("err_write_char_escape_e", func("what can I say except \\e"))
case("err_write_char_escape_0", func("what can I say except \\0"))
case("err_write_char_uppercase_space", func("what can I say except Space"))
case("err_write_char_hex", func("what can I say except 0x41"))
case("err_write_char_no_param", func("what can I say except"))
case("ok_read_char", func(*["let me in. LET ME IIIIIIIIN " + r for r in R8]))
case("err_read_char_r64", func("let me in. LET ME IIIIIIIIN rax"))
case("err_read_char_char", func("let me in. LET ME IIIIIIIIN a"))
case("err_read_char_pointer", func("let me in. LET ME IIIIIIIIN al" + PTR))
case("err_read_char_pointer_r64", func("let me in. LET ME IIIIIIIIN rax" + PTR))
case("err_read_char_wrong_case", func("let me in. LET ME IIIIIIIN al"))

# memory
case("ok_free_real_estate", func(*["it's free real estate " + r for r in R64]))
case("err_free_real_estate_r32", func("it's free real estate eax"))
case("err_free_real_estate_decimal", func("it's free real estate 4096"))
case("err_free_real_estate_pointer", func("it's free real estate rax" + PTR))

# random commands
case("ok_random_commands", func(
    "guess I'll die", "wait, that's illegal", "oh no! anyway", "refuses to elaborate and leaves",
    "you shall not pass!", "Houston, we have a problem", "we need air support", "it's a trap"))
case("ok_shall_not_pass_twice", func("you shall not pass!", "upvote rax", "you shall not pass!"))
case("ok_rdrand", func(*["it's dangerous to go alone, take " + r for r in R64 + R32 + R16]))
case("err_rdrand_r8", func("it's dangerous to go alone, take al"))
case("err_rdrand_decimal", func("it's dangerous to go alone, take 5"))
case("err_rdrand_pointer", func("it's dangerous to go alone, take rax" + PTR))
case("err_die_with_param", func("guess I'll die rax"))
case("err_illegal_wrong_quote", func("wait, that\u2019s illegal"))

# confused stonks
case("ok_confused_stonks", main("upvote rax", "confused stonks", "downvote rax", "upvote rbx"))
case("ok_confused_stonks_twice", lines(*fn("f", ["confused stonks", "upvote rax"], RET),
                                       *fn("main", ["confused stonks", "f: whomst has summoned the almighty one"], WIN)))
case("ok_confused_stonks_one_line_function", lines(DEF + "f", "confused stonks", RET))
case("ok_confused_stonks_or_draw_25", main("upvote rax", "confused stonks or draw 25", "downvote rax"))
case("ok_confused_stonks_with_labels", main("monke au", "confused stonks", "upgrade", "fuck go back", "return to monke au"))

# perfectly balanced: only checked to assemble
case("ok_perfectly_balanced", main("perfectly balanced as all things should be", "upvote rax", "upvote rbx", "upvote rcx", "downvote rax"))
case("ok_perfectly_balanced_twice", lines(
    *fn("f", ["perfectly balanced as all things should be", "sneak 100 rax", "stonks rax", "not stonks rax",
              "what can I say except a", "rax is brilliant, but I like 5"], RET),
    *fn("main", ["perfectly balanced as all things should be", "upvote rax", "oh no! anyway",
                 "rax units are ready, with rbx more well on the way"], WIN)))
case("ok_perfectly_balanced_three_times", main(
    "perfectly balanced as all things should be", "perfectly balanced as all things should be",
    "perfectly balanced as all things should be", "upvote rax", "downvote rbx", "bitconneeeeeeect al 5",
    "what can I say except \\n", "oh no! anyway"))
case("ok_perfectly_balanced_indented_crlf", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun g\r\n"
                                            b"\t perfectly balanced as all things should be \t\r\n"
                                            b"\tupvote rax\r\n\tupvote rbx\r\n" + RET.encode() + b"\r\n")

# or draw 25
case("ok_or_draw_25", main("upvote rax or draw 25", "upvote rax  or draw 25", "\tsneak 100 rbx or draw 25"))
case("ok_or_draw_25_invalid_param", main("upvote xyz or draw 25", "rax is brilliant, but I like 99999999999999999999 or draw 25",
                                         "who would win? rax or rbx or draw 25", "monke xx or draw 25",
                                         "return to monke au or draw 25"))
case("ok_or_draw_25_pointer", main("upvote rax" + PTR + " or draw 25", "rax" + PTR + " is brilliant, but I like 5 or draw 25"))
case("ok_or_draw_25_label_commands", main("upgrade or draw 25", "fuck go back or draw 25", "they're the same picture or draw 25",
                                          "corporate needs you to find the difference between rax and rbx or draw 25",
                                          "monke au or draw 25", "monke au or draw 25"))
case("ok_or_draw_25_func_call", main("f: whomst has summoned the almighty one or draw 25",
                                     "who would win? rax or rbx (e edition) or draw 25", "e: rax wins or draw 25"))
case("err_or_draw_25_alone", main("or draw 25"))
case("err_or_draw_25_two_spaces", main("upvote rax or draw  25"))
case("err_or_draw_25_trailing_word", main("upvote rax or draw 25 x"))
case("err_or_draw_25_tab", main("upvote\trax\tor draw 25"))
case("err_or_draw_25_replaces_return", lines(DEF + "f", "upvote rax", RET + " or draw 25"))
case("err_or_draw_25_replaces_def", lines(DEF + "f or draw 25", RET))
case("err_or_draw_25_two_pointers", main("rax" + PTR + " is brilliant, but I like rbx" + PTR + " or draw 25"))
case("err_or_draw_25_incomplete_command", main("upvote or draw 25"))
case("ok_or_draw_25_after_return_value", lines(DEF + "f", RET, "upvote rax or draw 25", WIN))

# ---------------------------------------------------------------------------------------------
# pointers: parsing details
case("ok_pointer_extra_spaces_after", func("rax do you know de wey   is brilliant, but I like rbx", "stonks rbx do you know de wey   "))
case("ok_pointer_suffix_glued", func("rax do you know de weyis brilliant, but I like rbx"))
case("err_pointer_two_spaces_before", func("rax  do you know de wey is brilliant, but I like rbx"))
case("err_pointer_twice_same_param", func("stonks rax do you know de wey do you know de wey"))
case("err_pointer_glued_trailing", func("stonks rax do you know de weyx"))
case("err_pointer_partial", func("stonks rax do you know"))
case("err_pointer_uppercase", func("stonks rax Do you know de wey"))
case("ok_pointer_sizes", func("rax" + PTR + " is brilliant, but I like eax", "eax" + PTR + " is brilliant, but I like al",
                              "rsp" + PTR + " is brilliant, but I like r15w", "r13d" + PTR + " is brilliant, but I like r13d",
                              "rbx is brilliant, but I like rbx" + PTR, "bx is brilliant, but I like r12d" + PTR))

# ---------------------------------------------------------------------------------------------
# lexical quirks
case("ok_lex_comments", lines(
    "What the hell happened here? a comment before the function",
    "What the hell happened here?",
    "What the hell happened here?no space",
    DEF + "main",
    "What the hell happened here? upvote rax",
    "    What the hell happened here? indented with spaces",
    "\t\tWhat the hell happened here? indented with tabs",
    " \t What the hell happened here? mixed",
    "    upvote rax",
    WIN,
    "What the hell happened here? a comment after the last return"))
case("err_lex_comment_mid_line", func("upvote rax What the hell happened here? no"))
case("err_lex_comment_without_question_mark", func("What the hell happened here"))
case("err_lex_comment_lowercase", func("what the hell happened here? x"))
case("ok_lex_blank_lines", "\n\n  \n\t\n" + DEF + "f\n\n \t \n    upvote rax\n\n\n" + RET + "\n\n\t\n")
case("ok_lex_crlf", "\r\n".join(fn("main", ["upvote rax", "", "what can I say except \\n", "What the hell happened here? x"], WIN)) + "\r\n")
case("ok_lex_crlf_no_final_newline", "\r\n".join(fn("main", ["upvote rax"], WIN)))
case("err_lex_cr_cr_lf", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\r\nupvote rax\r\r\n" + RET.encode() + b"\r\n")
case("err_lex_cr_cr_lf_on_return", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\nupvote rax\n" + RET.encode() + b"\r\r\n")
case("err_lex_lone_cr_mid_line", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\nupvote rax\rupvote rbx\n" + RET.encode() + b"\n")
case("err_lex_lone_cr_as_line_end", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\rupvote rax\r" + RET.encode() + b"\r")
case("ok_lex_cr_quirk_last_line", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\nupvote rax\n" + RET.encode() + b"\rX")
case("ok_lex_cr_quirk_last_line_cr", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\nupvote rax\n" + RET.encode() + b"\r\r")
case("ok_lex_cr_quirk_last_line_nul", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\nupvote rax\n" + RET.encode() + b"\r\0")
case("err_lex_cr_last_line_unterminated", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\nupvote rax\n" + RET.encode() + b"\r")
case("err_lex_cr_last_line_two_bytes_after", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\nupvote rax\n" + RET.encode() + b"\rXY")
case("ok_lex_cr_quirk_whole_line", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\n" + RET.encode() + b"\n\rX")
case("ok_lex_cr_quirk_comment", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\n" + RET.encode() + b"\nWhat the hell happened here?\rX")
case("err_lex_cr_quirk_mid_file", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\nupvote rax\rX\n" + RET.encode() + b"\n")
case("ok_lex_cr_crlf_blank_line", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\r\n\r\n  \r\n\t\r\n" + RET.encode() + b"\r\n")
case("err_lex_cr_only_line", b"I like to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\n\r\r\n" + RET.encode() + b"\n")
case("ok_lex_tabs_before_first_token", "\t" + DEF + "f\n\t\tupvote rax\n \t upvote rbx\n\t" + RET + "\n")
case("ok_lex_tab_after_first_token", func("upvote\trax", "sneak\t100 rax", "rax\tis brilliant, but I like 5",
                                          "what\tcan I say except a", "f:\twhomst has summoned the almighty one"))
case("ok_lex_tab_after_first_token_def", "I\tlike to have fun, fun, fun, fun, fun, fun, fun, fun, fun, fun f\n" + RET + "\n")
case("err_lex_two_tabs_after_first_token", func("upvote\t\trax"))
case("err_lex_tab_later", func("rax is\tbrilliant, but I like 5"))
case("err_lex_tab_before_param", func("upvote \trax"))
case("err_lex_tab_in_return", lines(DEF + "f", "right back\tat ya, buckaroo"))
case("ok_lex_tab_before_decimal", func("stonks \t5", "rax is brilliant, but I like \t7", "who would win? rax or \t5 (e edition)", "e: \t5 wins", "e: rax wins"))
case("err_lex_tab_before_decimal_label", func("who would win? rax or \t5", "\t5 wins", "rax wins"))
case("ok_lex_whitespace_before_decimal", func("stonks \x0c5", "stonks \r5", "rax is brilliant, but I like \x0c\t-7"))
case("err_lex_vt_before_decimal", func("stonks \x0b5"))
case("ok_lex_tab_before_ascii_code", func("what can I say except \t65", "what can I say except \t065", "what can I say except \x0c\t0"))
case("err_lex_tab_before_single_char", func("what can I say except \ta"))
case("ok_lex_multiple_spaces", "   " + DEF.replace(" ", "  ") + "  f\n    upvote     rax\n  rax   is   brilliant,    but  I  like   5\n" + "   right   back  at  ya,  buckaroo\n")
case("ok_lex_trailing_blanks", func("upvote rax   ", "upvote rbx\t", "upvote rcx \t \t", "stonks rax" + PTR + " \t") .replace(RET + "\n", RET + " \t \n"))
case("err_lex_trailing_vt", func("upvote rax\x0b"))
case("err_lex_trailing_ff", func("upvote rax\x0c"))
case("err_lex_vt_line", func("\x0b"))
case("err_lex_ff_line", func("\x0c"))
case("ok_lex_nul_cuts_line", func("upvote rax\0junk", "upvote rbx \0 junk", "stonks rcx\0") .replace(RET + "\n", RET + "\0garbage\n"))
case("ok_lex_nul_in_comment", func("What the hell happened here?\0 x", "What the hell happened here? \0", "upvote rax"))
case("err_lex_nul_at_line_start", func("\0upvote rax"))
case("err_lex_nul_after_blanks", func("  \t\0"))
case("err_lex_nul_inside_comment_prefix", func("What the hell\0 happened here?"))
case("err_lex_nul_only_line", func("\0"))
case("ok_lex_no_trailing_newline", func("upvote rax").rstrip("\n"))
case("ok_lex_no_trailing_newline_comment", func("upvote rax") + "What the hell happened here? end")
case("err_lex_empty_file", b"")
case("err_lex_only_newlines", b"\n\n\n")
case("err_lex_only_blanks_crlf", b"\n\r\n \t\n\t\r\n   ")
case("err_lex_only_comments", lines("What the hell happened here? nothing", "    What the hell happened here? else"))
case("err_lex_uppercase_command", func("UPVOTE rax"))
case("err_lex_unicode_param", func("upvote r\xc3\xa4x"))
case("err_lex_glued_tokens", func("upvoterax"))
case("err_lex_missing_comma", func("rax is brilliant but I like 5"))
case("err_lex_extra_word", func("upvote rax please"))
case("ok_lex_tab_separated_first_param_wins", func("rax\twins", "who would win? rax or rax"))
case("ok_lex_long_line", func("rax is brilliant, but I like " + "0" * 500 + "1"))

# ---------------------------------------------------------------------------------------------
# numbers
case("ok_decimals_various", func(
    "rax is brilliant, but I like 0", "rax is brilliant, but I like -0", "rax is brilliant, but I like +0",
    "rax is brilliant, but I like 69", "rax is brilliant, but I like 420", "rax is brilliant, but I like +2147483647",
    "rax is brilliant, but I like -9223372036854775808", "rax is brilliant, but I like 9223372036854775807",
    "rax is brilliant, but I like 00000000000000000000009223372036854775807",
    "rax units are ready, with -2147483648 more well on the way",
    "eax units are ready, with 4294967295 more well on the way",
    "eax units are ready, with -2147483648 more well on the way",
    "ax units are ready, with 65535 more well on the way", "ax units are ready, with -32768 more well on the way",
    "al units are ready, with 255 more well on the way", "al units are ready, with -128 more well on the way",
    "ah units are ready, with 128 more well on the way"))
case("err_decimal_too_large_64bit_add", func("rax units are ready, with 9223372036854775808 more well on the way"))
case("err_decimal_r16_add_too_large", func("ax units are ready, with 65536 more well on the way"))
case("err_decimal_negative_overflow", func("rax is brilliant, but I like -99999999999999999999"))
case("err_decimal_spaces_inside", func("rax is brilliant, but I like 1 2"))
case("err_decimal_underscore", func("rax is brilliant, but I like 1_000"))
case("err_decimal_float", func("rax is brilliant, but I like 1.5"))
case("err_decimal_pointer", func("rax is brilliant, but I like 5" + PTR))
case("ok_chars_in_operands", func(
    "rax is brilliant, but I like a", "al is brilliant, but I like \\v", "al is brilliant, but I like \\\\",
    "al is brilliant, but I like \\", "al is brilliant, but I like '", "al is brilliant, but I like \\\"",
    "al is brilliant, but I like \\?", "al is brilliant, but I like space", "al is brilliant, but I like \\s",
    "al is brilliant, but I like \\t", "al is brilliant, but I like \\f", "al is brilliant, but I like \\b",
    "al is brilliant, but I like \\n", "al is brilliant, but I like -", "al is brilliant, but I like +",
    "al is brilliant, but I like \x7f", "al is brilliant, but I like \xff", "al is brilliant, but I like #"))

# ---------------------------------------------------------------------------------------------
# realistic programs (also run by run_programs.py)
PRINT_DEC = fn("printDec", [
    "What the hell happened here? prints rdi (>= 0) in decimal, preserves all registers",
    "stonks rax", "stonks rbx", "stonks rcx", "stonks r8",
    "rax is brilliant, but I like rdi",
    "sneak 100 rcx",
    "monke uaaaaaaa",
    "    rbx is brilliant, but I like rax",
    "    look at what 10 needs to mimic a fraction of rax",
    "    r8 is brilliant, but I like rax",
    "    r8 is getting out of hand, now there are 10 of them",
    "    parry r8 you filthy casual rbx",
    "    rbx units are ready, with 48 more well on the way",
    "    stonks rbx",
    "    upvote rcx",
    "    who would win? rax or 0 (pdDigits edition)",
    "    return to monke uaaaaaau",
    "    pdDigits: rax wins",
    "    return to monke uaaaaaaa",
    "    pdDigits: 0 wins",
    "monke uaaaaaau",
    "    not stonks rbx",
    "    what can I say except bl",
    "    downvote rcx",
    "    who would win? rcx or 0 (pdPrint edition)",
    "    return to monke uaaaaauu",
    "    pdPrint: rcx wins",
    "    return to monke uaaaaaau",
    "    pdPrint: 0 wins",
    "monke uaaaaauu",
    "not stonks r8", "not stonks rcx", "not stonks rbx", "not stonks rax",
], RET)

case("ok_prog_fizzbuzz", lines(*PRINT_DEC, "", *fn("main", [
    "What the hell happened here? FizzBuzz from 1 to 30",
    "r12 is brilliant, but I like 1",
    "monke uuaaaaaa",
    "    sneak 100 r13",
    "    What the hell happened here? r14 = r12 % 3",
    "    r14 is brilliant, but I like r12",
    "    look at what 3 needs to mimic a fraction of r14",
    "    r14 is getting out of hand, now there are 3 of them",
    "    rbx is brilliant, but I like r12",
    "    parry r14 you filthy casual rbx",
    "    who would win? rbx or 0 (fizz edition)",
    "    what can I say except F",
    "    what can I say except i",
    "    what can I say except z",
    "    what can I say except z",
    "    upvote r13",
    "    fizz: rbx wins",
    "    fizz: 0 wins",
    "    What the hell happened here? r14 = r12 % 5",
    "    r14 is brilliant, but I like r12",
    "    look at what 5 needs to mimic a fraction of r14",
    "    r14 is getting out of hand, now there are 5 of them",
    "    rbx is brilliant, but I like r12",
    "    parry r14 you filthy casual rbx",
    "    who would win? rbx or 0 (buzz edition)",
    "    what can I say except B",
    "    what can I say except u",
    "    what can I say except z",
    "    what can I say except z",
    "    upvote r13",
    "    buzz: rbx wins",
    "    buzz: 0 wins",
    "    who would win? r13 or 0 (num edition)",
    "    rdi is brilliant, but I like r12",
    "    printDec: whomst has summoned the almighty one",
    "    num: r13 wins",
    "    num: 0 wins",
    "    what can I say except \\n",
    "    upvote r12",
    "    who would win? r12 or 30 (loop edition)",
    "    return to monke uuaaaaaa",
    "    loop: 30 wins",
    "    return to monke uuaaaaaa",
    "    loop: r12 wins",
], WIN)))

case("ok_prog_fibonacci", lines(*fn("main", [
    "What the hell happened here? the first 20 Fibonacci numbers, separated by spaces",
    "sneak 100 rbx",
    "r12 is brilliant, but I like 1",
    "r13 is brilliant, but I like 20",
    "banana",
    "    rdi is brilliant, but I like rbx",
    "    printDec: whomst has summoned the almighty one",
    "    what can I say except space",
    "    rax is brilliant, but I like rbx",
    "    rax units are ready, with r12 more well on the way",
    "    rbx is brilliant, but I like r12",
    "    r12 is brilliant, but I like rax",
    "    downvote r13",
    "    corporate needs you to find the difference between r13 and 0",
    "where banana",
    "they're the same picture",
    "what can I say except \\n",
], WIN), "", *PRINT_DEC))

case("ok_prog_factorial_recursive", lines(
    *fn("fact", [
        "What the hell happened here? rax = rdi!, recursive",
        "who would win? rdi or 1 (base edition)",
        "rax is brilliant, but I like 1",
        "right back at ya, buckaroo",
        "base: 1 wins",
        "rax is brilliant, but I like 1",
        "right back at ya, buckaroo",
        "base: rdi wins",
        "stonks rdi",
        "downvote rdi",
        "fact: whomst has summoned the almighty one",
        "not stonks rdi",
        "rax is getting out of hand, now there are rdi of them",
    ], RET), "",
    *fn("main", [
        "r12 is brilliant, but I like 0",
        "upgrade",
        "    rdi is brilliant, but I like r12",
        "    fact: whomst has summoned the almighty one",
        "    rdi is brilliant, but I like rax",
        "    printDec: whomst has summoned the almighty one",
        "    what can I say except \\n",
        "    upvote r12",
        "    corporate needs you to find the difference between r12 and 21",
        "fuck go back",
        "they're the same picture",
    ], WIN), "", *PRINT_DEC))

case("ok_prog_power_and_bits", lines(*fn("main", [
    "What the hell happened here? exercises power, shifts, not, and, imul, division of negatives",
    "rbx is brilliant, but I like 3",
    "rbx UNLIMITED POWER 5",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "rbx is brilliant, but I like 2",
    "rcx is brilliant, but I like 10",
    "rbx UNLIMITED POWER rcx",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "rbx is brilliant, but I like -1",
    "rbx UNLIMITED POWER 7",
    "rbx \\s",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "rbx is brilliant, but I like 5",
    "rbx UNLIMITED POWER -2",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "rbx is brilliant, but I like 1",
    "upgrades, people. Upgrades rbx",
    "upgrades, people. Upgrades rbx",
    "upgrades, people. Upgrades rbx",
    "upgrades, people. Upgrades rbx",
    "they had us in the first half, not gonna lie rbx",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "rbx is brilliant, but I like 4294967295",
    "bitconneeeeeeect rbx 3855",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "rbx is brilliant, but I like -100",
    "look at what -7 needs to mimic a fraction of rbx",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "rbx is brilliant, but I like 1000",
    "rcx is brilliant, but I like 7",
    "look at what rcx needs to mimic a fraction of rbx",
    "rbx is getting out of hand, now there are rcx of them",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "ebx is brilliant, but I like 4294967295",
    "upvote ebx",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "sneak 100 rbx",
    "bl is brilliant, but I like 255",
    "upvote bl",
    "bh is brilliant, but I like 1",
    "rdi is brilliant, but I like rbx",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
    "rax is brilliant, but I like 0 or draw 25",
    "rdi is brilliant, but I like rax",
    "bitconneeeeeeect rdi 0",
    "rdi units are ready, with 1 more well on the way",
    "printDec: whomst has summoned the almighty one",
    "what can I say except \\n",
], WIN), "", *PRINT_DEC))

case("ok_prog_bubble_sort", lines(*fn("main", [
    "What the hell happened here? sorts 10 numbers in memory from free real estate, then prints them",
    "rbx is brilliant, but I like 80",
    "it's free real estate rbx",
    "rcx is brilliant, but I like rbx",
    "rax is brilliant, but I like 31",
    "rdx is brilliant, but I like 10",
    "monke auaaaaa",
    "    rcx do you know de wey is brilliant, but I like rax",
    "    rax is getting out of hand, now there are 17 of them",
    "    bitconneeeeeeect rax 127",
    "    rcx units are ready, with 8 more well on the way",
    "    downvote rdx",
    "    who would win? rdx or 0 (fill edition)",
    "    return to monke auaaaua",
    "    fill: rdx wins",
    "    return to monke auaaaaa",
    "    fill: 0 wins",
    "monke auaaaua",
    "What the hell happened here? bubble sort: repeat until no swap",
    "monke auaaaau",
    "    sneak 100 r8",
    "    rcx is brilliant, but I like rbx",
    "    r9 is brilliant, but I like 9",
    "    monke auaaauu",
    "        r10 is brilliant, but I like rcx do you know de wey",
    "        rcx units are ready, with 8 more well on the way",
    "        r11 is brilliant, but I like rcx do you know de wey",
    "        who would win? r10 or r11 (cmp edition)",
    "        return to monke auaauuu",
    "        cmp: r11 wins",
    "        return to monke auaauuu",
    "        cmp: r10 wins",
    "        rcx do you know de wey is brilliant, but I like r10",
    "        parry 8 you filthy casual rcx",
    "        rcx do you know de wey is brilliant, but I like r11",
    "        rcx units are ready, with 8 more well on the way",
    "        upvote r8",
    "        monke auaauuu",
    "        downvote r9",
    "        who would win? r9 or 0 (inner edition)",
    "        return to monke auaauau",
    "        inner: r9 wins",
    "        return to monke auaaauu",
    "        inner: 0 wins",
    "        monke auaauau",
    "    who would win? r8 or 0 (outer edition)",
    "    return to monke auaauua",
    "    outer: r8 wins",
    "    return to monke auaaaau",
    "    outer: 0 wins",
    "monke auaauua",
    "What the hell happened here? print",
    "rcx is brilliant, but I like rbx",
    "rdx is brilliant, but I like 10",
    "monke auauuuu",
    "    rdi is brilliant, but I like rcx do you know de wey",
    "    printDec: whomst has summoned the almighty one",
    "    what can I say except space",
    "    rcx units are ready, with 8 more well on the way",
    "    downvote rdx",
    "    who would win? rdx or 0 (print edition)",
    "    return to monke auauuua",
    "    print: rdx wins",
    "    return to monke auauuuu",
    "    print: 0 wins",
    "monke auauuua",
    "what can I say except \\n",
], WIN), "", *PRINT_DEC))

case("ok_prog_echo_upper", lines(*fn("main", [
    "What the hell happened here? copies stdin to stdout in upper case until the end of input (a read gives 0)",
    "monke uuuaa",
    "    sneak 100 rax",
    "    let me in. LET ME IIIIIIIIN al",
    "    who would win? al or 0 (eof edition)",
    "    no, I don't think I will",
    "    eof: 0 wins",
    "    no, I don't think I will",
    "    eof: al wins",
    "    who would win? al or 96 (lower edition)",
    "    lower: 96 wins",
    "    what can I say except al",
    "    return to monke uuuaa",
    "    lower: al wins",
    "    who would win? al or z (upper edition)",
    "    upper: z wins",
    "    parry 32 you filthy casual al",
    "    upper: al wins",
    "    what can I say except al",
    "    return to monke uuuaa",
], WIN)))

case("ok_prog_stack_and_chars", lines(*fn("main", [
    "What the hell happened here? pushes characters and prints them in reverse; exercises 8 and 16 bit registers",
    "stonks \\n",
    "stonks !",
    "stonks d",
    "stonks 108",
    "stonks r",
    "stonks o",
    "stonks w",
    "stonks space",
    "stonks 111",
    "stonks l",
    "stonks l",
    "stonks e",
    "stonks H",
    "r12 is brilliant, but I like 13",
    "monke uuauaua",
    "    not stonks rax",
    "    what can I say except al",
    "    downvote r12",
    "    corporate needs you to find the difference between r12 and 0",
    "    return to monke uuauaua",
    "they're the same picture",
    "sneak 100 rcx",
    "cx is brilliant, but I like 16706",
    "what can I say except cl",
    "what can I say except ch",
    "ch is brilliant, but I like cl",
    "upvote ch",
    "what can I say except ch",
    "r8w is brilliant, but I like 67",
    "r8w units are ready, with 1 more well on the way",
    "what can I say except r8b",
    "dil is brilliant, but I like \\v",
    "dil units are ready, with \\t more well on the way",
    "dil units are ready, with \\b more well on the way",
    "dil units are ready, with 065 more well on the way",
    "what can I say except dil",
    "what can I say except 065",
    "what can I say except \\\\",
    "what can I say except \\",
    "what can I say except \\\"",
    "what can I say except \\?",
    "what can I say except \\t",
    "what can I say except \\s",
    "what can I say except '",
    "what can I say except \\n",
    "oh no! anyway",
    "wait, that's illegal",
], WIN)))

case("ok_prog_exit_code", lines(*fn("main", [
    "What the hell happened here? exits with status 1 after printing something",
    "what can I say except o",
    "what can I say except k",
    "what can I say except \\n",
    "who would win? rax or rax",
    "rax wins",
], LOSE)))

case("ok_prog_syscall_exit", lines(*fn("main", [
    "What the hell happened here? exit(42) via air support",
    "what can I say except b",
    "what can I say except y",
    "what can I say except e",
    "what can I say except \\n",
    "rax is brilliant, but I like 60",
    "rdi is brilliant, but I like 42",
    "we need air support",
], WIN)))

case("ok_prog_memory_string", lines(*fn("main", [
    "What the hell happened here? builds a string in memory with 32 bit pointers and byte stores, then prints it",
    "r12 is brilliant, but I like 64",
    "it's free real estate r12",
    "rsi is brilliant, but I like r12",
    "al is brilliant, but I like M",
    "rsi do you know de wey is brilliant, but I like al",
    "upvote rsi",
    "al is brilliant, but I like e",
    "rsi do you know de wey is brilliant, but I like al",
    "upvote rsi",
    "al is brilliant, but I like m",
    "rsi do you know de wey is brilliant, but I like al",
    "upvote rsi",
    "al is brilliant, but I like e",
    "rsi do you know de wey is brilliant, but I like al",
    "upvote rsi",
    "eax is brilliant, but I like 560821057",
    "rsi do you know de wey is brilliant, but I like eax",
    "rsi units are ready, with 4 more well on the way",
    "ax is brilliant, but I like 10",
    "rsi do you know de wey is brilliant, but I like ax",
    "rsi is brilliant, but I like r12",
    "banana",
    "    bl is brilliant, but I like rsi do you know de wey",
    "    corporate needs you to find the difference between bl and 0",
    "    what can I say except bl",
    "    upvote rsi",
    "where banana",
    "they're the same picture",
    "rax is brilliant, but I like 7",
    "r12 do you know de wey is brilliant, but I like rax",
    "r12 do you know de wey units are ready, with rax more well on the way",
    "rbx is brilliant, but I like r12 do you know de wey",
    "bitconneeeeeeect rbx r12 do you know de wey",
    "parry rax you filthy casual rbx",
    "look at what rax needs to mimic a fraction of r12 do you know de wey",
    "rdi is brilliant, but I like r12 do you know de wey",
    "rdi units are ready, with rbx more well on the way",
    "rdi units are ready, with 48 more well on the way",
    "what can I say except dil",
    "what can I say except \\n",
], WIN)))

# ---------------------------------------------------------------------------------------------
# examples of the reference repository
EXAMPLES = "/home/janezrotman.guest/work/MemeAssembly/examples"
for src, name in [
    ("HelloWorld.memeasm", "HelloWorld"), ("alphabet.memeasm", "alphabet"), ("brainfuck.memeasm", "brainfuck"),
    ("free-real-estate.memeasm", "free_real_estate"), ("is_nice.memeasm", "is_nice"),
    ("reverse-string.memeasm", "reverse_string"), ("the-link.memeasm", "the_link"),
    ("Stalinsort/stalin-sort.memeasm", "stalinsort"), ("rot13/rot13.memeasm", "rot13"),
    ("toupper/toupper.memeasm", "toupper"),
]:
    with open(os.path.join(EXAMPLES, src), "rb") as f:
        case("ok_example_" + name, f.read())


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for name, data in CASES.items():
        with open(os.path.join(out, name + ".memeasm"), "wb") as f:
            f.write(data)
    print(len(CASES), "cases written")
