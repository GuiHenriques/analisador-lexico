import sys
from dfa import DFA
from lexer import Lexer

def main():
    # if len(sys.argv) != 2:
    #     print("Usage: python main.py <caminho_do_arquivo>")
    #     sys.exit(1)

    # file_path = sys.argv[1]
    # lexer = Lexer(file_path)

    d0 = DFA(
        states={"q0", "q1", "q2"},
        alphabet={"a", "b"},
        transition_function={
            ("q0", 'a'): 'q0',
            ("q0", 'b'): 'q1',
            ("q1", 'a'): 'q2',
            ("q1", 'b'): 'q1',
            ("q2", 'a'): 'q2',
            ("q2", 'b'): 'q2',
        },
        start_state="q0",
        accept_states={"q0", "q1"}
    )

    print(d0.run("ba"))

    # try:
    #     tokens = lexer.tokenize()
    #     for token in tokens:
    #         print(token)
    #     print("\nTabela de Símbolos:")
    #     print(lexer.symbol_table)
    # except Exception as e:
    #     print(f"Erro: {e}")

if __name__ == "__main__":
    main()

