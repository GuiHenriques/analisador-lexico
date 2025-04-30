# Trabalho de Compiladores - Parte A
# Grupo: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques

from tokens import RelationalOperator, Token, TokenType
from table import SymbolTable
from dfa import relop_dfa, num_dfa, id_dfa

class Lexer:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.input = f.read()
        self.position = 0    # posicao atual na string de entrada
        self.line = 1        # contador de linha (1-indexado)
        self.column = 1      # contador de coluna (1-indexado)
        self.symbol_table = SymbolTable()  # inicializa tabela de simbolos (com palavras-chave)

    def next(self):
        #Retorna o proximo caractere da entrada e atualiza a posicao, linha e coluna
        if self.position >= len(self.input):
            return None  # EOF
        c = self.input[self.position]
        self.position += 1
        if c == '\n':
            # Nova linha: incrementa contador de linha e reseta coluna
            self.line += 1
            self.column = 1
        else:
            # Caractere comum: incrementa coluna
            self.column += 1
        return c

    def peek(self):
        #Retorna o caractere atual sem avancar a posicao
        if self.position >= len(self.input):
            return None
        return self.input[self.position]

    def scan(self):
        #Analisa a entrada e retorna a lista de tokens reconhecidos
        tokens = []
        while True:
            c = self.peek()
            if c is None:
                break  # fim da entrada
            if c.isspace():
                # Ignora espacos em branco (incluindo \n, \t, etc.)
                self.next()
                continue
            # Decide qual token reconhecer com base no proximo caractere
            if c.isalpha():
                tokens.append(self.lex_identifier())
            elif c.isdigit():
                tokens.append(self.lex_number())
            elif c in ['>', '<', '=', '!']:
                tokens.append(self.lex_operator())
            else:
                # Caractere nao reconhecido por nenhum token valido
                raise Exception(f"Caractere invalido '{c}' na linha {self.line}, coluna {self.column}")
        return tokens

    def lex_identifier(self):
        #Reconhece um identificador ou palavra-chave a partir da posicao atual
        start_column = self.column  # marca onde o token comecou
        lexeme = ''
        current_state = id_dfa.start_state
        # Percorre o DFA de identificadores enquanto houver transicoes validas
        while True:
            c = self.peek()
            if c is None or (current_state, c) not in id_dfa.transition_function:
                break
            lexeme += self.next()  # consome o caractere e adiciona ao lexema
            current_state = id_dfa.transition_function[(current_state, c)]
        # Verifica se terminou em estado de aceitacao
        if current_state not in id_dfa.accept_states:
            raise Exception(f"Identificador malformado '{lexeme}' na linha {self.line}, coluna {start_column}")
        # Insere na tabela de simbolos se for um identificador novo (se ja existe, pode ser palavra-chave ou duplicata)
        if self.symbol_table.get(lexeme) is None:
            self.symbol_table.insert(lexeme, TokenType.ID)
        # Retorna token do tipo ID (valor armazenado e o proprio lexema do identificador)
        return Token(TokenType.ID, value=lexeme, line=self.line, column=start_column)

    def lex_number(self):
        #Reconhece um numero inteiro a partir da posicao atual
        start_column = self.column
        lexeme = ''
        current_state = num_dfa.start_state
        # Percorre DFA de numeros enquanto caracteres forem digitos
        while True:
            c = self.peek()
            if c is None or (current_state, c) not in num_dfa.transition_function:
                break
            lexeme += self.next()
            current_state = num_dfa.transition_function[(current_state, c)]
        # Verifica estado final
        if current_state not in num_dfa.accept_states:
            raise Exception(f"Número inteiro malformado '{lexeme}' na linha {self.line}, coluna {start_column}")
        # Cria token INTEGER com valor inteiro
        return Token(TokenType.INTEGER, value=int(lexeme), line=self.line, column=start_column)

    def lex_operator(self):
        """Reconhece um operador relacional válido da linguagem: <, <=, >, >=, ==, !="""
        start_column = self.column
        lexeme = ''
        current_state = relop_dfa.start_state

        while True:
            c = self.peek()
            if c is None or (current_state, c) not in relop_dfa.transition_function:
                break
            lexeme += self.next()
            current_state = relop_dfa.transition_function[(current_state, c)]

        if current_state not in relop_dfa.accept_states:
            raise Exception(f"Operador relacional inválido '{lexeme}' na linha {self.line}, coluna {start_column}")

        # Verifica se logo após o lexema reconhecido há outro símbolo relacional
        next_char = self.peek()
        if next_char in relop_dfa.alphabet:
            raise Exception(f"Sequência inválida de operadores relacionais iniciando em '{lexeme + next_char}' na linha {self.line}, coluna {start_column}")

        # Mapeia estado final para o tipo de operador relacional
        if current_state == "q1":
            token_type = RelationalOperator.LT      # <
        elif current_state == "q2":
            token_type = RelationalOperator.GT      # >
        elif current_state == "q5":
            token_type = RelationalOperator.LE      # <=
        elif current_state == "q6":
            token_type = RelationalOperator.GE      # >=
        elif current_state == "q7":
            token_type = RelationalOperator.EQ      # ==
        elif current_state == "q8":
            token_type = RelationalOperator.NE      # !=
        else:
            raise Exception(f"Estado final inesperado '{current_state}' para o lexema '{lexeme}'")

        return Token(token_type, line=self.line, column=start_column)
