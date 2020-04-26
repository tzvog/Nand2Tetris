from JackTokenizer import *
from SymbolTable import *
from VMWriter import *


OP_LST = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
OP_DICT = {'+': 'ADD', '-': 'SUB', '*': ("Math.multiply", 2),
           '/': ("Math.divide", 2), '&': "AND", '|': "OR", '<': 'LT',
           '>': "GT", '=': "EQ"}
# OP_DICT = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
KEY_WORD_CONST = {'true': ("CONST", 0), 'false': ("CONST", 0), 'null': ("CONST", 0),
                  'this': ("POINTER", 0)}
UNARY_OP = {'-': "NEG", '~': "NOT"}
TYPE_DICT = {'FIELD': 'THIS', STATIC: STATIC, VAR: 'LOCAL', ARG: ARG}


class CompilationEngine:

    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.symbol_table = SymbolTable()
        self.vm_writer = VMWriter(output_file)
        self.current_sub_name = None
        self.class_name = None
        self.func_counter = 0
        self.while_counter = 0
        self.if_counter = 0

        # starts the process
        self.tokenizer.advance()
        self.compile_class()
        self.vm_writer.close()

    def compile_class(self):
        """
        compiles the class function
        :return: none
        """
        # advances a single step to get the class name
        self.tokenizer.advance()
        # set class's name
        self.class_name = self.tokenizer.current_token
        # moves to the symbol {
        self.tokenizer.advance()

        # move to the next symbol and check what it is
        self.tokenizer.advance()

        # compiles class variable
        while KEY_WORDS.get(self.tokenizer.current_token) == STATIC or \
                KEY_WORDS.get(self.tokenizer.current_token) == FIELD:
                    self.compile_class_var_dec()
        # compiles subroutine
        while KEY_WORDS.get(self.tokenizer.current_token) == CONSTRUCTOR or \
                KEY_WORDS.get(self.tokenizer.current_token) == METHOD or \
                KEY_WORDS.get(self.tokenizer.current_token) == FUNCTION:
                    self.compile_sub_routine()
        # we are now at the <symbol> } <symbol> which closes the class

    def compile_class_var_dec(self):
        """
        compiles a var dec
        :return: none
        """
        var_kind = self.tokenizer.key_word()
        # advances the token to the var's type
        self.tokenizer.advance()
        if self.tokenizer.token_type() == KEY_WORD:
            var_type = self.tokenizer.key_word()
        else:
            var_type = self.tokenizer.identifier()
        # advances the token to the var's identifier
        self.tokenizer.advance()
        if self.tokenizer.token_type() == KEY_WORD:
            var_name = self.tokenizer.key_word()
        else:
            var_name = self.tokenizer.identifier()

        # update symbol table
        self.symbol_table.define(var_name, var_type, var_kind)

        # advance to next token, and check if there are more var_names
        self.tokenizer.advance()
        while self.tokenizer.current_token != ";":
            # token is <symbol> , <symbol>
            # advance to var's identifier
            self.tokenizer.advance()
            var_name = self.tokenizer.current_token
            # update symbol table
            self.symbol_table.define(var_name, var_type, var_kind)
            self.tokenizer.advance()

        # the current token is <symbol> ; <symbol>, advance to next
        self.tokenizer.advance()

    def compile_sub_routine(self):
        """
        compiles a single sub routine
        :return: none
        """
        # start new subroutine symbol table
        self.symbol_table.start_subroutine()
        # get subroutine type (method/construction/function)
        sub_type = self.tokenizer.key_word()

        # advances the token to what the subroutine returns
        self.tokenizer.advance()
        # updates the return type
        if self.tokenizer.token_type() == KEY_WORD:
            return_type = self.tokenizer.key_word()
        else:
            return_type = self.tokenizer.identifier()

        # advances the token to <identifier> sub_name <identifier>
        self.tokenizer.advance()
        # update the subroutine name
        subroutine_name = self.tokenizer.identifier()
        self.current_sub_name = subroutine_name

        # advance to <symbol> ( <symbol>
        self.tokenizer.advance()
        # if subroutine is a method, add 'this' to the symbol table as argument 0
        if sub_type == METHOD:
            self.symbol_table.define("this", self.class_name, "ARG")
        # compiles the parameter list
        self.compile_parameter_list()
        # we are at <symbol> ) <symbol>
        # advance to subroutine body, and compile it
        self.tokenizer.advance()
        self.compile_subroutine_body(sub_type)

    def compile_subroutine_body(self, sub_type):
        """
        the method compiles the subroutine body
        :return: none
        """
        # we are at bracket {, advance
        self.tokenizer.advance()

        # compile var dec
        while KEY_WORDS.get(self.tokenizer.current_token) == VAR:
            self.compile_var_dec()

        # write function label
        self.vm_writer.write_function(self.class_name + '.' + self.current_sub_name, self.symbol_table.var_count("VAR"))

        # if is method, update THIS to the object
        if sub_type == METHOD:
            self.vm_writer.write_push(ARG, 0)
            self.vm_writer.write_pop("POINTER", 0)

        # if is constructor, allocate memory, and put in this
        if sub_type == CONSTRUCTOR:
            self.vm_writer.write_push("CONST", self.symbol_table.var_count("FIELD"))
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("POINTER", 0)

        if self.tokenizer.current_token != "}":
            self.compile_statements()

        # we are at bracket }, advance
        self.tokenizer.advance()

    def compile_parameter_list(self):
        """
        compiles a parameter list
        :return: none
        """
        # advance to first parameter
        self.tokenizer.advance()
        # while there are more parameters
        while self.tokenizer.current_token != ')':
            # tests what to put as the type of the object
            if self.tokenizer.token_type() == KEY_WORD:
                var_type = self.tokenizer.key_word()
            else:
                var_type = self.tokenizer.identifier()

            # advance to variables name <identifier> var_name <identifier>
            self.tokenizer.advance()
            var_name = self.tokenizer.identifier()

            # define new variable
            self.symbol_table.define(var_name, var_type, "ARG")

            # gets the next token
            self.tokenizer.advance()

            # advance to next token if we are at ','
            if self.tokenizer.current_token == ",":
                self.tokenizer.advance()

    def compile_var_dec(self):
        """
        compiles a declaration of a variable
        :return: none
        """
        # we are at <keyword> var <keyword>
        # advance to variable type
        self.tokenizer.advance()
        if self.tokenizer.token_type() == KEY_WORD:
            var_type = self.tokenizer.key_word()
        else:
            var_type = self.tokenizer.identifier()

        # advance to the variables name
        self.tokenizer.advance()
        while self.tokenizer.current_token != ';':
            # we are at <identifier> var_name <identifier>
            var_name = self.tokenizer.identifier()
            # define variable in symbol table
            self.symbol_table.define(var_name, var_type, "VAR")
            # advance to next token
            self.tokenizer.advance()
            # tests what to put as the type of the object
            if self.tokenizer.current_token == ",":
                self.tokenizer.advance()
        # we are at <symbol> ; <symbol>
        # advance to next token
        self.tokenizer.advance()

    def compile_statements(self):
        """
        the method compiles statements
        :return: none
        """
        # while there are more statements, deal with each one
        while self.tokenizer.current_token != '}':
            statement_type = self.tokenizer.key_word()
            if statement_type == LET:
                self.compile_let()
            elif statement_type == IF:
                self.compile_if()
            elif statement_type == WHILE:
                self.compile_while()
            elif statement_type == DO:
                self.compile_do()
            elif statement_type == RETURN:
                self.compile_return()

    def compile_do(self):
        """
        the method compiles a do command
        :return: none
        """
        # we are at <keyword> do <keyword>
        # advance to next token <identifier> name_of_func <identifier>
        self.tokenizer.advance()
        func_name = self.tokenizer.identifier()
        self.tokenizer.advance()
        # compile the subroutine call
        self.compile_subroutine_call(func_name)
        # pop the result from the function into temp
        self.vm_writer.write_pop("TEMP", 0)
        # we are at <symbol> ; <symbol>, advance to next token
        self.tokenizer.advance()

    def compile_let(self):
        """
        the method compiles a let statement
        :return: none
        """
        # we are at <keyword> let <keyword>
        # advance to next token (var_name)
        self.tokenizer.advance()
        # we are at <identifier> var_name <identifier>
        var_name = self.tokenizer.identifier()
        # get variable data
        var_index = self.symbol_table.index_of(var_name)
        var_kind = TYPE_DICT.get(self.symbol_table.kind_of(var_name))
        # advance to next token ('[' | '=')
        self.tokenizer.advance()
        is_array = False
        if self.tokenizer.current_token == '[':
            is_array = True
            # push arr
            self.vm_writer.write_push(var_kind, var_index)
            # advance to expression and compile it
            self.tokenizer.advance()
            self.compile_expression()
            # we are at <symbol> ] <symbol>, advance to next token
            self.tokenizer.advance()
            # add the index of array and the expression to get the correct location
            self.vm_writer.write_arithmetic("ADD")
        # we are at <symbol> = <symbol>
        # advance to expression and compile it
        self.tokenizer.advance()
        self.compile_expression()

        # if var is an array
        if is_array:
            self.vm_writer.write_pop("TEMP", 0)
            self.vm_writer.write_pop("POINTER", 1)
            self.vm_writer.write_push("TEMP", 0)
            self.vm_writer.write_pop("THAT", 0)
        # if var is not an array
        else:
            self.vm_writer.write_pop(var_kind, var_index)

        # we are at <symbol> ; <symbol>, advance to next
        self.tokenizer.advance()
        return

    def compile_while(self):
        """
        the method compiles a while statement
        :return: none
        """
        while_counter = str(self.while_counter)
        # update the while counter
        self.while_counter += 1
        # create new label for the start of the while
        self.vm_writer.write_label("While_" + while_counter)
        # we are at <keyword> while <keyword>, advance to next token
        self.tokenizer.advance()
        # we are at <symbol> ( <symbol>, advance to next token
        self.tokenizer.advance()
        self.compile_expression()
        # we are at <symbol> ) <symbol>, advance to next token
        self.tokenizer.advance()
        # negate expression
        self.vm_writer.write_arithmetic("NOT")
        # if condition is not met, go to the end of the while
        self.vm_writer.write_if("End_While_" + while_counter)
        # we are at <symbol> { <symbol>, advance to next token
        self.tokenizer.advance()
        # compile statements
        self.compile_statements()
        # go back to the start of the while
        self.vm_writer.write_goto("While_" + while_counter)
        # create new label for the end of the while
        self.vm_writer.write_label("End_While_" + while_counter)
        # we are at <symbol> } <symbol>, advance to next token
        self.tokenizer.advance()
        return

    def compile_return(self):
        """
        the method compiles a return statement
        :return: none
        """
        # we are at <keyword> return <keyword>, advance to next token
        self.tokenizer.advance()
        if self.tokenizer.current_token != ';':
            self.compile_expression()
        else:
            # if function is void, push const 0 to the stack
            self.vm_writer.write_push("CONST", 0)
        # we are at <symbol> ; <symbol>, advance to next token
        self.tokenizer.advance()
        self.vm_writer.write_return()
        return

    def compile_if(self):
        """
        the method compiles an if statement
        :return: none
        """
        if_count = str(self.if_counter)
        # update if counter
        self.if_counter += 1
        # we are at <keyword> if <keyword>, advance to next token
        self.tokenizer.advance()
        # we are at <symbol> ( <symbol>, advance to next token
        self.tokenizer.advance()
        # compile expression
        self.compile_expression()
        # negate the expression
        self.vm_writer.write_arithmetic("NOT")
        # check if condition is met
        self.vm_writer.write_if("ELSE_" + if_count)
        # we are at <symbol> ) <symbol>, advance to next token
        self.tokenizer.advance()
        # we are at <symbol> { <symbol>, advance to next token
        self.tokenizer.advance()
        self.compile_statements()
        # jump to the end of the if
        self.vm_writer.write_goto("END_IF_" + if_count)
        # we are at <symbol> } <symbol>, advance to next token
        self.tokenizer.advance()
        # create else label (which may be empty)
        self.vm_writer.write_label("ELSE_" + if_count)
        if self.tokenizer.current_token == 'else':
            # we are at <keyword> else <keyword>, advance
            self.tokenizer.advance()
            # we are at <symbol> { <symbol>, advance
            self.tokenizer.advance()
            self.compile_statements()
            # we are at <symbol> } <symbol>, advance
            self.tokenizer.advance()
        # create new label
        self.vm_writer.write_label("END_IF_" + if_count)
        return

    def compile_expression(self):
        """
        the method compiles an expression
        :return:
        """
        # compile the term
        self.compile_term()
        while self.tokenizer.current_token in OP_LST:
            call_math = False
            # we are at <symbol> op <symbol>
            op = OP_DICT.get(self.tokenizer.current_token)
            # check if operator needs to call math
            if self.tokenizer.current_token == '*' or self.tokenizer.current_token == '/':
                call_math = True
            # advance to next term and compile term
            self.tokenizer.advance()
            self.compile_term()
            # output the operator
            if call_math:
                self.vm_writer.write_call(op[0], op[1])
            else:
                self.vm_writer.write_arithmetic(op)
        return

    def compile_term(self):
        """
        the method compiles a term
        :return: none
        """
        token_type = self.tokenizer.token_type()
        if token_type == INT_CONST:
            # push the const int
            self.vm_writer.write_push("CONST", self.tokenizer.int_val())
            self.tokenizer.advance()
        elif token_type == STRING_CONST:
            # write without the ""
            string_val = self.tokenizer.string_val()
            # push the len of the string and call the string constructor
            self.vm_writer.write_push("CONST", len(string_val))
            self.vm_writer.write_call("String.new", 1)
            # update new string
            for char in string_val:
                self.vm_writer.write_push("CONST", ord(char))
                self.vm_writer.write_call("String.appendChar", 2)
            self.tokenizer.advance()
        elif self.tokenizer.current_token in KEY_WORD_CONST:
            segment, idx = KEY_WORD_CONST.get(self.tokenizer.current_token)
            self.vm_writer.write_push(segment, idx)
            if self.tokenizer.current_token == 'true':
                self.vm_writer.write_arithmetic('NOT')
            self.tokenizer.advance()
        elif self.tokenizer.current_token == '(':
            # we are at <symbol> ( <symbol>, advance to next token
            self.tokenizer.advance()
            self.compile_expression()
            # we are at <symbol> ) <symbol>, advance to next token
            self.tokenizer.advance()
        elif self.tokenizer.current_token in UNARY_OP:
            op_command = UNARY_OP.get(self.tokenizer.current_token)
            self.tokenizer.advance()
            self.compile_term()
            self.vm_writer.write_arithmetic(op_command)
        # var/var[expression]/subroutine_call
        else:
            # we are at <identifier> var_name <identifier>
            var_name = self.tokenizer.identifier()
            self.tokenizer.advance()
            # if is var_name[expression]
            if self.tokenizer.current_token == '[':
                var_kind = TYPE_DICT.get(self.symbol_table.kind_of(var_name))
                var_index = self.symbol_table.index_of(var_name)
                # push arr
                self.vm_writer.write_push(var_kind, var_index)
                # we are at <symbol> [ <symbol>, advance to expression and compile it
                self.tokenizer.advance()
                self.compile_expression()
                # add the index of array and the expression to get the correct location
                self.vm_writer.write_arithmetic("ADD")
                # set the that pointer
                self.vm_writer.write_pop("POINTER", 1)
                # push to the stack what is in the arr[i]
                self.vm_writer.write_push("THAT", 0)
                # we are at <symbol> ] <symbol>, advance
                self.tokenizer.advance()
            # if is a subroutine call
            elif self.tokenizer.current_token == '(' or self.tokenizer.current_token == '.':
                self.compile_subroutine_call(var_name)
            else:
                # if is just 'var'
                var_kind = TYPE_DICT.get(self.symbol_table.kind_of(var_name))
                var_index = self.symbol_table.index_of(var_name)
                self.vm_writer.write_push(var_kind, var_index)
        return

    def compile_expression_list(self):
        """
        the method compiles a list of expressions
        :return: amount of arguments in the expression list
        """
        expression_counter = 0
        # check that list is not empty
        if self.tokenizer.current_token != ')':
            expression_counter += 1
            # compile first expression
            self.compile_expression()
            # if there are more expressions, compile them
            while self.tokenizer.current_token == ',':
                expression_counter += 1
                # we are at <symbol> , <symbol>, advance
                self.tokenizer.advance()
                # compile expression
                self.compile_expression()
        return expression_counter

    def compile_subroutine_call(self, identifier):
        """
        the method compiles a subroutine call (not including the subroutine
        first varName
        :return: none
        """
        func_name = self.class_name + "." + identifier
        num_of_arguments = 0
        if self.tokenizer.current_token == '.':
            # change func name to its class name
            if self.symbol_table.type_of(identifier) is not None:
                func_name = self.symbol_table.type_of(identifier)
                # we are at <symbol> . <symbol>, advance
                self.tokenizer.advance()
                # we are at <identifier> sub_name <identifier>
                func_name = func_name + "." + self.tokenizer.identifier()
                self.tokenizer.advance()
                # push the object to the stack
                segment = TYPE_DICT.get(self.symbol_table.kind_of(identifier))
                idx = self.symbol_table.index_of(identifier)
                self.vm_writer.write_push(segment, idx)
                num_of_arguments += 1
            else:
                # we are at <symbol> . <symbol>, advance
                self.tokenizer.advance()
                # we are at <identifier> sub_name <identifier>
                func_name = identifier + "." + self.tokenizer.identifier()
                self.tokenizer.advance()
        else:
            self.vm_writer.write_push("POINTER", 0)
            num_of_arguments += 1
        # we are at <symbol> ( <symbol>, advance
        self.tokenizer.advance()
        num_of_arguments += self.compile_expression_list()
        # we are at <symbol> ) <symbol>, advance
        self.tokenizer.advance()
        self.vm_writer.write_call(func_name, num_of_arguments)
        return
