import re
from collections import namedtuple

Token = namedtuple("Token", ["type", "value"])

class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        token_specifications = [
            ('KEYWORD', r'\b(DEFINE|SPAWN_PARALLEL|IF|LOOP|EXIT|CMD_EXEC|RETURN|CALL|DECLARE|ON_EVENT)\b'),
            ('IDENTIFIER', r'\b[A-Za-z_][A-Za-z_0-9]*\b'),
            ('NUMBER', r'\b\d+\b'),
            ('OPERATOR', r'[+\-*/=<>!&|]'),
            ('PUNCTUATION', r'[(),{};]'),
            ('STRING', r'"([^"\\]|\\.)*"'),
            ('WHITESPACE', r'[ \t\n\r]+'),
            ('COMMENT', r'//.*'),
            ('UNKNOWN', r'.')
        ]
        
        line_num = 1
        line_start = 0
        regex_parts = []
        for pair in token_specifications:
            regex_parts.append(f"(?P<{pair[0]}>{pair[1]})")
        master_pattern = re.compile('|'.join(regex_parts))

        for mo in master_pattern.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            
            if kind == 'WHITESPACE' or kind == 'COMMENT':
                continue
            elif kind == 'UNKNOWN':
                raise SyntaxError(f"Unknown character {value} at position {mo.start()}")
            else:
                self.tokens.append(Token(kind, value))

    def next_token(self):
        if self.position < len(self.tokens):
            self.position += 1
            return self.tokens[self.position - 1]
        return None
