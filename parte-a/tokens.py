# Trabalho de Compiladores - Parte A
# Grupo: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques

from enum import Enum

# Tipos de tokens suportados pelo analisador léxico
class TokenType(Enum):
    ID = 1
    INTEGER = 2
    OPERATOR = 3

class RelationalOperator(Enum):
    GT = 1   # >
    GE = 2   # >=
    LT = 3   # <
    LE = 4   # <=
    EQ = 5   # =  (igualdade)
    NE = 6   # !=

class Token:
    def __init__(self, token_type, value=None, line=0, column=0):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        if self.value is not None:
            return f'{self.token_type.name}({self.value})'
        return f'{self.token_type.name}'
