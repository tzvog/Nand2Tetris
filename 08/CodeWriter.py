from Parser import *

POP_FUNCTION = "pop"
PUSH_FUNCTION = "push"
CONST = "constant"
TEMP = "temp"
POINTER = "pointer"

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
        self.label_counter = 0
        self.asm_file = open(output_file_name, "w")
        self.write_init()

    def write_init(self):
        """
        this function write the initial part of the code
        :return: none
        """

        # sets the pointer to the first part of the stack
        self.asm_file.write("@256\nD=A\n@SP\nM=D\n")

        self.write_call("Sys.init", 0)

    def save_pointers(self):
        """
        saves the location of previous pointers
        :return: previous pointers
        """

        # sets the value of the local in the stack
        self.asm_file.write("@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # sets the value of the arguments in the stack
        self.asm_file.write("@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # sets the value of the this in the stack
        self.asm_file.write("@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")
        # sets the value of the that in the stack
        self.asm_file.write("@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

    def set_file_name(self, vm_file_name):

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
            elif cm_type == FUNCTION:
                func, function_name, arguments = \
                    current_vm_file.current_command.split(' ')
                self.write_function(function_name, arguments)
            elif cm_type == LABEL:
                self.write_label(current_vm_file.current_command.split(' ')[1])
            elif cm_type == IF:
                self.write_if(current_vm_file.current_command.split(' ')[1])
            elif cm_type == RETURN:
                self.write_return()
            elif cm_type == CALL:
                call, function_name, arguments = \
                    current_vm_file.current_command.split(' ')
                self.write_call(function_name, arguments)
            elif cm_type == GOTO:
                self.write_goto(current_vm_file.current_command.split(' ')[1])

    def write_arithmetic(self, command):

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
                                "@A_POS" + str(self.label_counter) + "\n"
                                "D;JGT\n")
            # check if the second value is positive, and if so jump
            self.asm_file.write("@SP\n"
                                "A=M-1\n"
                                "D=M\n"
                                "@B_POS" + str(self.label_counter) + "\n"
                                "D;JGT\n")
            # a and b <= 0
            self.asm_file.write("@SAME_SIGN" + str(self.label_counter) + "\n"
                                "0;JMP\n")
            # a > 0
            self.asm_file.write("(A_POS" + str(self.label_counter) + ")\n")
            # check if b is positive
            self.asm_file.write("@SP\n"
                                "A=M-1\n"
                                "D=M\n"
                                "@SAME_SIGN" + str(self.label_counter) + "\n"
                                "D;JGT\n")
            # a > 0; b <= 0
            self.asm_file.write("@SP\n"
                                "A=M\n"
                                "D=M\n"
                                "@TRUE" + str(self.label_counter) + "\n"
                                "D;" + compare_dict.get(command) + "\n"
                                "@FALSE" + str(self.label_counter) + "\n"
                                "0;JMP\n")
            # b > 0, a <= 0
            self.asm_file.write("(B_POS" + str(self.label_counter) + ")\n"
                                "@SP\n"
                                "A=M\n"
                                "D=M\n"
                                "@TRUE" + str(self.label_counter) + "\n"
                                "D;" + compare_dict.get(command) + "\n"
                                "@FALSE" + str(self.label_counter) + "\n"
                                "0;JMP\n")
            # a and b have the same sign, compare the numbers
            self.asm_file.write("(SAME_SIGN" + str(self.label_counter) + ")\n"
                                "@SP\n"
                                "A=M\n"
                                "D=M-D\n"
                                "@TRUE" + str(self.label_counter) + "\n"
                                "D;" + compare_dict.get(command) + "\n"
                                "@FALSE" + str(self.label_counter) + "\n"
                                "0;JMP\n")
            # if the output is true
            self.asm_file.write("(TRUE" + str(self.label_counter) + ")\n"
                                "@SP\n"
                                "A=M-1\n"
                                "M=-1\n"
                                "@END" + str(self.label_counter) + "\n"
                                "0;JMP\n")
            self.asm_file.write("(FALSE" + str(self.label_counter) + ")\n"
                                "@SP\n"
                                "A=M-1\n"
                                "M=0\n")
            # end commands and lowers value of pointer
            self.asm_file.write("(END" + str(self.label_counter) + ")\n")
            self.label_counter += 1

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

            # if we are dealing with static no point of manipulating pointers
            if location == "static":
                self.asm_file.write("@" + file_name + "." + str(destination)
                                    + "\nM=D\n")
                return

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
            if location != TEMP and location != POINTER:
                self.asm_file.write("M\n")
            else:
                self.asm_file.write("A\n")

            self.asm_file.write("@LOC_HOLDER\nM=M+D\n")
            self.asm_file.write("@pop_holder\nD=M\n")
            self.asm_file.write("@LOC_HOLDER\nA=M\nM=D\n")

        # if we are dealing with a push command
        elif command_type == PUSH_FUNCTION:

            # if we are dealing with static no point of manipulating pointers
            if location == "static":
                self.asm_file.write("@" + file_name + "." + str(destination)
                                    + "\nD=M\n")
            else:
                # gets a value for the a destination since we cannot
                # use number bigger than one will just use it as a
                # pointer location
                self.asm_file.write("@" + destination + "\n" + "D=A\n")

                if location != CONST:
                    # sets the location we need to the value from
                    self.asm_file.write("@LOC_HOLDER\nM=D\n")

                    if location in location_to_asm_dict:

                        self.asm_file.write("@" +
                                            location_to_asm_dict.get(location)
                                            + "\nD=")
                    else:
                        self.asm_file.write("@" + file_name +
                                            "." + str(destination)
                                            + "\nD=")

                    # checks if we are dealing with a pointer
                    # location or addressing
                    if location != TEMP and location != POINTER:
                        self.asm_file.write("M\n")
                    else:
                        self.asm_file.write("A\n")

                    self.asm_file.write("@LOC_HOLDER\nM=M+D\n")
                    self.asm_file.write("A=M\nD=M\n")

            # pushes the value of D onto the stack
            self.asm_file.write("@SP\nA=M\nM=D\n")

            # raises the location of the stack pointer
            self.asm_file.write("@SP\nM=M+1\n")

    def write_function(self, name, argument_amount):
        """
        writes a function to the assembly page
        :param name: the function name
        :param argument_amount: the amount of arguments it receive
        :return: none
        """

        # writes the functions name as a label
        self.write_label(name)

        for x in range(int(argument_amount)):

            # fill with zero and raise stack pointer
            self.asm_file.write("@SP\nA=M\nM=0\n@SP\nM=M+1\n")

        self.label_counter += 1

    def write_label(self, label):
        """
        writes a label to the assembly
        :param label: the label to write
        :return: none
        """

        # writes the functions name
        self.asm_file.write("(" + label + ")\n")

    def write_if(self, new_loc):
        """
        writes the if function
        :return: none
        """

        # gets the value from the stack pointer and lowers it
        self.asm_file.write("@SP\nA=M-1\nD=M\n@SP\nM=M-1\n")

        # jumps based on if the previous place in the stack is negative
        self.asm_file.write("@" + new_loc + "\nD,JNE\n")

    def write_return(self):
        """
        write the return function to return all back to previous state
        :return: none
        """

        # holds the value in the local
        self.asm_file.write("@LCL\nD=M\n@R11\nM=D\n")

        # saves the value of where the return address
        self.asm_file.write("@5\nA=D-A\nD=M\n@R12\nM=D\n")

        # saves the value of where the last function ended
        self.asm_file.write("@ARG\nD=M\n@0\nD=D+A\n@R13\nM=D\n")

        # saves the last value of the stack pointer as in
        # the return val location
        self.asm_file.write("@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n")

        # sets the stack pointer to the new location
        self.asm_file.write("@ARG\nD=M\n@SP\nM=D+1\n")

        # sets that back to the previous location
        self.asm_file.write("@R11\nD=M-1\nM=D\nA=M\nD=M\n@THAT\nM=D\n")

        # sets this back to the previous location
        self.asm_file.write("@R11\nD=M-1\nM=D\nA=M\nD=M\n@THIS\nM=D\n")

        # sets ARG back to the previous location
        self.asm_file.write("@R11\nD=M-1\nM=D\nA=M\nD=M\n@ARG\nM=D\n")

        # sets local back to the previous location
        self.asm_file.write("@R11\nD=M-1\nM=D\nA=M\nD=M\n@LCL\nM=D\n")

        # jumps to the return address
        self.asm_file.write("@R12\nA=M\n0;JMP\n")

    def write_goto(self, new_loc):
        """
        writes the goto command
        :param new_loc: the new location
        :return: none
        """

        # jump to new location
        self.asm_file.write("@" + new_loc + "\n0;JMP\n")

    def write_call(self, name, argument_amount):
        """
        writes a call to a function
        :param name: the name of th efunction we want to go to
        :param argument_amount: the amount of arguments the function will take
        :return: none
        """

        # sets the location line the program needs to return too
        self.asm_file.write("@RETURN_" + str(self.label_counter) +
                            "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n")

        self.save_pointers()

        # resets the arguments and local location
        self.asm_file.write("@SP\nD=M\n@5\nD=D-A\n@" + str(argument_amount)
                            + "\nD=D-A\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n")

        # has the function call the main loop
        self.asm_file.write("@" + name + "\n0;JMP\n")

        # the next line to commit
        self.asm_file.write("(RETURN_" + str(self.label_counter) + ")\n")

        self.label_counter += 1

    def close(self):
        self.asm_file.close()
