class SymbolTable:

    def __init__(self):

        self.symbols_dict = {
            "SP": "0",
            "LCL": "1",
            "ARG": "2",
            "THIS": "3",
            "THAT": "4",
            "SCREEN": "16384",
            "KBD": "24567",
            "R0": "0",
            "R1": "1",
            "R2": "2",
            "R3": "3",
            "R4": "4",
            "R5": "5",
            "R6": "6",
            "R7": "7",
            "R8": "8",
            "R9": "9",
            "R10": "10",
            "R11": "11",
            "R12": "12",
            "R13": "13",
            "R14": "14",
            "R15": "15",
        }

    def add_entry(self, symbol, address):
        """
        adds an address to the dictionary
        :param symbol: the symbol to add to the dictionary
        :param address: the address to add in the dictionary
        :return:
        """
        self.symbols_dict[symbol] = str(address)

    def contains(self, symbol):
        """
        checks if it contains wanted key
        :return: if the symbol is found
        """

        if symbol in self.symbols_dict:
            return True
        return False

    def get_address(self, symbol):
        """
        gets the address of a certain symbol
        :param symbol: the symbol we are looking for
        :return: the address
        """
        return self.symbols_dict.get(symbol)
