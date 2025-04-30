from enum import Enum

# The 3 valid tokens for this lex analyzer
class TokenType(Enum):
    ID = 1
    INTEGER = 2
    OPERATOR = 3
    UNK = 4

class RelationalOperator(Enum):
    GT = 1 # greater than >
    GE = 2 # greater equal >=
    LT = 3 # less than <
    LE = 4 # less equal <=
    EQ = 5 # equal = (it is one equal char bcause here, it is different from the 'assign' =, it means equals to)
    NE = 6 # not equal !=

class Token:
    def __init__(self, token_type, value=None, line=0, column=0):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        if self.value: return f'{self.token_type}:{self.value}'
        return f'{self.token_type}'

