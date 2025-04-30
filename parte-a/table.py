# Trabalho de Compiladores - Parte A
# Grupo: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques

class SymbolTable:
    def __init__(self):
        # Palavras-chave predefinidas já inseridas na tabela
        self.symbols = {
            "int": "KEYWORD",
            "if": "KEYWORD",
            "else": "KEYWORD",
            "def": "KEYWORD",
            "print": "KEYWORD",
            "return": "KEYWORD"
        }

    def insert(self, lexeme, token_type):
        # Armazena o lexema com o nome do tipo (se for Enum, usa atributo name)
        self.symbols[lexeme] = token_type.name if hasattr(token_type, 'name') else str(token_type)

    def get(self, lexeme):
        return self.symbols.get(lexeme, None)

    def __repr__(self):
        # Exibe cada entrada
        return "\n".join(f"{lex} -> {typ}" for lex, typ in self.symbols.items())
