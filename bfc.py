#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
     print(f"Usage: {sys.argv[0]} brainfuck-source")
     exit()
prog = sys.argv[1]
print(f"compiling program: {prog}")

loopcounter = 0
loopstack = []

with open('output.s', 'w') as outf:
    # write header
    outf.write(".text\n")
    outf.write(".global _start\n")
    outf.write(".align 4\n")
    outf.write("_start:\n")
    outf.write("sub sp, sp, #0x100\n")
    outf.write("mov x1, sp\n")
    for i in range(16):
        outf.write(f"str xzr, [x1, #{i*16}]\n")
    for char in prog:
        if char == '+':
            outf.write("ldr x7, [x1]\n")
            outf.write("add x7, x7, #1\n")
            outf.write("str x7, [x1]\n")
        elif char == '-':
            outf.write("ldr x7, [x1]\n")
            outf.write("add x7, x7, #-1\n")
            outf.write("str x7, [x1]\n")
        elif char == '>':
            outf.write("add x1, x1, #16\n")
        elif char == '<':
            outf.write("add x1, x1, #-16\n")
        elif char == '.':
            outf.write("mov x6, x1\n")
            outf.write("mov x0, #1\n")
            outf.write("mov x2, #1\n")
            outf.write("mov x16, #4\n")
            outf.write("svc #0x80\n")
            outf.write("mov x1, x6\n")
        elif char == ',':
            outf.write("mov x6, x1\n")
            outf.write("mov x0, #0\n")
            outf.write("mov x2, #1\n")
            outf.write("mov x16, #3\n")
            outf.write("svc #0x80\n")
            outf.write("mov x1, x6\n")
        elif char == '[':
            outf.write(f"LS{loopcounter}:\n")
            outf.write("ldr x7, [x1]\n")
            outf.write(f"cbz x7, LC{loopcounter}\n")
            loopstack.append(loopcounter)
            loopcounter += 1
        elif char == ']':
            loopind = loopstack.pop()
            outf.write(f"LC{loopind}:\n")
            outf.write("ldr x7, [x1]\n")
            outf.write(f"cbnz x7, LS{loopind}\n")
    
    outf.write("add sp, sp, #0x100\n")
    outf.write("mov w0, #0\n")
    outf.write("ret\n")
