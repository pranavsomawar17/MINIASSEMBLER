from utils.diagnostics import Diagnostic


class SemanticAnalyzer:

    def __init__(self):

        self.variables = set()

        self.labels = set()

        self.errors = []

    # =====================================
    # RESET
    # =====================================

    def reset(self):

        self.variables.clear()

        self.labels.clear()

        self.errors.clear()

    # =====================================
    # ERROR
    # =====================================

    def add_error(

        self,

        line,

        message,

        suggestion=""
    ):

        self.errors.append(

            Diagnostic(

                severity="ERROR",

                line=line,

                message=message,

                suggestion=suggestion
            ).to_dict()
        )

    # =====================================
    # DECLARE VARIABLE
    # =====================================

    def declare_variable(

        self,

        variable,

        line
    ):

        if variable in self.variables:

            self.add_error(

                line,

                f"Variable '{variable}' already declared",

                "Use another variable name"
            )

        else:

            self.variables.add(variable)

    # =====================================
    # CHECK VARIABLE
    # =====================================

    def check_variable(

        self,

        variable,

        line
    ):

        if variable not in self.variables:

            self.add_error(

                line,

                f"Variable '{variable}' not declared",

                f"Declare '{variable}' before use"
            )

    # =====================================
    # ANALYZE
    # =====================================

    def analyze(self, ast):

        self.reset()

        # =================================
        # FIRST PASS
        # =================================

        for index, node in enumerate(ast):

            line_no = index + 1

            node_name = node.__class__.__name__

            # =============================
            # VARIABLE
            # =============================

            if node_name == "VariableNode":

                self.declare_variable(

                    node.name,

                    line_no
                )

            # =============================
            # CONSTANT
            # =============================

            elif node_name == "ConstantNode":

                self.declare_variable(

                    node.name,

                    line_no
                )

            # =============================
            # LABEL
            # =============================

            elif node_name == "LabelNode":

                if node.name in self.labels:

                    self.add_error(

                        line_no,

                        f"Duplicate label '{node.name}'",

                        "Rename label"
                    )

                else:

                    self.labels.add(node.name)

        # =================================
        # SECOND PASS
        # =================================

        for index, node in enumerate(ast):

            line_no = index + 1

            node_name = node.__class__.__name__

            # =============================
            # MOV
            # =============================

            if node_name == "MovNode":

                self.check_variable(

                    node.variable,

                    line_no
                )

            # =============================
            # LOAD
            # =============================

            elif node_name == "LoadNode":

                self.check_variable(

                    node.variable,

                    line_no
                )

            # =============================
            # STORE
            # =============================

            elif node_name == "StoreNode":

                self.check_variable(

                    node.variable,

                    line_no
                )

            # =============================
            # ADD
            # =============================

            elif node_name == "AddNode":

                self.check_variable(

                    node.left,

                    line_no
                )

                self.check_variable(

                    node.right,

                    line_no
                )

            # =============================
            # SUB
            # =============================

            elif node_name == "SubNode":

                self.check_variable(

                    node.left,

                    line_no
                )

                self.check_variable(

                    node.right,

                    line_no
                )

            # =============================
            # MUL
            # =============================

            elif node_name == "MulNode":

                self.check_variable(

                    node.left,

                    line_no
                )

                self.check_variable(

                    node.right,

                    line_no
                )

            # =============================
            # DIV
            # =============================

            elif node_name == "DivNode":

                self.check_variable(

                    node.left,

                    line_no
                )

                self.check_variable(

                    node.right,

                    line_no
                )

            # =============================
            # PRINT
            # =============================

            elif node_name == "PrintNode":

                self.check_variable(

                    node.variable,

                    line_no
                )

            # =============================
            # READ
            # =============================

            elif node_name == "ReadNode":

                self.check_variable(

                    node.variable,

                    line_no
                )

            # =============================
            # CMP
            # =============================

            elif node_name == "CompareNode":

                self.check_variable(

                    node.left,

                    line_no
                )

                self.check_variable(

                    node.right,

                    line_no
                )

            # =============================
            # JUMP
            # =============================

            elif node_name == "JumpNode":

                if node.label not in self.labels:

                    self.add_error(

                        line_no,

                        f"Undefined label '{node.label}'",

                        "Create label before jump"
                    )

        # =================================
        # RETURN
        # =================================

        return {

            "errors": self.errors,

            "symbols": sorted(

                list(self.variables)
            )
        }