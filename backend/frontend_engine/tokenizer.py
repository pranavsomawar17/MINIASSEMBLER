# backend/frontend_engine/tokenizer.py

class Tokenizer:

    def tokenize(self, line):

        # =====================================
        # REMOVE COMMENTS
        # =====================================

        if ";" in line:

            line = line.split(";")[0]

        line = str(line).strip()

        if not line:

            return []

        # =====================================
        # CLEAN SYMBOLS
        # =====================================

        replacements = {

            ",": " ",

            "=": " = ",

            "\t": " "
        }

        for old, new in replacements.items():

            line = line.replace(old, new)

        # =====================================
        # TOKENIZE
        # =====================================

        tokens = [

            token.strip()

            for token in line.split()

            if token.strip()
        ]

        return tokens