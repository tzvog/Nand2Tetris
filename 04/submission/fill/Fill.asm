// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


// sets the location of the end of the screen 
@8191
D=A
@ScreenEnd
M=D


(LOOP)
	@index
	M=0
	
	// gets the keyboard input  
	@KBD
	D=M
		
	// jumps if it is equal to 	
	@WHITE
	D;JEQ
	
	// sets our current color to black 
	@color
	M=-1
	
	// goes to the loop
	@COLOR_SCREEN
	0;JMP

// sets our current color to white 
(WHITE)
	@color
	M=0




(COLOR_SCREEN)

	// gets the current location 
	@index
	D=M
	
	// gets the ratio towards the end of the screen 
	@ScreenEnd
	D=D-M
	
	// goes to the loop if we are dealing are passed the screen 
	@LOOP
	D;JGT
	
	// gets the loation of the screen 
	@SCREEN
	D=A
	
	// sets the index of where we want to paint 
	@index
	D=D+M
	
	// sets our current address 
	@currentAddress
	M=D
	
	// gets the color we want to color with 
	@color
	D=M
	
	// paints the current address
	@currentAddress
	A=M
	M=D
	
	// raises the index by one 
	@index
	M=M+1
	
	// goes back to color the screen 
	@COLOR_SCREEN
	0;JMP







