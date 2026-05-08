class SemanticAnalyzer:

    def __init__(self):

        self.variables = {}

        self.labels = set()

        self.errors = []

        self.address_counter = 100


    # =========================================
    # DECLARE VARIABLE
    # =========================================

    def declare_variable(self, name):

        if name not in self.variables:

            self.variables[name] = {

                "address": self.address_counter
            }

            self.address_counter += 1


    # =========================================
    # ANALYZE
    # =========================================

    def analyze(self, ast):

        # -------------------------------------
        # PASS 1 → LABELS
        # -------------------------------------

        for node in ast:

            if hasattr(node, "label"):

                self.labels.add(node.label)

        # -------------------------------------
        # PASS 2 → VARIABLES
        # -------------------------------------

        for node in ast:

            node_type = type(node).__name__

            # ---------------------------------
            # VARIABLE DECLARATION
            # ---------------------------------

            if node_type == "VariableNode":

                self.declare_variable(
                    node.name
                )

            # ---------------------------------
            # ASSIGNMENT
            # ---------------------------------

            elif node_type == "AssignmentNode":

                # auto declare left side

                self.declare_variable(
                    node.target
                )

                # check operands

                for operand in [

                    node.left,

                    node.right
                ]:

                    if operand is None:
                        continue

                    if operand.isdigit():
                        continue

                    if operand not in self.variables:

                        self.errors.append(

                            f"Undefined variable '{operand}'"
                        )

            # ---------------------------------
            # SHOW
            # ---------------------------------

            elif node_type == "ShowNode":

                variable = node.variable

                if variable not in self.variables:

                    self.errors.append(

                        f"Undefined variable '{variable}'"
                    )

            # ---------------------------------
            # IF
            # ---------------------------------

            elif node_type == "IfNode":

                if node.left not in self.variables:

                    self.errors.append(

                        f"Undefined variable '{node.left}'"
                    )

                if not node.right.isdigit():

                    if node.right not in self.variables:

                        self.errors.append(

                            f"Undefined variable '{node.right}'"
                        )

                if node.label not in self.labels:

                    self.errors.append(

                        f"Undefined label '{node.label}'"
                    )

        return {

            "errors": self.errors,

            "symbols": [

                {

                    "symbol": name,

                    "address": info["address"]
                }

                for name, info in self.variables.items()
            ]
        }