import Code
from SymbolTable import *

LINE_COMMAND = "L_COMMAND"
ADDRESS_COMMAND = "A_COMMAND"
CONTROL_COMMAND = "C_COMMAND"
FIRST_FREE_MEMORY_LOCATION = 16


class Parser:

    def __init__(self, file_name):
        self.current_command = ""
        self.line_list = []
        self.Table = SymbolTable()
        self.read_file(file_name)
        self.line_number = 0
        self.first_read()
        self.second_read()

    def read_file(self, file_name):
        """
        reads a file given by the user and parses every line into the
        data structure
        :param file_name: the name of the file
        :return: none
        """
        fh = open(file_name)
        for line in fh:

            # splits the comments off
            line = line.split('//')[0]

            # checks that we have something to write in from the line
            if line != '' and line[0] != '\n':

                # gets rid of the new space and replaces the whitespace
                line = line.rstrip()
                line = line.replace(" ", "")

                # gets rid of bad comments
                self.line_list.append(line.split('//')[0])
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
        self.line_number += 1
        self.current_command = self.line_list[self.line_number - 1]

    def command_type(self):
        """
        gets the type of command this line is
        :return: what type of line it is
        """
        if self.current_command[0] == '(':
            return LINE_COMMAND
        elif self.current_command[0] == '@':
            return ADDRESS_COMMAND
        else:
            return CONTROL_COMMAND

    def symbol(self):
        """
        gets the value from the symbol
        :return: the symbol value
        """

        c_type = self.command_type()

        if c_type == ADDRESS_COMMAND:
            return self.current_command[1:]
        elif c_type == LINE_COMMAND:
            return self.current_command[1:len(self.current_command) - 1]

    def dest(self):
        """
        gets the destination in string form
        :return: the destination
        """

        if self.command_type() == CONTROL_COMMAND:

            if '=' in self.current_command:
                return Code.dest(self.current_command.split('=')[0])
            else:
                return Code.dest("")

    def jump(self):
        """
        gets where to jump to afterwards
        :return:
        """

        if self.command_type() == CONTROL_COMMAND:
            if ";" in self.current_command:
                return Code.jump(self.current_command.split(';')[1])
            else:
                return Code.jump("")

    def comp(self):
        """
        gets the command
        :return: the command in binary form
        """

        comp_command = self.current_command.split(';')[0]

        if '=' in comp_command:
            comp_command = comp_command.split('=')[1]

        return Code.comp(comp_command)

    def get_binary(self):
        """
        print the binary version of a line
        :return: none
        """

        if self.command_type() == CONTROL_COMMAND:

            if ">>" in self.current_command or "<<" in self.current_command:
                return "101" + self.comp() + self.dest() + self.jump()
            else:
                return "111" + self.comp() + self.dest() + self.jump()
        else:
            if self.Table.contains(self.symbol()):
                return bin(int(self.Table.get_address(self.symbol())))[2:].zfill(16)
            elif self.symbol().isdigit():
                return bin(int(self.symbol()))[2:].zfill(16)

    def first_read(self):

        line_counter = -1
        new_list = []

        while self.has_more_commands():
            self.advance()

            # checks if we are dealing with an a or
            if self.command_type() == LINE_COMMAND:
                if self.Table.contains(self.symbol()) is False:
                    self.Table.add_entry(self.symbol(), line_counter + 1)
            else:
                line_counter += 1
                new_list.append(self.current_command)

        # resets a the values
        self.line_number = 0
        self.line_list = new_list

    def second_read(self):

        current_free_location = FIRST_FREE_MEMORY_LOCATION

        while self.has_more_commands():
            self.advance()

            # checks if we are dealing with an a or
            if self.command_type() == ADDRESS_COMMAND:
                if self.Table.contains(self.symbol()) is False and\
                        self.symbol().isdigit() is False:
                    self.Table.add_entry(self.symbol(), current_free_location)
                    current_free_location += 1

        # resets a the values
        self.line_number = 0
