import re


class Tokenizer:

    def tokenize(self, line):

        # -----------------------------------------
        # Clean line
        # -----------------------------------------
        line = line.strip()

        # -----------------------------------------
        # Remove comments
        # -----------------------------------------
        if "#" in line:

            line = line.split("#")[0]

        # -----------------------------------------
        # Token regex
        # -----------------------------------------
        pattern = r'''

        [A-Za-z_][A-Za-z0-9_]*

        |==|!=|>=|<=

        |[+\-*/%=<>?]

        |\d+

        |:

        '''

        # -----------------------------------------
        # Extract tokens
        # -----------------------------------------
        tokens = re.findall(
            pattern,
            line,
            re.VERBOSE
        )

        return tokens