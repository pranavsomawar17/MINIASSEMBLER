# backend/frontend_engine/parser.py

from frontend_engine.tokenizer import Tokenizer

from frontend_engine.ast_nodes import *


class Parser:

    def __init__(self):

        self.tokenizer = Tokenizer()

    def parse(self, line):

        line = line.strip()

        if not line:

            return None

        # =====================================
        # LABEL
        # =====================================

        if line.endswith(":"):

            label = line.replace(
                ":",
                ""
            ).strip()

            return LabelNode(label)

        tokens = self.tokenizer.tokenize(line)

        if not tokens:

            return None

        # =====================================
        # BEGIN
        # =====================================

        if tokens[0] == "BEGIN":

            return BeginNode()

        # =====================================
        # DONE
        # =====================================

        if tokens[0] == "DONE":

            return DoneNode()

        # =====================================
        # VARIABLE
        # =====================================

        if tokens[0] == "NUMBER":

            return VariableNode(

                "NUMBER",

                tokens[1]
            )

        # =====================================
        # ASK
        # =====================================

        if tokens[0] == "ASK":

            return AskNode(tokens[1])

        # =====================================
        # SHOW
        # =====================================

        if tokens[0] == "SHOW":

            return ShowNode(tokens[1])

        # =====================================
        # IF
        # =====================================

        if tokens[0] == "IF":

            return IfNode(

                left=tokens[1],

                operator=tokens[2],

                right=tokens[3],

                label=tokens[5]
            )
        
        # =====================================
        # COMPARE
        # =====================================

        if "?" in tokens:

            return CompareNode(

                left=tokens[0],

                right=tokens[2]
            )
        
        # =====================================
        # ASSIGNMENT
        # =====================================

        if "=" in tokens:

            target = tokens[0]

            if len(tokens) == 3:

                return AssignmentNode(

                    target=target,

                    left=tokens[2]
                )

            if len(tokens) == 5:

                return AssignmentNode(

                    target=target,

                    left=tokens[2],

                    operator=tokens[3],

                    right=tokens[4]
                )

        raise Exception(
            f"Invalid syntax: {line}"
        )
        # =====================================
        # COMPARE
        # =====================================

        if "?" in tokens:

            return CompareNode(

                left=tokens[0],

                right=tokens[2]
            )