# backend/frontend_engine/lexer.py

from frontend_engine.tokenizer import Tokenizer


class Lexer:

    def __init__(self, source):

        self.source = source

        self.tokenizer = Tokenizer()

    def tokenize(self):

        tokens = []

        lines = self.source.splitlines()

        for line in lines:

            line_tokens = self.tokenizer.tokenize(line)

            if not line_tokens:

                continue

            tokens.extend(line_tokens)

            tokens.append("NEWLINE")

        return tokens