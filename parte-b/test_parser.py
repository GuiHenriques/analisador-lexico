
from lexer_ply import Lexer
from parser import Parser

# =======================
# CASOS DE TESTE VÁLIDOS
# =======================
testes_validos = [
    # Declaração de variáveis
    "int x;",
    "int a, b;",

    # Atribuições com expressão e com chamada de função
    "x = 5;",
    "y = x;",
    "x = 1 + 2 * 3;",
    "x = soma(a, b);",

    # Print
    "print 1;",
    "print x;",

    # Return
    "return x;",
    "return;",

    # If
    "if (1 < 2) { ; }",
    "if (x == y) { int z; } else { print z; }",

    # Bloco de instruções
    "{ int x; x = 5; print x; }",

    # Comando vazio
    ";",

    # Funções
    "def f() { ; }",
    "def soma(int a, int b) { return a; }",
    "def vazio() { int x; print x; return; }"
]

# =========================
# CASOS DE TESTE INVÁLIDOS
# =========================
testes_invalidos = [
    "int;",                    # faltou identificador
    "x = ;",                   # faltou expressão
    "print ;",                 # faltou expressão
    "return 123 456;",         # dois valores no return
    "if (x) x = 1;",           # faltou bloco entre { }
    "x = soma(1, 2;",          # parêntese não fechado
    "def () { ; }",            # nome da função faltando
    "def f(,) { ; }",          # parâmetro vazio
    "def f(int a, int) { ; }", # nome do parâmetro faltando
    "def f(int a) ;"           # faltou o corpo
]

lexer = Lexer()
parser = Parser()

def testar_lista(casos, esperado_valido=True):
    for i, codigo in enumerate(casos, 1):
        tokens, lex_errors = lexer.tokenize(codigo)
        sucesso = False

        if not lex_errors:
            sucesso = parser.parse(tokens)

        if sucesso != esperado_valido:
            print(f"\n❌ Teste {i} {'(esperado VÁLIDO)' if esperado_valido else '(esperado INVÁLIDO)'}")
            print("Código:")
            print(codigo)
            if lex_errors:
                print("Erros léxicos:")
                for e in lex_errors:
                    print("  ", e)
            else:
                print("Erros sintáticos:")
                for e in parser.errors:
                    print("  ", e)

# Testar ambos os grupos
testar_lista(testes_validos, esperado_valido=True)
testar_lista(testes_invalidos, esperado_valido=False)
