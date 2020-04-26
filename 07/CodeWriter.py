from Parser import *

POP_FUNCTION = "pop"
PUSH_FUNCTION = "push"
CONST = "constant"

operator_dict = {
    "and": "&",
    "add": "+",
    "or": "|",
    "sub": "-"
}

compare_dict = {
    "eq": "JEQ",
    "gt": "JLT",
    "lt": "JGT"
}

self_switch_dict = {
    "neg": "-",
    "not": "!"
}

location_to_asm_dict = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "temp": "R5",
    "pointer": "R3"
}


class CodeWriter:

    def __init__(self, output_file_name):
        """
        constructor
        :param output_file_name: the name of the output file
        """
        self.func_counter = 0
        self.asm_file = open(output_file_name, "w")

    def set_file_name(self, vm_file_name):
        """
        the method receives a name of a file and compiles it into vm code
        :param vm_file_name: the file to be compiled
        :return:
        """

        current_vm_file = Parser(vm_file_name)
        only_file_name = vm_file_name.split('/')[-1]
        only_file_name = only_file_name.split('.')[0]

        while current_vm_file.has_more_commands():

            # move the file a line
            current_vm_file.advance()

            # gets the type of the line
            cm_type = current_vm_file.command_type()

            # checks the type of the command
            if cm_type == ARITHMETIC:
                self.write_arithmetic(current_vm_file.current_command)
            elif cm_type == PUSH or cm_type == POP:
                self.write_push_pop(current_vm_file.current_command,
                                    only_file_name)

    def write_arithmetic(self, command):
        """
        the method receives an arithmetic command and compiles it into
        vm code, and writes the vm code into the file
        :param command: the command to be compiled
        :return:
        """

        if command in operator_dict:

            # sets pointer to first value
            self.asm_file.write("@SP\n"
                                "A=M\n"
                                "A=A-1\n")

            # saves first value and goes to next value and
            # adds it to next value
            self.asm_file.write("D=M\n"
                                "A=A-1\n"
                                "M=M" + operator_dict.get(command) + "D\n")

            # lowers value of pointer
            self.asm_file.write("@SP\n"
                                "M=M-1\n")

        elif command in compare_dict:
            # sets pointer to first value
            self.asm_file.write("@SP\n"
                                "M=M-1\n"
                                "A=M\n")
            # check if first value is positive, and if so jump
            self.asm_file.write("D=M\n"
                                "@A_POS" + str(self.func_counter) + "\n"
                                "D;JGT\n")
            # check if the second value is positive, and if so jump
            self.asm_file.write("@SP\n"
                                "A=M-1\n"
                                "D=M\n"
                                "@B_POS" + str(self.func_counter) + "\n"
                                "D;JGT\n")
            # a and b <= 0
            self.asm_file.write("@SAME_SIGN" + str(self.func_counter) + "\n"
                                "0;JMP\n")
            # a > 0
            self.asm_file.write("(A_POS" + str(self.func_counter) + ")\n")
            # check if b is positive
            self.asm_file.write("@SP\n"
                                "A=M-1\n"
                                "D=M\n"
                                "@SAME_SIGN" + str(self.func_counter) + "\n"
                                "D;JGT\n")
            # a > 0; b <= 0
            self.asm_file.write("@SP\n"
                                "A=M\n"
                                "D=M\n"
                                "@TRUE" + str(self.func_counter) + "\n"
                                "D;" + compare_dict.get(command) + "\n"
                                "@FALSE" + str(self.func_counter) + "\n"
                                "0;JMP\n")
            # b > 0, a <= 0
            self.asm_file.write("(B_POS" + str(self.func_counter) + ")\n"
                                "@SP\n"
                                "A=M\n"
                                "D=M\n"
                                "@TRUE" + str(self.func_counter) + "\n"
                                "D;" + compare_dict.get(command) + "\n"
                                "@FALSE" + str(self.func_counter) + "\n"
                                "0;JMP\n")
            # a and b have the same sign, compare the numbers
            self.asm_file.write("(SAME_SIGN" + str(self.func_counter) + ")\n"
                                "@SP\n"
                                "A=M\n"
                                "D=M-D\n"
                                "@TRUE" + str(self.func_counter) + "\n"
                                "D;" + compare_dict.get(command) + "\n"
                                "@FALSE" + str(self.func_counter) + "\n"
                                "0;JMP\n")
            # if the output is true
            self.asm_file.write("(TRUE" + str(self.func_counter) + ")\n"
                                "@SP\n"
                                "A=M-1\n"
                                "M=-1\n"
                                "@END" + str(self.func_counter) + "\n"
                                "0;JMP\n")
            self.asm_file.write("(FALSE" + str(self.func_counter) + ")\n"
                                "@SP\n"
                                "A=M-1\n"
                                "M=0\n")
            # end commands and lowers value of pointer
            self.asm_file.write("(END" + str(self.func_counter) + ")\n")
            self.func_counter += 1

            # # saves first value and goes to next value and
            # # removes it from next value
            # self.asm_file.write("D=M\nA=A-1\nM=M-D\nD=M\n")
            #
            # # creates a temp to hold the value
            # self.asm_file.write("@x\nM=D\nD=M\n")
            #
            # # lowers value of stack pointer
            # self.asm_file.write("@SP\nM=M-1\n")
            #
            # # checks if the value is equal to zero
            # self.asm_file.write("@FALSE" + str(self.func_counter) +
            #                     "\nD," + compare_dict.get(command) + "\n")
            #
            # # sets the value of d and goes to the end
            # self.asm_file.write("D=-1\n@END" + str(self.func_counter) +
            #                     "\n0;JMP\n")
            #
            # # sets the value if not equal
            # self.asm_file.write("(FALSE" + str(self.func_counter) +
            #                     ")\nD=0\n(END" + str(self.func_counter)
            #                     + ")\n")
            #
            # # gets the location we must set
            # self.asm_file.write("@SP\nA=M-1\nM=D\n")

            # raises the counter
            # self.func_counter += 1

        elif command in self_switch_dict:
            # sets pointer to first value
            self.asm_file.write("@SP\nA=M\nA=A-1\nM=" +
                                self_switch_dict.get(command) + "M\n")

    def write_push_pop(self, command, file_name):
        """
        writes the push and pop command to the file
        :param command: what command to write
        :return: none
        """

        command_type, location, destination = command.split(SPACE)

        if command_type == POP_FUNCTION:

            # pops a value from the stack
            self.asm_file.write("@SP\nA=M-1\nD=M\n")

            # lowers the value of the SP
            self.asm_file.write("@SP\nM=M-1\n")

            # creates a location to hold the value
            # until we set the pointer location
            self.asm_file.write("@pop_holder\nM=D\n")

            # gets the location above the stack we need to push
            self.asm_file.write("@" + destination + "\n" + "D=A\n")

            # sets the location we need to the value from
            self.asm_file.write("@LOC_HOLDER\nM=D\n")

            if location in location_to_asm_dict:

                self.asm_file.write("@" + location_to_asm_dict.get(location)
                                    + "\nD=")
            else:
                self.asm_file.write("@" + file_name + "." + str(destination)
                                    + "\nD=")

            # checks if we are dealing with a pointer location or addressing
            if location != "temp" and location != "pointer":
                self.asm_file.write("M\n")
            else:
                self.asm_file.write("A\n")

            self.asm_file.write("@LOC_HOLDER\nM=M+D\n")
            self.asm_file.write("@pop_holder\nD=M\n")
            self.asm_file.write("@LOC_HOLDER\nA=M\nM=D\n")

        # if we are dealing with a push command
        elif command_type == PUSH_FUNCTION:

            # gets a value for the a destination since we cannot
            # use number bigger than one will just use it as a
            # pointer location
            self.asm_file.write("@" + destination + "\n" + "D=A\n")

            if location != CONST:
                # sets the location we need to the value from
                self.asm_file.write("@LOC_HOLDER\nM=D\n")

                if location in location_to_asm_dict:

                    self.asm_file.write("@" + location_to_asm_dict.get(location)
                                        + "\nD=")
                else:
                    self.asm_file.write("@" + file_name + "." + str(destination)
                                        + "\nD=")

                # checks if we are dealing with a pointer location or addressing
                if location != "temp" and location != "pointer":
                    self.asm_file.write("M\n")
                else:
                    self.asm_file.write("A\n")

                self.asm_file.write("@LOC_HOLDER\nM=M+D\n")
                self.asm_file.write("A=M\nD=M\n")

            # pushes the value of D onto the stack
            self.asm_file.write("@SP\nA=M\nM=D\n")

            # raises the location of the stack pointer
            self.asm_file.write("@SP\nM=M+1\n")

    def close(self):
        self.asm_file.close()
