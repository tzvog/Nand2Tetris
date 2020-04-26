
COMMAND_DIC = {"ADD": "add", "SUB": "sub", "NEG": "neg", "EQ": "eq", "GT": "gt",
               "LT": "lt", "AND": "and", "OR": "or", "NOT": "not"}

SEGMENT_DICT = {"CONST": "constant", "ARG": "argument", "LOCAL": "local",
                "STATIC": "static", "THIS": "this", "THAT": "that",
                "POINTER": "pointer", "TEMP": "temp"}


class VMWriter:

    def __init__(self, output_file_name):
        """
        creates a new file and prepares it for writing
        :param output_file_name: the name of the output file
        """
        self.output_file = open(output_file_name, 'w')

    def write_push(self, segment, index):
        """
        writes a VM push command
        :param segment: CONST/ARG/LOCAL/STATIC/THIS/THAT/POINTER/TEMP
        :param index: int
        :return: None
        """
        self.output_file.write("push " + SEGMENT_DICT[segment] + " " + str(index) + "\n")

    def write_pop(self, segment, index):
        """
        writes a VM pop command
        :param segment: CONST/ARG/LOCAL/STATIC/THIS/THAT/POINTER/TEMP
        :param index: int
        :return: None
        """
        self.output_file.write("pop " + SEGMENT_DICT[segment] + " " + str(index) + "\n")

    def write_arithmetic(self, command):
        """
        writes a VM arithmetic command
        :param command: ADD/SUB/NEG/EQ/GT/LT/AND/OR/NOT
        :return: None
        """
        self.output_file.write(COMMAND_DIC[command] + "\n")

    def write_label(self, label):
        """
        writes a VM arithmetic command
        :param label: the name of the label (string)
        :return: none
        """
        self.output_file.write("label " + label + "\n")

    def write_goto(self, label):
        """
        writes a VM goto command
        :param label: the name of the label (string)
        :return: none
        """
        self.output_file.write("goto " + label + "\n")

    def write_if(self, label):
        """
        writes a VM if-goto command
        :param label: the name of the label (string)
        :return: none
        """
        self.output_file.write("if-goto " + label + "\n")

    def write_call(self, name, n_args):
        """
        writes a VM call command
        :param name: subroutine name (string)
        :param n_args: amount of arguments (int)
        :return: none
        """
        self.output_file.write("call " + name + " " + str(n_args) + "\n")

    def write_function(self, name, n_locals):
        """
        writes a VM function command
        :param name: the name of subroutine (string)
        :param n_locals: amount of local arguments (int)
        :return: none
        """
        self.output_file.write("function " + name + " " + str(n_locals) + "\n")

    def write_return(self):
        """
        writes a VM return command
        :return: none
        """
        self.output_file.write("return\n")

    def close(self):
        """
        closes the output file
        :return: none
        """
        self.output_file.close()
