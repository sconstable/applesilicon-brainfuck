#!/usr/bin/env python3
import sys

if len(sys.argv) != 2:
     print(f"Usage: {sys.argv[0]} brainfuck-source")
     exit()
# TODO: replace this with reading a .b file
prog = sys.argv[1]
print(f"compiling program: {prog}")

# needed to implement loops
loopcounter = 0
loopstack = []  # it's a stack

with open('output.s', 'w') as outf:
    # write header
    outf.write(".text\n")
    outf.write(".global _start\n")
    outf.write(".align 4\n")
    outf.write("_start:\n")
    # allocate 256 bits of stack space
    outf.write("sub sp, sp, #0x100\n")
    # copy the stack pointer to x1, x1 will be our cell pointer
    outf.write("mov x1, sp\n")
    # initialize our 16 cells (16 bits each) to zero
    for i in range(16):
        outf.write(f"str xzr, [x1, #{i*16}]\n")
    # this is the big one
    for char in prog:
        if char == '+':
            outf.write("ldr x7, [x1]\n")    # load current cell into x7
            outf.write("add x7, x7, #1\n")  # increment value by 1
            outf.write("str x7, [x1]\n")    # store new value in memory
        elif char == '-':
            outf.write("ldr x7, [x1]\n")    
            outf.write("add x7, x7, #-1\n") # decrement value by 1
            outf.write("str x7, [x1]\n")    
        elif char == '>':
            outf.write("add x1, x1, #16\n") # increment pointer to next cell
        elif char == '<':
            outf.write("add x1, x1, #-16\n")# decrement pointer to previous cell
        elif char == '.':
            outf.write("mov x6, x1\n")      # save value of x1 in x6 (x1 gets overwritten)
            outf.write("mov x0, #1\n")      # file descriptor of stdout is 1
            outf.write("mov x2, #1\n")      # length of string to be printed is also 1
            outf.write("mov x16, #4\n")     # in arm64, syscall 4 is write
            outf.write("svc #0x80\n")       # calls the kernel to print character
            outf.write("mov x1, x6\n")      # restore x1 since it got ruined by syscall
        elif char == ',':
            outf.write("mov x6, x1\n")
            outf.write("mov x0, #0\n")      # file descriptor for stdin is 0
            outf.write("mov x2, #1\n")      # length of character to read is 1
            outf.write("mov x16, #3\n")     # in arm64, syscall 4 is read
            outf.write("svc #0x80\n")
            outf.write("mov x1, x6\n")
        elif char == '[':
            outf.write(f"LS{loopcounter}:\n")        # create a label for loop start N
            outf.write("ldr x7, [x1]\n")             # read the current cell value into x7
            outf.write(f"cbz x7, LC{loopcounter}\n") # if value is zero jump to loop close
            loopstack.append(loopcounter)            # push this loop index on the stack
            loopcounter += 1                         # start a new loop
        elif char == ']':
            loopind = loopstack.pop()                # pull most recent loop index
            outf.write(f"LC{loopind}:\n")            # write a label for loop close N
            outf.write("ldr x7, [x1]\n")             # load current cell value into x7
            outf.write(f"cbnz x7, LS{loopind}\n")    # if value != zero jump to loop start
    
    outf.write("add sp, sp, #0x100\n")      # restore stack pointer to original position
    outf.write("mov w0, #0\n")              # set return code to 0
    outf.write("ret\n")                     # exit
