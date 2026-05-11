# backend/core/assembler.py

from core.codegen import CodeGenerator
from core.optimizer import Optimizer

from utils.tables import SymbolTable

# =========================================
# ASSEMBLER
# =========================================

class Assembler:

    # =====================================
    # INIT
    # =====================================

    def __init__(self):

        self.codegen = CodeGenerator()

        self.optimizer = Optimizer()

        self.symbol_table = SymbolTable()

    # =====================================
    # NODE STRING
    # =====================================

    def node_to_string(self, node):

        name = node.__class__.__name__

        values = vars(node)

        # =================================
        # EMPTY NODE
        # =================================

        if not values:

            return name

        # =================================
        # FORMAT VALUES
        # =================================

        content = []

        for key, value in values.items():

            content.append(

                f"{key}={value}"
            )

        return (

            f"{name}("
            +
            ", ".join(content)
            +
            ")"
        )

    # =====================================
    # SYMBOL TABLE
    # =====================================

    def generate_symbols(self, ast):

        symbols = []

        self.symbol_table.clear()

        address = 100

        for node in ast:

            node_name = (

                node.__class__.__name__
            )

            # =============================
            # VARIABLE
            # =============================

            if node_name == "VariableNode":

                variable = node.name

                if not self.symbol_table.exists(

                    variable
                ):

                    self.symbol_table.add(

                        variable,

                        address
                    )

                    symbols.append({

                        "symbol": variable,

                        "address": address
                    })

                    address += 1

            # =============================
            # MOV
            # =============================

            elif node_name == "MovNode":

                variable = node.variable

                if not self.symbol_table.exists(

                    variable
                ):

                    self.symbol_table.add(

                        variable,

                        address
                    )

                    symbols.append({

                        "symbol": variable,

                        "address": address
                    })

                    address += 1

            # =============================
            # LABEL
            # =============================

            elif node_name == "LabelNode":

                label = node.name

                if not self.symbol_table.exists(

                    label
                ):

                    self.symbol_table.add(

                        label,

                        address
                    )

                    symbols.append({

                        "symbol": label,

                        "address": address
                    })

        return symbols

    # =====================================
    # SAFE VM
    # =====================================

    def build_safe_vm(self, vm):

        safe_vm = []

        for instruction in vm:

            # =============================
            # LIST
            # =============================

            if isinstance(

                instruction,

                list
            ):

                safe_vm.append(

                    " ".join(

                        map(str, instruction)
                    )
                )

            # =============================
            # STRING
            # =============================

            else:

                safe_vm.append(

                    str(instruction)
                )

        return safe_vm

    # =====================================
    # ASSEMBLE
    # =====================================

    def assemble(self, ast):

        # =================================
        # AST VIEW
        # =================================

        ast_view = []

        for node in ast:

            ast_view.append(

                self.node_to_string(node)
            )

        # =================================
        # CODE GENERATION
        # =================================

        generated = self.codegen.generate(ast)

        # =================================
        # INTERMEDIATE
        # =================================

        intermediate = generated.get(

            "intermediate",

            []
        )

        # =================================
        # VM
        # =================================

        vm = generated.get(

            "vm",

            []
        )

        # =================================
        # MACHINE
        # =================================

        machine = generated.get(

            "machine",

            []
        )

        # =================================
        # SAFE VM
        # =================================

        safe_vm = self.build_safe_vm(vm)

        # =================================
        # OPTIMIZE
        # =================================

        optimized_vm, optimization_logs = (

            self.optimizer.optimize(

                safe_vm
            )
        )

        # =================================
        # SYMBOL TABLE
        # =================================

        symbols = self.generate_symbols(ast)

        # =================================
        # RETURN
        # =================================

        return {

            "ast": ast_view,

            "intermediate": intermediate,

            "vm": optimized_vm,

            "machine": machine,

            "symbols": symbols,

            "optimization": optimization_logs
        }