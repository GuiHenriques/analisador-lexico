# Trabalho de Compiladores - Parte A
# Grupo: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques

from tokens import RelationalOperator, Token, TokenType
from table import SymbolTable
from dfa import relop_dfa, num_dfa, id_dfa

class Lexer:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.input = f.read()
        self.position = 0    # posição atual na string de entrada
        self.line = 1        # contador de linha (1-indexado)
        self.column = 1      # contador de coluna (1-indexado)
        self.symbol_table = SymbolTable()  # inicializa tabela de símbolos (com palavras-chave)

    def next(self):
        """Retorna o próximo caractere da entrada e atualiza a posição, linha e coluna."""
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
        """Retorna o caractere atual sem avançar a posição."""
        if self.position >= len(self.input):
            return None
        return self.input[self.position]

    def scan(self):
        """Analisa a entrada e retorna a lista de tokens reconhecidos."""
        tokens = []
        while True:
            c = self.peek()
            if c is None:
                break  # fim da entrada
            if c.isspace():
                # Ignora espaços em branco (incluindo \n, \t, etc.)
                self.next()
                continue
            # Decide qual token reconhecer com base no próximo caractere
            if c.isalpha():
                tokens.append(self.lex_identifier())
            elif c.isdigit():
                tokens.append(self.lex_number())
            elif c in ['>', '<', '=', '!']:
                tokens.append(self.lex_operator())
            else:
                # Caractere não reconhecido por nenhum token válido
                raise Exception(f"Caractere inválido '{c}' na linha {self.line}, coluna {self.column}")
        return tokens

    def lex_identifier(self):
        """Reconhece um identificador ou palavra-chave a partir da posição atual."""
        start_column = self.column  # marca onde o token começou
        lexeme = ''
        current_state = id_dfa.start_state
        # Percorre o DFA de identificadores enquanto houver transições válidas
        while True:
            c = self.peek()
            if c is None or (current_state, c) not in id_dfa.transition_function:
                break
            lexeme += self.next()  # consome o caractere e adiciona ao lexema
            current_state = id_dfa.transition_function[(current_state, c)]
        # Verifica se terminou em estado de aceitação
        if current_state not in id_dfa.accept_states:
            raise Exception(f"Identificador malformado '{lexeme}' na linha {self.line}, coluna {start_column}")
        # Insere na tabela de símbolos se for um identificador novo (se já existe, pode ser palavra-chave ou duplicata)
        if self.symbol_table.get(lexeme) is None:
            self.symbol_table.insert(lexeme, TokenType.ID)
        # Retorna token do tipo ID (valor armazenado é o próprio lexema do identificador)
        return Token(TokenType.ID, value=lexeme, line=self.line, column=start_column)

    def lex_number(self):
        """Reconhece um número inteiro a partir da posição atual."""
        start_column = self.column
        lexeme = ''
        current_state = num_dfa.start_state
        # Percorre DFA de números enquanto caracteres forem dígitos
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
        """Reconhece um operador relacional (inclusive operadores de dois caracteres)."""
        start_column = self.column
        lexeme = ''
        current_state = relop_dfa.start_state
        # Percorre DFA de operadores relacionais
        while True:
            c = self.peek()
            # Encerra se fim de entrada ou próximo símbolo não tiver transição válida
            if c is None or (current_state, c) not in relop_dfa.transition_function:
                break
            lexeme += self.next()
            current_state = relop_dfa.transition_function[(current_state, c)]
        # Se parou em estado não-final, é um operador inválido/incompleto
        if current_state not in relop_dfa.accept_states:
            raise Exception(f"Operador relacional inválido '{lexeme}' na linha {self.line}, coluna {start_column}")
        # Ajusta estados intermediários para seus correspondentes finais (caso de < ou > não seguidos de '=')
        if current_state == "q1":
            current_state = "q4"   # < sozinho
        elif current_state == "q6":
            current_state = "q8"   # > sozinho
        final_state = current_state
        # Mapeia estado final para o tipo de operador relacional
        if final_state == "q2":
            token_type = RelationalOperator.LE    # <=
        elif final_state == "q3":
            token_type = RelationalOperator.NE    # !=
        elif final_state == "q4":
            token_type = RelationalOperator.LT    # <
        elif final_state == "q5":
            token_type = RelationalOperator.EQ    # =
        elif final_state == "q7":
            token_type = RelationalOperator.GE    # >=
        elif final_state == "q8":
            token_type = RelationalOperator.GT    # >
        else:
            # (Não era para acontecer devido ao check de accept_states acima)
            raise Exception(f"Operador relacional inválido '{lexeme}' na linha {self.line}, coluna {start_column}")
        # Retorna token do tipo de operador relacional identificado
        return Token(token_type, line=self.line, column=start_column)
