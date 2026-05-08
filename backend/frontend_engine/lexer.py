from utils.tables import (
    KEYWORDS,
    OPERATORS
)


class Lexer:

    def validate(self, tokens):

        if not tokens:
            return None

        first = tokens[0]

        # Keywords
        if first in KEYWORDS:
            return None

        # Label
        if len(tokens) >= 2 and tokens[1] == ":":
            return None

        # Assignment
        if "=" in tokens:
            return None

        return None