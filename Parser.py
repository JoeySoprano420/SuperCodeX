class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.next_token()
    
    def parse(self):
        program = []
        while self.current_token:
            if self.current_token[0] == 'KEYWORD':
                if self.current_token[1] == 'DEFINE':
                    program.append(self.parse_define())
                elif self.current_token[1] == 'SPAWN_PARALLEL':
                    program.append(self.parse_spawn_parallel())
                else:
                    raise SyntaxError(f"Unknown keyword {self.current_token[1]}")
            self.current_token = self.lexer.next_token()
        return program

    def parse_define(self):
        self.consume('KEYWORD', 'DEFINE')
        func_name = self.consume('IDENTIFIER')
        args = []
        self.consume('PUNCTUATION', '(')
        while self.current_token and self.current_token[0] != 'PUNCTUATION' or self.current_token[1] != ')':
            args.append(self.consume('IDENTIFIER'))
        self.consume('PUNCTUATION', ')')
        body = self.parse_statements()
        return ('DEFINE', func_name[1], args, body)
    
    def parse_statements(self):
        statements = []
        while self.current_token and self.current_token[0] != 'KEYWORD':
            statements.append(self.parse_statement())
        return statements
    
    def parse_statement(self):
        if self.current_token[0] == 'KEYWORD' and self.current_token[1] == 'EXIT':
            self.consume('KEYWORD', 'EXIT')
            return ('EXIT',)
    
    def consume(self, expected_type, expected_value=None):
        if self.current_token and self.current_token[0] == expected_type:
            if expected_value and self.current_token[1] != expected_value:
                raise SyntaxError(f"Expected {expected_value}, got {self.current_token[1]}")
            token = self.current_token
            self.current_token = self.lexer.next_token()
            return token
        else:
            raise SyntaxError(f"Expected {expected_type}, got {self.current_token}")
