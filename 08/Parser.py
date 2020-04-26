ARITHMETIC = "C_ARITHMETIC"
PUSH = "C_PUSH"
POP = "C_POP"
LABEL = "C_LABEL"
GOTO = "C_GOTO"
IF = "C_IF"
FUNCTION = "C_FUNCTION"
RETURN = "C_RETURN"
CALL = "C_CALL"
SPACE = ' '


class Parser:

    arithmetic_set = {"add", "sub", "neg", "eq", "gt",
                      "lt", "and", "or", "not"}

    def __init__(self, file_name):
        self.current_command = ""
        self.line_list = []
        self.read_file(file_name)
        self.line_number = 0

    def read_file(self, file_name):
        """
        reads a file given by the user and parses every line into the
        data structure
        :param file_name: the name of the file
        :return: none
        """
        fh = open(file_name)
        for line in fh:
            if line[0] != '/' and line[0] != '\n':
                line = line.split('/')[0]
                line = line.strip()
                self.line_list.append(line)
        fh.close()

    def has_more_commands(self):
        """
        checks if we have more commands to read
        :return:
        """
        if self.line_number == len(self.line_list):
            return False
        return True

    def advance(self):
        """
        gets the next line to deal with in the file
        :return: the line itself
        """

        if self.has_more_commands():
            self.line_number += 1
            self.current_command = self.line_list[self.line_number - 1]

    def command_type(self):
        """
        gets the type of the command
        :return:
        """

        type_def = self.current_command.split(' ')[0]

        if type_def in self.arithmetic_set:
            return ARITHMETIC
        elif type_def == "pop":
            return POP
        elif type_def == "push":
            return PUSH
        elif type_def == "label":
            return LABEL
        elif type_def == "goto":
            return GOTO
        elif type_def == "return":
            return RETURN
        elif type_def == "function":
            return FUNCTION
        elif type_def == "if-goto":
            return IF
        elif type_def == "call":
            return CALL

    def arg1(self):
        """
        gets the first part of the first argument
        :return: the first argument
        """

        current_command_type = self.command_type()

        # checks if we can call the function
        if current_command_type != RETURN:

            # checks if we are dealing with an arithmetic
            if current_command_type == ARITHMETIC:
                return self.current_command
            else:
                return self.current_command.split(SPACE)[1]

    def arg2(self):
        """
        gets the second argument
        :return: the second argument
        """

        current_command_type = self.command_type()

        if current_command_type == PUSH or current_command_type == POP \
                or current_command_type == FUNCTION or \
                current_command_type == CALL:
            return self.current_command.split(SPACE)[2]
