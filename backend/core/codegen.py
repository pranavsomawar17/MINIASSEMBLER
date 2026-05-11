# backend/core/codegen.py

class CodeGenerator:

    # =====================================
    # INIT
    # =====================================

    def __init__(self):

        self.opcodes = {

            "BEGIN": "00",

            "DECLARE": "01",

            "SET": "02",

            "ADD": "03",

            "SUB": "04",

            "MUL": "05",

            "DIV": "06",

            "SAVE": "07",

            "SHOW": "08",

            "READ": "09",

            "CMP": "0A",

            "JNZ": "0C",

            "JZ": "0D",

            "HOP": "0E",

            "LABEL": "0F",

            "HALT": "FF"
        }

        self.reset()

    # =====================================
    # RESET
    # =====================================

    def reset(self):

        self.intermediate = []

        self.vm = []

        self.machine = []

        self.address = 100

        self.labels = {}

        self.variables = set()

    # =====================================
    # GENERATE
    # =====================================

    def generate(self, ast):

        self.reset()

        # =================================
        # FIRST PASS
        # LABEL ADDRESSES
        # =================================

        temp_address = self.address

        for node in ast:

            node_name = node.__class__.__name__

            if node_name == "LabelNode":

                self.labels[node.name] = temp_address

            else:

                temp_address += 1

        # =================================
        # SECOND PASS
        # =================================

        for node in ast:

            node_name = node.__class__.__name__

            # =============================
            # BEGIN
            # =============================

            if node_name in [

                "StartNode",

                "BeginNode"
            ]:

                self.emit(

                    "HELLO",

                    "BEGIN"
                )

            # =============================
            # MOV
            # =============================

            elif node_name == "MovNode":

                variable = node.variable

                value = node.value

                # =========================
                # DECLARE ONCE
                # =========================

                if variable not in self.variables:

                    self.emit(

                        f"{variable} ASSIGN 0",

                        "DECLARE",

                        variable
                    )

                    self.variables.add(variable)

                # =========================
                # SET
                # =========================

                self.emit(

                    f"COPY {variable}, {value}",

                    "SET",

                    f"{variable} {value}"
                )

            # =============================
            # ADD
            # =============================

            elif node_name == "AddNode":

                self.emit(

                    f"PLUS {node.left} {node.right}",

                    "ADD",

                    f"{node.left} {node.right}"
                )

            # =============================
            # SUB
            # =============================

            elif node_name == "SubNode":

                self.emit(

                    f"MINUS {node.left} {node.right}",

                    "SUB",

                    f"{node.left} {node.right}"
                )

            # =============================
            # MUL
            # =============================

            elif node_name == "MulNode":

                self.emit(

                    f"MULTIPLY {node.left} {node.right}",

                    "MUL",

                    f"{node.left} {node.right}"
                )

            # =============================
            # DIV
            # =============================

            elif node_name == "DivNode":

                self.emit(

                    f"DIVIDE {node.left} {node.right}",

                    "DIV",

                    f"{node.left} {node.right}"
                )

            # =============================
            # SAVE
            # =============================

            elif node_name == "StoreNode":

                variable = node.variable

                if variable not in self.variables:

                    self.emit(

                        f"{variable} ASSIGN 0",

                        "DECLARE",

                        variable
                    )

                    self.variables.add(variable)

                self.emit(

                    f"SAVE {variable}",

                    "SAVE",

                    variable
                )

            # =============================
            # SHOW
            # =============================

            elif node_name == "PrintNode":

                self.emit(

                    f"SHOW {node.variable}",

                    "SHOW",

                    node.variable
                )

            # =============================
            # READ
            # =============================

            elif node_name == "ReadNode":

                self.emit(

                    f"READ {node.variable}",

                    "READ",

                    node.variable
                )

            # =============================
            # CMP
            # =============================

            elif node_name == "CompareNode":

                self.emit(

                    f"CMP {node.left} {node.right}",

                    "CMP",

                    f"{node.left} {node.right}"
                )

            # =============================
            # LABEL
            # =============================

            elif node_name == "LabelNode":

                self.emit(

                    f"{node.name}:",

                    "LABEL",

                    node.name
                )

            # =============================
            # JUMP
            # =============================

            elif node_name == "JumpNode":

                target = self.labels.get(

                    node.label,

                    0
                )

                # =========================
                # JZ
                # =========================

                if node.condition == "ZERO":

                    self.emit(

                        f"JZ {node.label}",

                        "JZ",

                        f"{node.label} {target}"
                    )

                # =========================
                # JNZ
                # =========================

                elif node.condition == "NOT_ZERO":

                    self.emit(

                        f"JNZ {node.label}",

                        "JNZ",

                        f"{node.label} {target}"
                    )

                # =========================
                # HOP
                # =========================

                else:

                    self.emit(

                        f"HOP {node.label}",

                        "HOP",

                        f"{node.label} {target}"
                    )

            # =============================
            # HALT
            # =============================

            elif node_name in [

                "EndNode",

                "HaltNode"
            ]:

                self.emit(

                    "TERMINATE",

                    "HALT"
                )

        # =================================
        # RETURN
        # =================================

        return {

            "intermediate": self.intermediate,

            "vm": self.vm,

            "machine": self.machine
        }

    # =====================================
    # EMIT
    # =====================================

    def emit(

        self,

        intermediate,

        instruction,

        operand=None
    ):

        # =================================
        # INTERMEDIATE
        # =================================

        self.intermediate.append(

            intermediate
        )

        # =================================
        # VM
        # =================================

        if operand:

            vm_line = (

                instruction
                +
                " "
                +
                operand
            )

        else:

            vm_line = instruction

        self.vm.append(vm_line)

        # =================================
        # MACHINE
        # =================================

        opcode = self.opcodes.get(

            instruction,

            "??"
        )

        if operand:

            machine_line = (

                f"{self.address}  "
                +
                f"{opcode}  "
                +
                f"{operand}"
            )

        else:

            machine_line = (

                f"{self.address}  "
                +
                f"{opcode}"
            )

        self.machine.append(

            machine_line
        )

        self.address += 1