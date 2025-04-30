from tokens import RelationalOperator, Token, TokenType
from table import SymbolTable
from dfa import relop_dfa, num_dfa, id_dfa

class Lexer:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.input = f.read()

        self.position = 0
        self.line = 1
        self.column = 1
        self.symbol_table = SymbolTable()

    def next(self):
        """Retorna o próximo caractere da entrada e atualiza a posição, linha e coluna."""
        if self.position >= len(self.input):
            return None
        c = self.input[self.position]
        self.position += 1

        if c == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return c

    def peek(self):
        """Retorna o caractere atual sem avançar a posição."""
        if self.position >= len(self.input):
            return None
        return self.input[self.position]

    def scan(self):
        """Tokeniza a entrada e retorna uma lista de tokens."""
        tokens = []

        while (c := self.peek()) is not None:
            if c.isspace():
                self.next()
                continue

            if c.isalpha():
                tokens.append(self.lex_identifier())
            elif c.isdigit():
                tokens.append(self.lex_number())
            elif c in ['>', '<', '=', '!']:
                tokens.append(self.lex_operator())
            else:
                tokens.append(self.lex_other())

        return tokens

    def lex_identifier(self):
        start_column = self.column
        lexeme = ''
        current_state = "q9"

        while True:
            c = self.peek()
            if c is None:
                break

            # Testar se o símbolo é válido no DFA
            if (current_state, c) not in id_dfa.transition_function:
                break

            next_lexeme = self.next()
            lexeme += "" if next_lexeme == None else next_lexeme
            current_state = id_dfa.transition_function[(current_state, c)]

        # Quando sai, checar se está num estado de aceitação
        if current_state not in id_dfa.accept_states:
            raise Exception(f"Erro: identificador inválido '{lexeme}' na linha {self.line}, coluna {start_column}")

        # Checa se é palavra-chave
        if self.symbol_table.get(lexeme) is None:
            self.symbol_table.insert(lexeme, TokenType.ID)

        return Token(TokenType.ID, line=self.line, column=start_column)

    def lex_number(self):
        start_column = self.column
        lexeme = ''
        current_state = "q12"

        while True:
            c = self.peek()
            if c is None or (current_state, c) not in num_dfa.transition_function:
                break

            next_lexeme = self.next()
            lexeme += "" if next_lexeme == None else next_lexeme
            current_state = num_dfa.transition_function[(current_state, c)]

        if current_state not in num_dfa.accept_states:
            raise Exception(f"Erro: número inválido '{lexeme}' na linha {self.line}, coluna {start_column}")

        return Token(TokenType.INTEGER, value=int(lexeme), line=self.line, column=start_column)


    def lex_operator(self):
        start_column = self.column
        full_lexeme = ''
        current_state = "q0"

        while True:
            c = self.peek()
            if c is None or (current_state, c) not in relop_dfa.transition_function:
                break

            next_lexeme = self.next()
            full_lexeme += "" if next_lexeme == None else next_lexeme
            current_state = relop_dfa.transition_function[(current_state, c)]

        final_state = current_state

        if final_state == "q2":
            token_type = RelationalOperator.LE
        elif final_state == "q3":
            token_type = RelationalOperator.NE
        elif final_state == "q4":
            token_type = RelationalOperator.LT
        elif final_state == "q5":
            token_type = RelationalOperator.EQ
        elif final_state == "q7":
            token_type = RelationalOperator.GE
        elif final_state == "q8":
            token_type = RelationalOperator.GT
        else:
            raise Exception(f"Erro: operador relacional inválido '{full_lexeme}' na linha {self.line}, coluna {start_column}")

        return Token(token_type, line=self.line, column=start_column)

    def lex_other(self):
        start_column = self.column
        c = self.next()

        return Token(TokenType.UNK, value=c, line=self.line, column=start_column)
