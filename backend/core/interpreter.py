class IntermediateGenerator:

    def generate(self, ast):

        code = []

        for node in ast:

            name = node.__class__.__name__

            # =================================
            # BEGIN
            # =================================

            if name == "BeginNode":

                code.append("BEGIN")

            # =================================
            # END
            # =================================

            elif name == "EndNode":

                code.append("END")

            # =================================
            # HALT
            # =================================

            elif name == "HaltNode":

                code.append("HALT")

            # =================================
            # VARIABLE
            # =================================

            elif name == "VariableNode":

                code.append(

                    f"DECLARE {node.name}"
                )

            # =================================
            # CONSTANT
            # =================================

            elif name == "ConstantNode":

                code.append(

                    f"CONST {node.name} {node.value}"
                )

            # =================================
            # COPY
            # =================================

            elif name == "MovNode":

                code.append(

                    f"SET {node.variable} {node.value}"
                )

            # =================================
            # LOAD
            # =================================

            elif name == "LoadNode":

                code.append(

                    f"LOAD {node.variable}"
                )

            # =================================
            # SAVE
            # =================================

            elif name == "StoreNode":

                code.append(

                    f"SAVE {node.variable}"
                )

            # =================================
            # PLUS
            # =================================

            elif name == "AddNode":

                code.append(

                    f"ADD {node.left} {node.right}"
                )

            # =================================
            # MINUS
            # =================================

            elif name == "SubNode":

                code.append(

                    f"SUB {node.left} {node.right}"
                )

            # =================================
            # MULTIPLY
            # =================================

            elif name == "MulNode":

                code.append(

                    f"MUL {node.left} {node.right}"
                )

            # =================================
            # DIVIDE
            # =================================

            elif name == "DivNode":

                code.append(

                    f"DIV {node.left} {node.right}"
                )

            # =================================
            # SHOW
            # =================================

            elif name == "PrintNode":

                code.append(

                    f"SHOW {node.variable}"
                )

            # =================================
            # READ
            # =================================

            elif name == "ReadNode":

                code.append(

                    f"READ {node.variable}"
                )

            # =================================
            # CMP
            # =================================

            elif name == "CompareNode":

                code.append(

                    f"CMP {node.left} {node.right}"
                )

            # =================================
            # JUMP
            # =================================

            elif name == "JumpNode":

                if node.condition == "LT":

                    code.append(

                        f"JL {node.label}"
                    )

                elif node.condition == "GT":

                    code.append(

                        f"JG {node.label}"
                    )

                elif node.condition == "EQ":

                    code.append(

                        f"JE {node.label}"
                    )

                else:

                    code.append(

                        f"JMP {node.label}"
                    )

            # =================================
            # LABEL
            # =================================

            elif name == "LabelNode":

                code.append(

                    f"LABEL {node.name}"
                )

        return code