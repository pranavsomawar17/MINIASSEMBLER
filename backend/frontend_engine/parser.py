# backend/frontend_engine/parser.py

from frontend_engine.ast_nodes import *

# =========================================
# PARSER
# =========================================

class Parser:

    # =====================================
    # PARSE
    # =====================================

    def parse(self, tokens):

        # =================================
        # EMPTY
        # =================================

        if not tokens:

            return None

        # =================================
        # STRING -> TOKENS
        # =================================

        if not isinstance(tokens, list):

            tokens = str(tokens).split()

        tokens = [

            str(token).strip()

            for token in tokens

            if str(token).strip()
        ]

        # =================================
        # EMPTY AFTER CLEAN
        # =================================

        if not tokens:

            return None

        keyword = tokens[0].upper()

        # =================================
        # BEGIN
        # =================================

        if keyword == "HELLO":

            return BeginNode()

        # =================================
        # HALT
        # =================================

        if keyword in [

            "TERMINATE",

            "HALT"
        ]:

            return HaltNode()

        # =================================
        # VARIABLE ASSIGN
        # X ASSIGN 0
        # =================================

        if len(tokens) >= 3:

            if tokens[1].upper() == "ASSIGN":

                return [

                    VariableNode(

                        tokens[0]
                    ),

                    MovNode(

                        tokens[0],

                        tokens[2]
                    )
                ]

        # =================================
        # COPY
        # COPY X, 10
        # =================================

        if keyword == "COPY":

            variable = (

                tokens[1]

                .replace(",", "")
            )

            value = tokens[2]

            return MovNode(

                variable,

                value
            )

        # =================================
        # PLUS
        # =================================

        if keyword == "PLUS":

            return AddNode(

                tokens[1],

                tokens[2]
            )

        # =================================
        # MINUS
        # =================================

        if keyword == "MINUS":

            return SubNode(

                tokens[1],

                tokens[2]
            )

        # =================================
        # MULTIPLY
        # =================================

        if keyword == "MULTIPLY":

            return MulNode(

                tokens[1],

                tokens[2]
            )

        # =================================
        # DIVIDE
        # =================================

        if keyword == "DIVIDE":

            return DivNode(

                tokens[1],

                tokens[2]
            )

        # =================================
        # SAVE
        # =================================

        if keyword == "SAVE":

            return StoreNode(

                tokens[1]
            )

        # =================================
        # SHOW
        # =================================

        if keyword == "SHOW":

            return PrintNode(

                tokens[1]
            )

        # =================================
        # READ
        # =================================

        if keyword == "READ":

            return ReadNode(

                tokens[1]
            )

        # =================================
        # CMP
        # =================================

        if keyword == "CMP":

            return CompareNode(

                tokens[1],

                tokens[2]
            )

        # =====================================
        # LABEL
        # LOOP:
        # =====================================

        if tokens[0].endswith(":"):

            label = tokens[0].replace(":", "")

            return LabelNode(label)

        # =====================================
        # HOP
        # =====================================

        if keyword == "HOP":

            return JumpNode(

                "ALWAYS",

                tokens[1]
            )

        # =====================================
        # JZ
        # =====================================

        if keyword == "JZ":

            return JumpNode(

                "ZERO",

                tokens[1]
            )

        # =====================================
        # JNZ
        # =====================================

        if keyword == "JNZ":

            return JumpNode(

                "NOT_ZERO",

                tokens[1]
            )
        return None