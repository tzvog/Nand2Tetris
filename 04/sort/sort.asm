// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/sort.asm
//
//sorts the values in the array 

@R14
D=M

@start_location
M=D

@R15
D=M

@arrLen 
M=D
M=M-1

(BIG_LOOP)

   @start_location
   D=M

   @curLoc
   M=D

   // sets how long the big loop is going to be 
   @arrLen
   D=M

   @J_INDEX
   M=D

(SMALL_LOOP)
   
   	@curLoc
   	A=M
   	D=M

	@temp 
        M=D

        @curLoc
   	A=M
   	A=A+1
        D=M

        @temp
        M=D-M
	D=M

	@NO_SWAP
        D,JLT

        @curLoc
   	A=M
   	D=M

	@temp 
        M=D

        @curLoc
   	A=M
   	A=A+1
        D=M

        @curLoc
   	A=M
        M=D

       	@temp 
        D=M

        @curLoc
   	A=M
   	A=A+1
        M=D
       
(NO_SWAP)
   	// updates to the next location 
   	@curLoc
   	M=M+1 

   	@J_INDEX
   	M=M-1
   	D=M

   	// goes to the begning of the small loop  
   	@SMALL_LOOP
   	D,JNE

   // reduces a value by one of the size 
   @arrLen 
   M=M-1
   D=M

   // goes to the begning of the loop  
   @BIG_LOOP
   D,JNE

(END)
