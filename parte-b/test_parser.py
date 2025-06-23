
from lexer_ply import Lexer
from parser import Parser

# =======================
# CASOS DE TESTE VÁLIDOS
# =======================
testes_validos = [
    "int x;",
    "int a, b;",
    "x = 5;",
    "y = x;",
    "x = 1 + 2 * 3;",
    "x = soma(a, b);",
    "print 1;",
    "print x;",
    "return x;",
    "return;",
    "if (1 < 2) { ; }",
    "if (x == y) { int z; } else { print z; }",
    "{ int x; x = 5; print x; }",
    ";",
    "def f() { ; }",
    "def soma(int a, int b) { return a; }",
    "def vazio() { int x; print x; return; }"
]

# =========================
# CASOS DE TESTE INVÁLIDOS
# =========================
testes_invalidos = [
    "int ;",
    "x = ;",
    "print ;",
    "return 123 456;",
    "if (x) x = 1;",
    "x = soma(1, 2;",
    "def () { ; }",
    "def f(,) { ; }",
    "def f(int a, int) { ; }",
    "def f(int a) ;"
]

lexer = Lexer()
parser = Parser()

def testar_lista(casos, esperado_valido=True):
    total = len(casos)
    passou = 0
    for i, codigo in enumerate(casos, 1):
        tokens, lex_errors = lexer.tokenize(codigo)
        # sucesso = False

        if not lex_errors:
            sucesso = parser.parse(tokens)

        if sucesso == esperado_valido:
            passou += 1
        else:
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
    print(f"\n✅ {passou} de {total} testes {'válidos' if esperado_valido else 'inválidos'} passaram.")

# Testar ambos os grupos
testar_lista(testes_validos, esperado_valido=True)
testar_lista(testes_invalidos, esperado_valido=False)
