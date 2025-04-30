# Trabalho de Compiladores - Parte A
# Grupo: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques

import sys
from lexer import Lexer

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <arquivo_de_entrada>")
        sys.exit(1)
    file_path = sys.argv[1]
    lexer = Lexer(file_path)
    try:
        tokens = lexer.scan()
        print("Tokens:")
        for token in tokens:
            print(f"  {token}")
        print("\nTabela de Símbolos:")
        print(lexer.symbol_table)
    except Exception as e:
        # Exibe mensagem de erro lexico com localizacao
        print(f"Erro lexico: {e}")

if __name__ == "__main__":
    main()
