from parsing_table import build_parsing_table
class Parser:
    def __init__(self):
        self.stack = []
        self.tokens = []
        self.current_token_index = 0
        self.errors = []
        self.table = build_parsing_table()

    def parse(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.stack = ['$', 'MAIN']  # símbolo inicial
        self.errors = []

        while self.stack:
            # print(f"Pilha: {self.stack}")
            top = self.stack.pop()
            current_token = self.peek()

            # Fim da análise com sucesso
            if top == '$':
                if current_token is None or current_token.type == '$':
                    return True  # aceito
                else:
                    self.errors.append(("trailing_input", current_token))
                    return False

            # Terminal: precisa bater com o tipo do token
            elif self.is_terminal(top):
                if current_token and top == current_token.type:
                    self.advance()
                else:
                    encontrado = current_token.type if current_token else 'EOF'
                    self.errors.append(("token_unexpected", top, current_token))
                    return False

            # Não-terminal: consulta a tabela LL(1)
            else:
                lookahead = current_token.type if current_token else '$'
                rule = self.table.get((top, lookahead))

                if rule is None:
                    self.errors.append(("no_rule", top, lookahead))
                    return False

                # Aplica a produção (em ordem inversa, porque é pilha)
                for symbol in reversed(rule):
                    if symbol != '':
                        self.stack.append(symbol)
        
        self.report_errors()

        return not self.errors

    def peek(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def advance(self):
        self.current_token_index += 1

    def is_terminal(self, symbol):
        return symbol not in {nt for (nt, _) in self.table} and symbol != '$'

    def report_errors(self):
        for tipo, *info in self.errors:
            if tipo == "token_unexpected":
                top, token = info
                print(f"Erro: token inesperado '{token.type}', esperava '{top}'")
            elif tipo == "no_rule":
                top, lookahead = info
                print(f"Erro: nenhuma regra para '{top}' com lookahead '{lookahead}'")
            elif tipo == "trailing_input":
                token = info[0]
                print(f"Erro: tokens extras após análise — '{token.value}'")
            self.errors.clear()
