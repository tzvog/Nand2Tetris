(SimpleFunction.test)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1
@0
D=A
@LOC_HOLDER
M=D
@LCL
D=M
@LOC_HOLDER
M=M+D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@LOC_HOLDER
M=D
@LCL
D=M
@LOC_HOLDER
M=M+D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
A=A-1
D=M
A=A-1
M=M+D
@SP
M=M-1
@SP
A=M
A=A-1
M=!M
@0
D=A
@LOC_HOLDER
M=D
@ARG
D=M
@LOC_HOLDER
M=M+D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
A=A-1
D=M
A=A-1
M=M+D
@SP
M=M-1
@1
D=A
@LOC_HOLDER
M=D
@ARG
D=M
@LOC_HOLDER
M=M+D
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M
A=A-1
D=M
A=A-1
M=M-D
@SP
M=M-1
@LCL
D=M
@R11
M=D
@5
A=D-A
D=M
@R12
M=D
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R11
D=M-1
M=D
A=M
D=M
@THAT
M=D
@R11
D=M-1
M=D
A=M
D=M
@THIS
M=D
@R11
D=M-1
M=D
A=M
D=M
@ARG
M=D
@R11
D=M-1
M=D
A=M
D=M
@LCL
M=D
@R12
A=M
0;JMP
