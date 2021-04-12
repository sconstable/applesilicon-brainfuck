# Apple Silicon Brainfuck
A very simple brainfuck compiler for apple silicon (m1) macs, written in python. 
Inspired by a hilarious post I read on [scalable, resilient brainfuck](https://zserge.com/posts/bfaas/) 
 I decided to finally get around with playing with arm64 (AArch64) assembly on my new 
 Apple Silicon MacBook Air 💻.  I haven't touched assembly in over a decade, but this was 
 a lot of fun!  [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) is a very simple 
 language that is technically Turing complete but it's very easy to implement.
 
 ## Usage
 There are two steps: a compilation step and an assembly step.  To compile some brainfuck 
 source code simply supply it as an argument to `bfc.py`:
 ```
 $ ./bfc.py "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++."
 ```
 note the use of quotes "" to ensure the shell does not misinterpret the >< characters. 
 This will generate some raw arm64 assembly in a file named `output.s` and that's basically 
 the entire point of this project. Please do peruse the contents of `output.s`
 
 In order to actually run this, you'll need to 
 assemble the instructions into a real binary using the included `assemble.sh` script:
 ```
 $ ./assemble.sh output.s
 ```
 this will generate a binary which can be executed directly:
 ```
 $ ./output
 Hello World!
 ```
 
 ## Limitations
 This was mainly an exercise for myself so it's not the greatest implementation.  The 
 biggest drawback is probably that the stack sized allocated is only 16 cells, which is 
 probably not enough for some of the bigger brainfuck programs.  However, this could be 
 easily raised in theory.
 
 Also, I only ever tested this on my MacBook Air 2020 (M1), so your milage may vary.  I 
 think in principle it could run under linux on a raspberry pi 3/4 with some minor tweaks 
 in `assemble.sh` (namely not linking to libSystem). It should not work on any x86 PC.
 
 Other than that there are definitely some low hanging fruit for optimization, I'll leave 
 that as a treat for myself.  Maybe one day I'll have a full compiler/interpreter in 
 arm64 assembly!
 
 ## Acknowledgements
 Most of my understanding was gleaned by compiling small trivial C programs with clang and
 reading the disassembled binary.  However, there were a number of references I relied on 
 that I'd like to list out below:
 - https://modexp.wordpress.com/2018/10/30/arm64-assembly/
 - https://en.wikipedia.org/wiki/Brainfuck (duh)
 - https://github.com/below/HelloSilicon
 
 ## License
 [Creative Commons Zero](https://creativecommons.org/share-your-work/public-domain/cc0/), 
 which is as close to public domain as we can get. 