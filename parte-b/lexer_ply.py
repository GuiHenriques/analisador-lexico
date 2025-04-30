"""
Analisador Léxico para a linguagem LSI-2025-1 utilizando PLY.
Integrantes: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques
Descrição:
    - Reconhece palavras-chave, identificadores, números inteiros, operadores 
      aritméticos/relacionais e separadores conforme a gramática da linguagem.
    - Imprime a lista de tokens na ordem de aparecimento.
    - Assinala erros léxicos indicando linha e coluna.
"""
import ply.lex as lex

class Lexer:
    # Palavras reservadas da linguagem mapeadas para tokens
    reserved = {
        'def': 'DEF',
        'int': 'INT',
        'if': 'IF',
        'else': 'ELSE',
        'return': 'RETURN',
        'print': 'PRINT'
    }

    # Lista de nomes de tokens (inclui palavras-chave e símbolos)
    tokens = [
        # Palavras-chave
        'DEF', 'INT', 'IF', 'ELSE', 'RETURN', 'PRINT',
        # Identificador e número
        'ID', 'NUM',
        # Operadores aritméticos
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
        # Operadores relacionais
        'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',
        # Separadores e pontuação
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMI'
    ]

    # Expressões regulares para tokens simples (de um caractere ou sequência fixa)
    t_PLUS   = r'\+'
    t_MINUS  = r'-'
    t_TIMES  = r'\*'
    t_DIVIDE = r'/'
    t_ASSIGN = r'='      # operador de atribuição
    t_EQ     = r'=='     # igual (relacional)
    t_NEQ    = r'!='     # diferente (relacional)
    t_LT     = r'<'      # menor que
    t_LE     = r'<='     # menor ou igual
    t_GT     = r'>'      # maior que
    t_GE     = r'>='     # maior ou igual
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA  = r','
    t_SEMI   = r';'

    # Ignorar espaços em branco e tabulações
    t_ignore  = ' \t'

    # Regra para reconhecer identificadores e palavras-chave
    def t_ID(self, t):
        r'[A-Za-z][A-Za-z0-9]*'
        # Verifica se o lexema corresponde a uma palavra reservada
        if t.value in Lexer.reserved:
            t.type = Lexer.reserved[t.value]   # redefine tipo do token para a palavra-chave
        return t

    # Regra para reconhecer números inteiros
    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)   # converte lexema para valor numérico inteiro
        return t

    # Regra para contar linhas e ajustar posição de coluna
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        # Não retorna token para nova linha (apenas atualiza contagem de linha)

    # Tratamento de erros léxicos: caractere ilegal
    def t_error(self, t):
        # Calcula a coluna do erro usando posição atual do lexer
        line = t.lexer.lineno
        # Posição inicial da linha atual = última ocorrência de '\n' antes de t.lexpos
        last_newline = self.data.rfind('\n', 0, t.lexpos)  
        if last_newline < 0:
            last_newline = -1
        col = (t.lexpos - last_newline)
        # Armazena mensagem de erro com linha, coluna e caractere inválido
        msg = f"Erro léxico na linha {line}, coluna {col}: símbolo inválido '{t.value[0]}'"
        self.errors.append(msg)
        t.lexer.skip(1)  # pula o caractere inválido e continua

    def __init__(self):
        # Constrói o lexer a partir das regras e armazena referência
        self.lexer = lex.lex(module=self)
        self.data = ""      # conteúdo do código fonte será armazenado aqui
        self.errors = []    # lista de mensagens de erro léxico

    def tokenize(self, text):
        """Tokeniza o texto de entrada e retorna lista de tokens e lista de erros."""
        self.data = text
        self.lexer.lineno = 1      # reinicia contagem de linhas
        self.errors = []           # limpa erros anteriores
        self.lexer.input(text)     # fornece o texto de entrada ao lexer

        tokens_list = []           # lista de tokens reconhecidos (como strings formatadas)
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # fim da entrada
            # Formata o token para saída: TIPO: valor (ou apenas TIPO, se token for palavra-chave)
            token_type = tok.type
            token_val  = tok.value
            if token_type in ['DEF','INT','IF','ELSE','RETURN','PRINT']:
                # Tokens de palavra-chave: redundância entre tipo e lexema, imprime somente tipo
                tokens_list.append(f"{token_type}: {token_val}")
            elif token_type == 'ID':
                tokens_list.append(f"ID: {token_val}")
            elif token_type == 'NUM':
                tokens_list.append(f"NUM: {token_val}")
            else:
                # Demais tokens (operadores e separadores): mostra tipo e símbolo
                tokens_list.append(f"{token_type}: {token_val}")
        return tokens_list, self.errors
