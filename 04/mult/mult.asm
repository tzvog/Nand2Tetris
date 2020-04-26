// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


    @R2
    M = 0 // R2 = 0

    @R1
    D = M

    @i
    M = D  // i = R2

    // if i >= 0
    @LOOP
    D;JGE

    // if i < 0
    @MINUSLOOP
    0;JMP
    

(LOOP)

    @i
    D=M

    @END
    D;JLE // if i==0 end loop

    @R0
    D=M
    @R2
    M=D+M // R2 = R2+R0

    @i
    M=M-1 // i=i-1

    @LOOP
    0;JMP

(MINUSLOOP)
    @i
    D=M

    @END
    D;JEQ // if i==0 end loop

    @R0
    D=M
    @R2
    M=M-D // R2=R2+R0

    @i
    M=M+1 // i=i+1

    @MINUSLOOP
    0;JMP

(END)