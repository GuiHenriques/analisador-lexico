# Trabalho de Compiladores - Parte B
# Grupo: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques

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

    # Lista de nomes de tokens (inclui palavras-chave e simbolos)
    tokens = [
        # Palavras-chave
        'DEF', 'INT', 'IF', 'ELSE', 'RETURN', 'PRINT',
        # Identificador e numero
        'ID', 'NUM',
        # Operadores aritmeticos
        'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN',
        # Operadores relacionais
        'EQ', 'NEQ', 'LT', 'LE', 'GT', 'GE',
        # Separadores e pontuacao
        'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMMA', 'SEMI'
    ]

    # Expressoes regulares para tokens simples (de um caractere ou sequencia fixa)
    t_PLUS   = r'\+'
    t_MINUS  = r'-'
    t_TIMES  = r'\*'
    t_DIVIDE = r'/'
    t_ASSIGN = r'='
    t_EQ     = r'=='
    t_NEQ    = r'!='
    t_LT     = r'<'
    t_LE     = r'<='
    t_GT     = r'>'
    t_GE     = r'>='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_COMMA  = r','
    t_SEMI   = r';'

    # Ignorar espacos em branco e tabulacoes
    t_ignore  = ' \t'

    # Regra para reconhecer identificadores e palavras-chave
    def t_ID(self, t):
        r'[A-Za-z][A-Za-z0-9]*'
        # Verifica se o lexema corresponde a uma palavra reservada
        if t.value in Lexer.reserved:
            t.type = Lexer.reserved[t.value]   # redefine tipo do token para a palavra-chave
        return t

    # Regra para reconhecer numeros inteiros
    def t_NUM(self, t):
        r'\d+'
        t.value = int(t.value)   # converte lexema para valor numerico inteiro
        return t

    # Regra para contar linhas e ajustar posicao de coluna
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        # nao retorna token para nova linha (apenas atualiza contagem de linha)

    # Tratamento de erros lexicos: caractere ilegal
    def t_error(self, t):
        # Calcula a coluna do erro usando posicao atual do lexer
        line = t.lexer.lineno
        # Posicao inicial da linha atual = ultima ocorrencia de '\n' antes de t.lexpos
        last_newline = self.data.rfind('\n', 0, t.lexpos)  
        if last_newline < 0:
            last_newline = -1
        col = (t.lexpos - last_newline)
        # Armazena mensagem de erro com linha, coluna e caractere invalido
        msg = f"Erro lexico na linha {line}, coluna {col}: simbolo invalido '{t.value[0]}'"
        self.errors.append(msg)
        t.lexer.skip(1)  # pula o caractere invalido e continua

    def __init__(self):
        # Constroi o lexer a partir das regras e armazena referencia
        self.lexer = lex.lex(module=self)
        self.data = ""      # conteudo do codigo fonte sera armazenado aqui
        self.errors = []    # lista de mensagens de erro lexico

    def tokenize(self, text):
        """Tokeniza o texto de entrada e retorna lista de tokens e lista de erros."""
        self.data = text
        self.lexer.lineno = 1      # reinicia contagem de linhas
        self.errors = []           # limpa erros anteriores
        self.lexer.input(text)     # fornece o texto de entrada ao lexer

        tokens_list = []           # lista de tokens reconhecidos
        while True:
            tok = self.lexer.token()
            if not tok:
                break  # fim da entrada
            # Formata o token para saida: TIPO: valor (ou apenas TIPO, se token for palavra-chave)
            token_type = tok.type
            token_val  = tok.value
            if token_type in ['DEF','INT','IF','ELSE','RETURN','PRINT']:
                # Tokens de palavra-chave: redundancia entre tipo e lexema, imprime somente tipo
                tokens_list.append(f"{token_type}: {token_val}")
            elif token_type == 'ID':
                tokens_list.append(f"ID: {token_val}")
            elif token_type == 'NUM':
                tokens_list.append(f"NUM: {token_val}")
            else:
                # Demais tokens (operadores e separadores): mostra tipo e simbolo
                tokens_list.append(f"{token_type}: {token_val}")
        return tokens_list, self.errors
