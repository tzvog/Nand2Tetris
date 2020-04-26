// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/divide.asm

// Put your code here.

@R15
M=0

@R13
D=M
@n
M=D // divisor (mone)

@R14
D=M
@m
M=D // dividor (mechane)

@temp
M=1

// if dividor == 0
@m
D=M
@END
D;JEQ

// check that n != 0
@n
D=M
@END
D;JEQ


(LOOP)
    // check that n >= m
    @n
    D=M  
    @m
    D=D-M
    @SET_RESULT
    D,JLT

    @m 
    M = M<< // m *= 2
    @temp
    M = M<< // temp *= 2

    @LOOP
    0;JMP
	

(SET_RESULT)

    // check that temp != 0
    @temp
    M=M>>
    D=M
    @END
    D;JEQ

    // check if n >= m
    @n
    D=M
    @m
    M=M>>
    D=D-M
    @SET_RESULT
    D;JLT

    // update the result
    @temp
    D=M
    @R15
    M=M+D

    // update the value of n
    @m
    D=M
    @n
    M=M-D

    // return to start of the loop
    @SET_RESULT
    0;JMP

(END)
