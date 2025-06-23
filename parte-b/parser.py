class Parser:
    def __init__(self):
        self.stack = []
        self.tokens = []
        self.current_token_index = 0
        self.errors = []
        self.table = self._build_parsing_table()

    def _build_parsing_table(self):
        return {
            # MAIN
            ('MAIN', 'DEF'): ['FLIST'],
            ('MAIN', 'INT'): ['STMT'],
            ('MAIN', 'ID'): ['STMT'],
            ('MAIN', 'PRINT'): ['STMT'],
            ('MAIN', 'RETURN'): ['STMT'],
            ('MAIN', 'IF'): ['STMT'],
            ('MAIN', 'LBRACE'): ['STMT'],
            ('MAIN', 'SEMI'): ['STMT'],
            ('MAIN', '$'): [],  # ε

            # FLIST
            ('FLIST', 'DEF'): ['FDEF', 'FLTAIL'],

            # FLTAIL
            ('FLTAIL', 'DEF'): ['FDEF', 'FLTAIL'],
            ('FLTAIL', '$'): [],

            # FDEF
            ('FDEF', 'DEF'): ['DEF', 'ID', 'LPAREN', 'PARLIST', 'RPAREN', 'LBRACE', 'STMTLIST', 'RBRACE'],

            # PARLIST
            ('PARLIST', 'INT'): ['INT', 'ID', 'PARTAIL'],
            ('PARLIST', 'RPAREN'): [],

            # PARTAIL
            ('PARTAIL', 'COMMA'): ['COMMA', 'INT', 'ID', 'PARTAIL'],
            ('PARTAIL', 'RPAREN'): [],

            # VARLIST
            ('VARLIST', 'ID'): ['ID', 'VARTAIL'],

            # VARTAIL
            ('VARTAIL', 'COMMA'): ['COMMA', 'ID', 'VARTAIL'],
            ('VARTAIL', 'SEMI'): [],

            # STMT
            ('STMT', 'INT'): ['INT', 'VARLIST', 'SEMI'],
            ('STMT', 'ID'): ['ATRIBST', 'SEMI'],
            ('STMT', 'PRINT'): ['PRINTST', 'SEMI'],
            ('STMT', 'RETURN'): ['RETURNST', 'SEMI'],
            ('STMT', 'IF'): ['IFSTMT'],
            ('STMT', 'LBRACE'): ['LBRACE', 'STMTLIST', 'RBRACE'],
            ('STMT', 'SEMI'): ['SEMI'],

            # ATRIBST
            ('ATRIBST', 'ID'): ['ID', 'ASSIGN', 'EXPR'],

            # FCALL
            ('FCALL', 'ID'): ['ID', 'LPAREN', 'PARLISTCALL', 'RPAREN'],

            # PARLISTCALL
            ('PARLISTCALL', 'ID'): ['ID', 'ARGTail'],
            ('PARLISTCALL', 'RPAREN'): [],

            # ARGTail
            ('ARGTail', 'COMMA'): ['COMMA', 'ID', 'ARGTail'],
            ('ARGTail', 'RPAREN'): [],

            # PRINTST
            ('PRINTST', 'PRINT'): ['PRINT', 'EXPR'],

            # RETURNST
            ('RETURNST', 'RETURN'): ['RETURN', 'RETVAL'],

            # RETVAL
            ('RETVAL', 'ID'): ['ID'],
            ('RETVAL', 'SEMI'): [],

            # IFSTMT
            ('IFSTMT', 'IF'): ['IF', 'LPAREN', 'EXPR', 'RPAREN', 'LBRACE', 'STMTLIST', 'RBRACE', 'ELSEPART'],

            # ELSEPART
            ('ELSEPART', 'ELSE'): ['ELSE', 'LBRACE', 'STMTLIST', 'RBRACE'],
            ('ELSEPART', '$'): [],  # ou follow de IFSTMT

            # STMTLIST
            ('STMTLIST', 'INT'): ['STMT', 'STMTTAIL'],
            ('STMTLIST', 'ID'): ['STMT', 'STMTTAIL'],
            ('STMTLIST', 'PRINT'): ['STMT', 'STMTTAIL'],
            ('STMTLIST', 'RETURN'): ['STMT', 'STMTTAIL'],
            ('STMTLIST', 'IF'): ['STMT', 'STMTTAIL'],
            ('STMTLIST', 'LBRACE'): ['STMT', 'STMTTAIL'],
            ('STMTLIST', 'SEMI'): ['STMT', 'STMTTAIL'],

            # STMTTAIL
            ('STMTTAIL', 'RBRACE'): [],  # follow
            ('STMTTAIL', 'INT'): ['STMT', 'STMTTAIL'],
            ('STMTTAIL', 'ID'): ['STMT', 'STMTTAIL'],
            ('STMTTAIL', 'PRINT'): ['STMT', 'STMTTAIL'],
            ('STMTTAIL', 'RETURN'): ['STMT', 'STMTTAIL'],
            ('STMTTAIL', 'IF'): ['STMT', 'STMTTAIL'],
            ('STMTTAIL', 'LBRACE'): ['STMT', 'STMTTAIL'],
            ('STMTTAIL', 'SEMI'): ['STMT', 'STMTTAIL'],

            # EXPR
            ('EXPR', 'NUM'): ['NUMEXPR', 'RELTAIL'],
            ('EXPR', 'LPAREN'): ['NUMEXPR', 'RELTAIL'],
            ('EXPR', 'ID'): ['NUMEXPR', 'RELTAIL'],

            # RELTAIL
            ('RELTAIL', 'LT'): ['LT', 'NUMEXPR'],
            ('RELTAIL', 'LE'): ['LE', 'NUMEXPR'],
            ('RELTAIL', 'GT'): ['GT', 'NUMEXPR'],
            ('RELTAIL', 'GE'): ['GE', 'NUMEXPR'],
            ('RELTAIL', 'EQ'): ['EQ', 'NUMEXPR'],
            ('RELTAIL', 'NEQ'): ['NEQ', 'NUMEXPR'],
            ('RELTAIL', 'SEMI'): [],  # follow
            ('RELTAIL', 'RPAREN'): [],

            # NUMEXPR
            ('NUMEXPR', 'NUM'): ['TERM', 'ADDTAIL'],
            ('NUMEXPR', 'LPAREN'): ['TERM', 'ADDTAIL'],
            ('NUMEXPR', 'ID'): ['TERM', 'ADDTAIL'],

            # ADDTAIL
            ('ADDTAIL', 'PLUS'): ['PLUS', 'TERM', 'ADDTAIL'],
            ('ADDTAIL', 'MINUS'): ['MINUS', 'TERM', 'ADDTAIL'],
            ('ADDTAIL', 'SEMI'): [],
            ('ADDTAIL', 'RPAREN'): [],
            ('ADDTAIL', 'LT'): [],
            ('ADDTAIL', 'LE'): [],
            ('ADDTAIL', 'GT'): [],
            ('ADDTAIL', 'GE'): [],
            ('ADDTAIL', 'EQ'): [],
            ('ADDTAIL', 'NEQ'): [],

            # TERM
            ('TERM', 'NUM'): ['FACTOR', 'MULTTAIL'],
            ('TERM', 'LPAREN'): ['FACTOR', 'MULTTAIL'],
            ('TERM', 'ID'): ['FACTOR', 'MULTTAIL'],

            # MULTTAIL
            ('MULTTAIL', 'TIMES'): ['TIMES', 'FACTOR', 'MULTTAIL'],
            ('MULTTAIL', 'DIVIDE'): ['DIVIDE', 'FACTOR', 'MULTTAIL'],
            ('MULTTAIL', 'PLUS'): [],
            ('MULTTAIL', 'MINUS'): [],
            ('MULTTAIL', 'SEMI'): [],
            ('MULTTAIL', 'RPAREN'): [],
            ('MULTTAIL', 'LT'): [],
            ('MULTTAIL', 'LE'): [],
            ('MULTTAIL', 'GT'): [],
            ('MULTTAIL', 'GE'): [],
            ('MULTTAIL', 'EQ'): [],
            ('MULTTAIL', 'NEQ'): [],

            # FACTOR
            ('FACTOR', 'NUM'): ['NUM'],
            ('FACTOR', 'LPAREN'): ['LPAREN', 'NUMEXPR', 'RPAREN'],
            ('FACTOR', 'ID'): ['ID'],
        }

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
                    break

            # Terminal: precisa bater com o tipo do token
            elif self.is_terminal(top):
                if current_token and top == current_token.type:
                    self.advance()
                else:
                    encontrado = current_token.type if current_token else 'EOF'
                    self.errors.append(("token_unexpected", top, current_token))
                    break

            # Não-terminal: consulta a tabela LL(1)
            else:
                lookahead = current_token.type if current_token else '$'
                rule = self.table.get((top, lookahead))

                if rule is None:
                    self.errors.append(("no_rule", top, lookahead))
                    break

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
