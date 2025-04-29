class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def insert(self, lexeme, token_type):
        self.symbols[lexeme] = token_type

    def get(self, lexeme):
        return self.symbols.get(lexeme, None)
