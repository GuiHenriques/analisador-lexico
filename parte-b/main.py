# Trabalho de Compiladores - Parte B
# Grupo: Higor Abreu, Giovane Pimentel, Isabela Vill, Guilherme Henriques

import sys
from lexer_ply import Lexer
from parser import Parser

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <arquivo_de_entrada>")
        sys.exit(1)
    caminho_arquivo = sys.argv[1]
    try:
        # Le o conteudo do arquivo de entrada
        with open(caminho_arquivo, 'r') as f:
            codigo = f.read()
    except FileNotFoundError:
        print(f"Erro: arquivo '{caminho_arquivo}' não encontrado.")
        sys.exit(1)

    # Inicializa o analisador lexico e processa o codigo
    lexer = Lexer()
    tokens, errors = lexer.tokenize(codigo)

    if errors:
        print("\nErros léxicos encontrados:")
        for msg in errors:
            print(msg)
        return

    parser = Parser()
    if parser.parse(tokens):
        print("Deu boa!")
    else:
        print("Deu ruim!")


if __name__ == "__main__":
    main()
