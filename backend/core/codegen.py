# backend/core/codegen.py

from frontend_engine.ast_nodes import *


class CodeGenerator:

    def __init__(self):

        self.intermediate = []

        self.machine = []

        self.address = 100

        self.opcodes = {

            "LOAD": "01",

            "STORE": "02",

            "ADD": "03",

            "SUB": "04",

            "MUL": "05",

            "DIV": "06",

            "MOD": "07",

            "PRINT": "08",

            "READ": "09",

            "JMP": "10",

            "JLT": "11",

            "JGT": "12",

            "JEQ": "13",

            "HALT": "FF"
        }

    # =====================================
    # GENERATE
    # =====================================

    def generate(self, ast):

        for node in ast:

            # =============================
            # ASSIGNMENT
            # =============================

            if isinstance(node, AssignmentNode):

                self.assignment(node)

            # =============================
            # SHOW
            # =============================

            elif isinstance(node, ShowNode):

                self.emit(

                    "PRINT",

                    node.variable
                )

            # =============================
            # ASK
            # =============================

            elif isinstance(node, AskNode):

                self.emit(

                    "READ",

                    node.variable
                )

            # =============================
            # DONE
            # =============================

            elif isinstance(node, DoneNode):

                self.emit("HALT")

        return {

            "intermediate": self.intermediate,

            "machine": self.machine
        }

    # =====================================
    # ASSIGNMENT
    # =====================================

    def assignment(self, node):

        if node.operator is None:

            self.emit(
                "LOAD",
                node.left
            )

            self.emit(
                "STORE",
                node.target
            )

            return

        self.emit(
            "LOAD",
            node.left
        )

        operators = {

            "+": "ADD",

            "-": "SUB",

            "*": "MUL",

            "/": "DIV",

            "%": "MOD"
        }

        opcode = operators.get(
            node.operator
        )

        self.emit(
            opcode,
            node.right
        )

        self.emit(
            "STORE",
            node.target
        )

    # =====================================
    # EMIT
    # =====================================

    def emit(

        self,

        instruction,

        operand=None
    ):

        # =============================
        # INTERMEDIATE
        # =============================

        if operand:

            self.intermediate.append(

                f"({instruction}, {operand})"
            )

        else:

            self.intermediate.append(

                f"({instruction})"
            )

        # =============================
        # MACHINE
        # =============================

        opcode = self.opcodes.get(
            instruction,
            "??"
        )

        if operand:

            machine_line = (

                f"{self.address}  "

                f"{opcode}  "

                f"{operand}"
            )

        else:

            machine_line = (

                f"{self.address}  "

                f"{opcode}"
            )

        self.machine.append(
            machine_line
        )

        self.address += 1