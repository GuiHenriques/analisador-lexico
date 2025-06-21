class Parser:
    def __init__(self):
        self.parsing_table = self._build_parsing_table()

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
        stack = ['$', 'MAIN']
        tokens.append('$')
        index = 0

        print(f"{'Stack':<40} {'Input':<40} Action")
        print('-'*100)

        while stack:
            top = stack.pop()
            current_token = tokens[index]

            print(f"{' '.join(stack[::-1]):<40} {' '.join(tokens[index:]):<40} ", end='')

            if top == current_token == '$':
                print("ACCEPT")
                return True

            elif top == current_token:
                print(f"Match terminal '{current_token}'")
                index += 1

            elif top in self._terminals():
                print(f"ERROR: expected '{top}', got '{current_token}'")
                return False

            else:
                production = self.parsing_table.get((top, current_token))

                if production is None:
                    print(f"ERROR: no rule for ({top}, {current_token})")
                    return False
                elif production == []:
                    print(f"Apply {top} ::= ε")
                else:
                    print(f"Apply {top} ::= {' '.join(production)}")
                    for symbol in reversed(production):
                        stack.append(symbol)

        print("Parsing failed.")
        return False

    def _terminals(self):
        return [
            'def', 'int', '{', '}', '(', ')', ';', ',', ':=',
            'id', 'num', 'print', 'return', 'if', 'else',
            '+', '-', '*', '/',
            '<', '<=', '>', '>=', '==', '<>'
        ]
