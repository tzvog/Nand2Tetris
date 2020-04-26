from JackTokenizer import *

XML_CLASS = "class"
XML_CLASS_VAR_DEC = "classVarDec"
XML_SUBROUTINE_DEC = "subroutineDec"
XML_PARAMETER_LIST = "parameterList"
XML_SUBROUTINE_BODY = "subroutineBody"
XML_VAR_DEC = "varDec"
XML_STATEMENTS = "statements"
XML_WHILE_STATEMENT = "whileStatement"
XML_IF_STATEMENT = "ifStatement"
XML_RETURN_STATEMENT = "returnStatement"
XML_LET_STATEMENT = "letStatement"
XML_DO_STATEMENT = "doStatement"
XML_EXPRESSION = "expression"
XML_TERM = "term"
XML_EXPRESSION_LIST = "expressionList"
XML_KEY_WORD = "keyword"
XML_IDENTIFIER = "identifier"
XML_SYMBOL = "symbol"
XML_STRING_CONST = "stringConstant"
XML_INT_CONST = "integerConstant"

OP_LST = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
OP_DICT = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}
KEY_WORD_CONST = {'true', 'false', 'null', 'this'}
UNARY_OP = {'-', '~'}


class CompilationEngine:

    def __init__(self, input_file, output_file):
        self.tokenizer = JackTokenizer(input_file)
        self.xml_file = open(output_file, "w")
        self.space_depth = 0

        # starts the process
        self.tokenizer.advance()
        self.compile_class()
        self.xml_file.close()

    def compile_class(self):
        """
        compiles the class function
        :return: none
        """
        # write <class>
        self.non_terminal_open(XML_CLASS)
        # write <keyword> class <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        # advances a single step to get the class name
        self.tokenizer.advance()
        # write <identifier> class_name <identifier>
        self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
        # moves for the symbol
        self.tokenizer.advance()
        # write <symbol> { <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
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
        # write <symbol> } <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        # write <class>
        self.non_terminal_end(XML_CLASS)

    def non_terminal_end(self, xml_type):
        """
        closes a non terminal function
        :param xml_type: the xml type we are working with
        :return: none
        """
        self.space_depth -= 1
        self.write_line(self.terminal_end(xml_type))

    def non_terminal_open(self, xml_type):
        """
        an opening for a non terminal
        :param xml_type: the xml type
        :return: none
        """
        self.write_line(self.terminal_opening(xml_type) + "\n")
        self.space_depth += 1

    def terminal_opening(self, word):
        """
        makes the word a starts of a function
        :param word: the word to make a start
        :return: the word as a start
        """

        return "<" + word + ">"

    def terminal_end(self, word):
        """
        makes the word a start and end
        :param word: the word to work with
        :return: the word as an end
        """

        return "</" + word + ">\n"

    def write_line(self, word):
        """
        writes the line to the file with the correct depth
        :param word: the word we are writing
        :return: none
        """

        self.xml_file.write("\t" * self.space_depth + word)

    def one_liner(self, xml_type, token):
        """
        writes the one liner function
        :param xml_type: the type
        :param token: thw token to put in the xml
        :return:
        """

        self.write_line(self.terminal_opening(xml_type) + " " + token + " "
                        + self.terminal_end(xml_type))

    def compile_class_var_dec(self):
        """
        compiles a var dec
        :return: none
        """
        # write <class_var_dict>
        self.non_terminal_open(XML_CLASS_VAR_DEC)
        # write <keyword> static/field <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        # advances the token
        self.tokenizer.advance()
        # tests what to put as the type of the object
        if self.tokenizer.token_type() == KEY_WORD:
            self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        else:
            self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
        self.tokenizer.advance()
        # write <identifier> var_name <identifier>
        self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
        self.tokenizer.advance()

        # check if there are more var_names
        while self.tokenizer.current_token != ";":
            # write <symbol> , <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
            # write <identifier> var_name <identifier>
            self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
            self.tokenizer.advance()

        # write <symbol> ; <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        # closes the statement
        self.non_terminal_end(XML_CLASS_VAR_DEC)
        self.tokenizer.advance()

    def compile_sub_routine(self):
        """
        compiles a single sub routine
        :return: none
        """
        # writes <subroutine_dec>
        self.non_terminal_open(XML_SUBROUTINE_DEC)
        # write <keyword> function/method/const <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        # advances the token
        self.tokenizer.advance()
        # tests what to put as the type of the object
        if self.tokenizer.token_type() == KEY_WORD:
            self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        else:
            self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
        # advances the token
        self.tokenizer.advance()
        # write <identifier> sub_name <identifier>
        self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
        self.tokenizer.advance()
        # write <symbol> ( <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        # compiles the parameter list
        self.compile_parameter_list()
        # write <symbol> ) <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        # compile subroutine body
        self.compile_subroutine_body()
        # closes the sub routine
        self.non_terminal_end(XML_SUBROUTINE_DEC)

    def compile_subroutine_body(self):
        """
        the method compiles the subroutine body
        :return: none
        """
        # write <sub routine>
        self.non_terminal_open(XML_SUBROUTINE_BODY)

        # opens the bracket {
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()

        # compile var dec
        while KEY_WORDS.get(self.tokenizer.current_token) == VAR:
            self.compile_var_dec()

        if self.tokenizer.current_token != "}":
            self.compile_statements()

        # closes the bracket
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        # closes the sub routine body (write <sub routine>)
        self.non_terminal_end(XML_SUBROUTINE_BODY)

    def compile_parameter_list(self):
        """
        compiles a parameter list
        :return: none
        """
        # writes <parameter_list>
        self.non_terminal_open(XML_PARAMETER_LIST)
        self.tokenizer.advance()

        while self.tokenizer.current_token != ')':
            # tests what to put as the type of the object
            if self.tokenizer.token_type() == KEY_WORD:
                self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
            else:
                self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)

            # gets the variables name
            self.tokenizer.advance()
            # write <identifier> var_name <identifier>
            self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)

            # gets the next token
            self.tokenizer.advance()

            # tests what to put as the type of the object
            if self.tokenizer.current_token == ",":
                self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
                self.tokenizer.advance()

        # closes the statement
        self.non_terminal_end(XML_PARAMETER_LIST)

    def compile_var_dec(self):
        """
        compiles a declaration of a variable
        :return: none
        """
        # writes the opening
        self.non_terminal_open(XML_VAR_DEC)
        # write <keyword> var <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        # tests what to put as the type of the object
        self.tokenizer.advance()
        if self.tokenizer.token_type() == KEY_WORD:
            self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        else:
            self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
        # gets the variables name
        self.tokenizer.advance()
        while self.tokenizer.current_token != ';':
            # writes <identifier> var_name <identifier>
            self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
            # gets the next token
            self.tokenizer.advance()
            # tests what to put as the type of the object
            if self.tokenizer.current_token == ",":
                self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
                self.tokenizer.advance()
        # writes <symbol> ; <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        # closes the statement
        self.non_terminal_end(XML_VAR_DEC)

    def compile_statements(self):
        """
        the method compiles statements
        :return: none
        """
        # write <statements>
        self.non_terminal_open(XML_STATEMENTS)
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
        # write <statements>
        self.non_terminal_end(XML_STATEMENTS)

    def compile_do(self):
        """
        the method compiles a do command
        :return: none
        """
        # write <do_statement>
        self.non_terminal_open(XML_DO_STATEMENT)
        # write <keyword> do <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        # advance to next token (subroutine call)
        self.tokenizer.advance()
        # write <identifier> name_of_func <identifier>
        self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
        self.tokenizer.advance()
        # compile the subroutine call
        self.compile_subroutine_call()
        # write <symbol> ; <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        # write <do_statement>
        self.non_terminal_end(XML_DO_STATEMENT)
        self.tokenizer.advance()

    def compile_let(self):
        """
        the method compiles a let statement
        :return: none
        """
        # write <let_statement>
        self.non_terminal_open(XML_LET_STATEMENT)
        # write <keyword> let <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        # advance to next token (var_name)
        self.tokenizer.advance()
        # write <identifier> var_name <identifier>
        self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
        # advance to next token ('[' | '=')
        self.tokenizer.advance()
        if self.tokenizer.current_token == '[':
            # write <symbol> [ <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            # advance to expression and compile it
            self.tokenizer.advance()
            self.compile_expression()
            # write <symbol> ] <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
        # write <symbol> = <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        # advance to expression and compile it
        self.tokenizer.advance()
        self.compile_expression()
        # write <symbol> ; <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        # write <let_statement>
        self.non_terminal_end(XML_LET_STATEMENT)
        self.tokenizer.advance()
        return

    def compile_while(self):
        """
        the method compiles a while statement
        :return: none
        """
        # write <while_statement>
        self.non_terminal_open(XML_WHILE_STATEMENT)
        # write <keyword> while <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        self.tokenizer.advance()
        # write <symbol> ( <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        self.compile_expression()
        # write <symbol> ) <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        # write <symbol> { <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        self.compile_statements()
        # write <symbol> } <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        # write <while_statement>
        self.non_terminal_end(XML_WHILE_STATEMENT)
        self.tokenizer.advance()
        return

    def compile_return(self):
        """
        the method compiles a return statement
        :return: none
        """
        # write <return_statement>
        self.non_terminal_open(XML_RETURN_STATEMENT)
        # write <keyword> return <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        self.tokenizer.advance()
        if self.tokenizer.current_token != ';':
            self.compile_expression()
        # write <symbol> ; <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        # write <return_statement>
        self.non_terminal_end(XML_RETURN_STATEMENT)
        self.tokenizer.advance()
        return

    def compile_if(self):
        """
        the method compiles an if statement
        :return: none
        """
        # write <if_statement>
        self.non_terminal_open(XML_IF_STATEMENT)
        # write <keyword> if <keyword>
        self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
        self.tokenizer.advance()
        # write <symbol> ( <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        self.compile_expression()
        # write <symbol> ) <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        # write <symbol> { <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        self.compile_statements()
        # write <symbol> } <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        if self.tokenizer.current_token == 'else':
            # write <keyword> else <keyword>
            self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
            self.tokenizer.advance()
            # write <symbol> { <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
            self.compile_statements()
            # write <symbol> } <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
        # write <if_statement>
        self.non_terminal_end(XML_IF_STATEMENT)
        return

    def compile_expression(self):
        """
        the method compiles an expression
        :return:
        """
        # write <expression>
        self.non_terminal_open(XML_EXPRESSION)
        self.compile_term()
        while self.tokenizer.current_token in OP_LST:
            # write <symbol> op <symbol>
            if self.tokenizer.current_token in OP_DICT:
                self.one_liner(XML_SYMBOL, OP_DICT.get(self.tokenizer.current_token))
            else:
                self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
            self.compile_term()
        # write <expression>
        self.non_terminal_end(XML_EXPRESSION)
        return

    def compile_term(self):
        """
        the method compiles a term
        :return: none
        """
        # write <term>
        self.non_terminal_open(XML_TERM)
        token_type = self.tokenizer.token_type()
        if token_type == INT_CONST:
            self.one_liner(XML_INT_CONST, self.tokenizer.current_token)
            self.tokenizer.advance()
        elif token_type == STRING_CONST:
            # write without the ""
            self.one_liner(XML_STRING_CONST, self.tokenizer.current_token[1:-1])
            self.tokenizer.advance()
        elif self.tokenizer.current_token in KEY_WORD_CONST:
            self.one_liner(XML_KEY_WORD, self.tokenizer.current_token)
            self.tokenizer.advance()
        elif self.tokenizer.current_token == '(':
            # write <symbol> ( <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
            self.compile_expression()
            # write <symbol> ) <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
        elif self.tokenizer.current_token in UNARY_OP:
            # write <symbol> unary_op <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
            self.compile_term()
        # var/var[expression]/subroutine_call
        else:
            # write <identifier> var_name <identifier>
            self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
            self.tokenizer.advance()
            # if is var_name[expression]
            if self.tokenizer.current_token == '[':
                # write <symbol> [ <symbol>
                self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
                self.tokenizer.advance()
                self.compile_expression()
                # write <symbol> ] <symbol>
                self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
                self.tokenizer.advance()
            # if is a subroutine call
            elif self.tokenizer.current_token == '(' or self.tokenizer.current_token == '.':
                self.compile_subroutine_call()
            # write <term>
        self.non_terminal_end(XML_TERM)
        return

    def compile_expression_list(self):
        """
        the method compiles a list of expressions
        :return: none
        """
        # write <expression_list>
        self.non_terminal_open(XML_EXPRESSION_LIST)
        # check that list is not empty
        if self.tokenizer.current_token != ')':
            # compile first expression
            self.compile_expression()
            # if there are more expressions, compile them
            while self.tokenizer.current_token == ',':
                # write <symbol> , <symbol>
                self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
                self.tokenizer.advance()
                # compile expression
                self.compile_expression()
        # write <expression_list>
        self.non_terminal_end(XML_EXPRESSION_LIST)
        return

    def compile_subroutine_call(self):
        """
        the method compiles a subroutine call (not including the subroutine
        first varName
        :return: none
        """
        if self.tokenizer.current_token == '.':
            # write <symbol> . <symbol>
            self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
            self.tokenizer.advance()
            # write <identifier> sub_name <identifier>
            self.one_liner(XML_IDENTIFIER, self.tokenizer.current_token)
            self.tokenizer.advance()
        # write <symbol> ( <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        self.compile_expression_list()
        # write <symbol> ) <symbol>
        self.one_liner(XML_SYMBOL, self.tokenizer.current_token)
        self.tokenizer.advance()
        return
