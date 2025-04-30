import sys
from dfa import DFA
from lexer import Lexer

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <caminho_do_arquivo>")
        sys.exit(1)

    file_path = sys.argv[1]
    lexer = Lexer(file_path)

    try:
        tokens = lexer.scan()
        for token in tokens:
            print(token)
        print("\nTabela de Símbolos:")
        print(lexer.symbol_table)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()

