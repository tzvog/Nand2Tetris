KEY_WORD = "KEYWORD"
SYMBOL = "SYMBOL"
IDENTIFIER = "IDENTIFIER"
INT_CONST = "INT_CONST"
STRING_CONST = "STRING_CONST"

CLASS = "CLASS"
METHOD = "METHOD"
FUNCTION = "FUNCTION"
CONSTRUCTOR = "CONSTRUCTOR"
INT = "INT"
BOOLEAN = "BOOLEAN"
CHAR = "CHAR"
VOID = "VOID"
VAR = "VAR"
STATIC = "STATIC"
FIELD = "FIELD"
LET = "LET"
DO = "DO"
IF = "IF"
ELSE = "ELSE"
WHILE = "WHILE"
RETURN = "RETURN"
TRUE = "TRUE"
FALSE = "FALSE"
NULL = "NULL"
THIS = "THIS"

KEY_WORDS = {"class": CLASS, "method": METHOD, "function": FUNCTION,
             "constructor": CONSTRUCTOR, "int": INT, "boolean": BOOLEAN,
             "char": CHAR, "void": VOID, "var": VAR, "static": STATIC,
             "field": FIELD, "let": LET, "do": DO, "if": IF, "else": ELSE,
             "while": WHILE, "return": RETURN, "true": TRUE, "false": FALSE,
             "null": NULL, "this": THIS}

SYMBOLS = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
           '-', '*', '/', '&', '&', '|', '<', '>', '=', '~'}


class JackTokenizer:

    def __init__(self, file_name):
        self.tokens = []
        self.parse_file(file_name)
        self.current_token = None
        self.token_counter = 0

    def parse_file(self, file_name):
        """
        parses the file into tokens
        :param file_name: the name of the file to parse
        :return: none
        """

        lines = []

        file = open(file_name)
        in_multi_line_comment = False


        for line in file:

            # cleans the spaces from the ends of the lines
            line = line.strip()

            line = line.split("//")[0]

            if len(line) == 0:
                continue

            # checks if we are in a multi line
            if in_multi_line_comment:
                # stops the multi line if so
                if line[-1] == '/' and line[-2] == '*':
                    in_multi_line_comment = False
                continue

            # checks if we are dealing with a comment on this line
            if line[0] == '/' and len(line) > 1 and line[1] == '*':
                if line[-1] == '/' and line[-2] == '*':
                    continue
                in_multi_line_comment = True
                continue

            lines.append(line)

        # adds spaces for the special characters
        for line_num in range(len(lines)):

            if "\"" in lines[line_num]:

                # sets the base for the sentence to be added
                complete_sentence = ""
                is_word = False

                # goes through every letter
                for letter in lines[line_num]:

                    # changes how we see the next words
                    if letter == '\"':
                        is_word = not is_word

                    if not is_word and letter in SYMBOLS:
                        complete_sentence = complete_sentence + " " + \
                                            letter + " "
                    else:
                        complete_sentence = complete_sentence + letter

                lines[line_num] = complete_sentence
            else:
                for symbol in SYMBOLS:
                    lines[line_num] = lines[line_num].replace(symbol, " " +
                                                              symbol + " ")

        # goes through all the line is the file
        for line in lines:

            # checks if we are dealing with a string inside
            if "\"" in line:

                split_line = line.split("\"", 1)

                # keeps going as long as we have a " in there
                while len(split_line) > 1:

                    # splits it by any white space
                    only_words = split_line[0].split()

                    # adds it all to the tokens
                    for word_index in range(len(only_words)):
                        self.tokens.append(only_words[word_index])

                    # catches the string part
                    string_const = split_line[1].split("\"", 1)[0]

                    # add the string as it is
                    self.tokens.append('\"' + string_const + '\"')

                    # updates the string
                    split_line[1] = split_line[1].split("\"", 1)[1]

                    # gets rid of the part we dont need
                    split_line = split_line[1].split("\"", 1)

                # finishes what is left from the line
                # splits it by any white space
                words_by_space = split_line[0].split()

                # adds it all to the tokens
                for word_index in range(len(words_by_space)):
                    self.tokens.append(words_by_space[word_index])
            else:
                # splits it by any white space
                words_by_space = line.split()

                # adds it all to the tokens
                for word_index in range(len(words_by_space)):
                    self.tokens.append(words_by_space[word_index])

    def has_more_tokens(self):
        """
        checks if we have another token to explore
        :return: if we have more tokens to explore
        """

        return self.token_counter < len(self.tokens)

    def advance(self):
        """
        gets the next token to parse
        :return: none
        """

        # checks if we have another token to parse
        if self.has_more_tokens():

            # gets the next token to parse and updates the counter
            self.current_token = self.tokens[self.token_counter]
            self.token_counter += 1

    def token_type(self):
        """
        gets the type of the token
        :return: the type of the token
        """

        # checks what type of token we are dealing with
        if self.current_token in KEY_WORDS:
            return KEY_WORD
        elif self.current_token in SYMBOLS:
            return SYMBOL
        elif self.current_token.isdigit():
            return INT_CONST
        elif self.current_token[0] == '"':
            return STRING_CONST
        else:
            return IDENTIFIER

    def symbol(self):
        """
        gets the symbol
        :return: the symbol
        """

        if self.token_type() == SYMBOL:
            return self.current_token

    def identifier(self):
        """
        gets the identifier
        :return: returns the identifier
        """

        if self.token_type() == IDENTIFIER:
            return self.current_token

    def int_val(self):
        """
        gets the int value of the token
        :return: the token in int value
        """

        if self.token_type() == INT_CONST:

            if '.' in self.current_token:
                return float(self.current_token)
            else:
                return int(self.current_token)

    def string_val(self):
        """
        gets the value of the string
        :return:  the value of the string without the qoutes
        """

        # checks if we our token type if a string
        if self.token_type() == STRING_CONST:

            # cuts off the edges
            return self.current_token[1:-1]

    def key_word(self):
        """
        gets the keyword from the dictionary
        :return: the keyword val
        """

        if self.token_type() == KEY_WORD:
            return KEY_WORDS.get(self.current_token)
