

VAR = "VAR"
ARG = "ARG"
FIELD = "FIELD"
STATIC = "STATIC"


class SymbolTable:

    def __init__(self):
        """
        creates a new empty symbol table
        """
        self.class_symbol_table = dict()
        self.subroutine_symbol_table = dict()
        self.counter = {VAR: 0, ARG: 0, FIELD: 0, STATIC: 0}

    def start_subroutine(self):
        """
        starts a new subroutine scope
        :return: None
        """
        self.subroutine_symbol_table.clear()
        self.counter[VAR] = 0
        self.counter[ARG] = 0

    def define(self, name, identifier_type, kind):
        """
        defines a new identifier of a given name and kind, and assigns it
        a running index. static and field identifiers have a class scope, while
        ARG and VAR have a subroutine scope
        :param name: identifier name (string)
        :param identifier_type: identifier type (string)
        :param kind: STATIC/FIELD/ARG/VAR
        :return: None
        """
        identifier_idx = self.counter[kind]
        self.counter[kind] += 1
        # update the relevant symbol table
        if kind == STATIC or kind == FIELD:
            self.class_symbol_table[name] = (identifier_type, kind, identifier_idx)
        else:
            # kind is var or arg
            self.subroutine_symbol_table[name] = (identifier_type, kind, identifier_idx)

    def var_count(self, kind):
        """
        returns the number of variables of the given kind that have already
        been defined in the current scope
        :param kind: static/int/field/arg/var
        :return: int
        """
        return self.counter[kind]

    def kind_of(self, name):
        """
        :param name: identifier name (string)
        :return: the kind of named identifier in the current scope, if identifier
        is unknown in the current scope, returns None
        """
        if name in self.subroutine_symbol_table:
            return self.subroutine_symbol_table[name][1]
        if name in self.class_symbol_table:
            return self.class_symbol_table[name][1]
        return None

    def type_of(self, name):
        """
        :param name: identifier name (string)
        :return: return the type of the named identifier in the current scope
        """
        if name in self.subroutine_symbol_table:
            return self.subroutine_symbol_table[name][0]
        if name in self.class_symbol_table:
            return self.class_symbol_table[name][0]
        return None

    def index_of(self, name):
        """
        :param name: identifier name (string)
        :return: the index assigned to the named identifier
        """
        if name in self.subroutine_symbol_table:
            return self.subroutine_symbol_table[name][2]
        if name in self.class_symbol_table:
            return self.class_symbol_table[name][2]
        return None
