from parsing_table import build_parsing_table
class Parser:
    def __init__(self):
        self.stack = []
        self.tokens = []
        self.current_token_index = 0
        self.errors = []
        self.table = build_parsing_table()
        self.non_terminals = set(nt for nt, _ in self.table) # conjunto de não-terminais da parsing table

    def parse(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.stack = ['$', 'MAIN']  # símbolo inicial
        self.errors = []

        while self.stack:
            top = self.stack.pop() # consome o topo da pilha
            current_token = self.peek() # obtém o token atual da lista de tokens, mas sem avançar

            # fim: quando acabar a analise, o topo da pilha tem que ser $
            if top == '$':
                if current_token is None: # lista de tokens vazia
                    return True  # aceito
                else:
                    # ainda tem tokens a serem lidos, mas o topo da pilha é $, é erro
                    self.errors.append(("trailing_input", current_token))
                    return False

            # terminal: precisa fazer match com o tipo do token
            elif self.is_terminal(top):
                if current_token and top == current_token.type:
                    self.advance() # avança para o próximo token
                else:
                    # token inesperado recebido
                    self.errors.append(("no_rule", top, f"Linha {current_token.lineno}"))
                    return False

            # non-terminal: consulta a tabela LL(1)
            else:
                lookahead = current_token.type if current_token else '$'
                rule = self.table.get((top, lookahead))

                if rule is None: # regra nao encontrada na parsing_table
                    # não tem regra para o símbolo no topo da pilha com o lookahead atual
                    self.errors.append(("no_rule", top, lookahead, f"Linha {current_token.lineno}"))
                    return False

                # Aplica a produção
                for symbol in reversed(rule): # em ordem inversa, porque é pilha em uma lista do python
                    if symbol != '': # ignora produções vazias
                        self.stack.append(symbol)

        return not self.errors

    def peek(self):
        if self.current_token_index < len(self.tokens): #verifica se o índice atual é válido (não ultrapassa o tamanho da lista de tokens)
            return self.tokens[self.current_token_index] # pega o token atual da lista de tokens
        return None

    def advance(self):
        self.current_token_index += 1

    def is_terminal(self, symbol):
        if symbol == '$':
            return False

        return symbol not in self.non_terminals
