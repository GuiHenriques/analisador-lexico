
from lexer_ply import Lexer
from parser import Parser

entradas = [
    ("int x;", True),
    ("int a, b, c;", True),
    ("def id() { ; }", True),
    ("def id(int x, int y) { int z; }", True),
    ("def soma(int a, int b) { int resultado; if (a < b) { print a; } else { print b; } return resultado; }", True),
    ("int x; x = 1 + 2 * 3;", True),
    ("x = soma(1, 2);", True),
    ("return;", True),
    ("x = 5;", True),

    ("int x", False),
    ("int int;", False),
    ("if (a < b { print a; }", False),
    ("else { print x; }", False),
    ("def f() { def g() { ; } }", False),
    ("x := soma(1, 2, );", False)
]

lexer = Lexer()
parser = Parser()

for i, (codigo, esperado) in enumerate(entradas, 1):
    print(f"\nTeste {i}: {'ESPERADO: VÁLIDO' if esperado else 'ESPERADO: INVÁLIDO'}")
    print("Código:")
    print(codigo)
    tokens, lex_errors = lexer.tokenize(codigo)
    if lex_errors:
        print("Erros léxicos:")
        for e in lex_errors:
            print("  ", e)
        if esperado:
            print("❌ Resultado incorreto: deveria ser válido")
        else:
            print("✅ Rejeitado corretamente (erro léxico)")
        continue

    sucesso = parser.parse(tokens)
    if sucesso == esperado:
        print("✅ Resultado correto")
    else:
        print("❌ Resultado incorreto")
        print("Erros sintáticos:")
        for e in parser.errors:
            print("  ", e)
