# backend/core/interpreter.py

from frontend_engine.ast_nodes import *


class Interpreter:

    def __init__(self):

        # =====================================
        # MEMORY
        # =====================================

        self.memory = {}

        # =====================================
        # OUTPUT
        # =====================================

        self.output = []

        # =====================================
        # DEBUG TRACE
        # =====================================

        self.debug = []

        # =====================================
        # LABEL TABLE
        # =====================================

        self.labels = {}

    # =========================================
    # GET VALUE
    # =========================================

    def get_value(self, token):

        # NUMBER

        if str(token).isdigit():

            return int(token)

        # VARIABLE

        return self.memory.get(token, 0)

    # =========================================
    # RUN
    # =========================================

    def run(self, ast):

        # =====================================
        # BUILD LABEL TABLE
        # =====================================

        for index, node in enumerate(ast):

            if isinstance(node, LabelNode):

                self.labels[node.name] = index

        # =====================================
        # PROGRAM COUNTER
        # =====================================

        pc = 0

        # =====================================
        # EXECUTION LOOP
        # =====================================

        while pc < len(ast):

            node = ast[pc]

            # =================================
            # DEBUG TRACE
            # =================================

            self.debug.append(

                f"PC {pc} -> {node}"
            )

            # =================================
            # BEGIN
            # =================================

            if isinstance(node, BeginNode):

                pass

            # =================================
            # DONE
            # =================================

            elif isinstance(node, DoneNode):

                break

            # =================================
            # VARIABLE DECLARATION
            # =================================

            elif isinstance(node, VariableNode):

                self.memory[node.name] = 0

            # =================================
            # ASK INPUT
            # =================================

            elif isinstance(node, AskNode):

                # DEMO INPUT VALUE

                self.memory[node.variable] = 0

            # =================================
            # SHOW OUTPUT
            # =================================

            elif isinstance(node, ShowNode):

                value = self.memory.get(

                    node.variable,

                    0
                )

                self.output.append(

                    f"{node.variable} = {value}"
                )

            # =================================
            # ASSIGNMENT
            # =================================

            elif isinstance(node, AssignmentNode):

                left = self.get_value(
                    node.left
                )

                result = left

                # =============================
                # EXPRESSION
                # =============================

                if node.operator:

                    right = self.get_value(
                        node.right
                    )

                    # ADD

                    if node.operator == "+":

                        result = left + right

                    # SUB

                    elif node.operator == "-":

                        result = left - right

                    # MUL

                    elif node.operator == "*":

                        result = left * right

                    # DIV

                    elif node.operator == "/":

                        result = left // right

                    # MOD

                    elif node.operator == "%":

                        result = left % right

                # STORE RESULT

                self.memory[node.target] = result

            # =================================
            # COMPARE VISUALIZATION
            # =================================

            elif isinstance(node, CompareNode):

                left = self.get_value(
                    node.left
                )

                right = self.get_value(
                    node.right
                )

                if left > right:

                    self.output.append(

                        f"{node.left} > {node.right}"
                    )

                elif left < right:

                    self.output.append(

                        f"{node.left} < {node.right}"
                    )

                else:

                    self.output.append(

                        f"{node.left} == {node.right}"
                    )

            # =================================
            # IF CONDITION
            # =================================

            elif isinstance(node, IfNode):

                left = self.get_value(
                    node.left
                )

                right = self.get_value(
                    node.right
                )

                condition = False

                # =============================
                # ==
                # =============================

                if node.operator == "==":

                    condition = left == right

                # =============================
                # !=
                # =============================

                elif node.operator == "!=":

                    condition = left != right

                # =============================
                # >
                # =============================

                elif node.operator == ">":

                    condition = left > right

                # =============================
                # <
                # =============================

                elif node.operator == "<":

                    condition = left < right

                # =============================
                # >=
                # =============================

                elif node.operator == ">=":

                    condition = left >= right

                # =============================
                # <=
                # =============================

                elif node.operator == "<=":

                    condition = left <= right

                # =============================
                # JUMP
                # =============================

                if condition:

                    pc = self.labels.get(

                        node.label,

                        pc
                    )

                    continue

            # =================================
            # LABEL
            # =================================

            elif isinstance(node, LabelNode):

                pass

            # =================================
            # NEXT INSTRUCTION
            # =================================

            pc += 1

        # =====================================
        # SYMBOL TABLE
        # =====================================

        symbol_table = {}

        address = 100

        for variable in self.memory:

            symbol_table[variable] = address

            address += 1

        # =====================================
        # RETURN RESULT
        # =====================================

        return {

            "memory": self.memory,

            "output": self.output,

            "debug": self.debug,

            "symbol_table": symbol_table
        }