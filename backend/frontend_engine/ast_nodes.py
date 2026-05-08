# backend/frontend_engine/ast_nodes.py

class ASTNode:
    pass


# =========================================
# BEGIN
# =========================================

class BeginNode(ASTNode):

    def __repr__(self):

        return "BeginNode()"


# =========================================
# DONE
# =========================================

class DoneNode(ASTNode):

    def __repr__(self):

        return "DoneNode()"


# =========================================
# VARIABLE
# =========================================

class VariableNode(ASTNode):

    def __init__(self, var_type, name):

        self.var_type = var_type

        self.name = name

    def __repr__(self):

        return f"VariableNode({self.var_type}, {self.name})"


# =========================================
# ASSIGNMENT
# =========================================

class AssignmentNode(ASTNode):

    def __init__(
        self,
        target,
        left,
        operator=None,
        right=None
    ):

        self.target = target

        self.left = left

        self.operator = operator

        self.right = right

    def __repr__(self):

        return (
            f"AssignmentNode("
            f"{self.target}, "
            f"{self.left}, "
            f"{self.operator}, "
            f"{self.right})"
        )


# =========================================
# SHOW
# =========================================

class ShowNode(ASTNode):

    def __init__(self, variable):

        self.variable = variable

    def __repr__(self):

        return f"ShowNode({self.variable})"


# =========================================
# ASK
# =========================================

class AskNode(ASTNode):

    def __init__(self, variable):

        self.variable = variable

    def __repr__(self):

        return f"AskNode({self.variable})"


# =========================================
# LABEL
# =========================================

class LabelNode(ASTNode):

    def __init__(self, name):

        self.name = name

    def __repr__(self):

        return f"LabelNode({self.name})"


# =========================================
# IF
# =========================================

class IfNode(ASTNode):

    def __init__(
        self,
        left,
        operator,
        right,
        label
    ):

        self.left = left

        self.operator = operator

        self.right = right

        self.label = label

    def __repr__(self):

        return (
            f"IfNode("
            f"{self.left}, "
            f"{self.operator}, "
            f"{self.right}, "
            f"{self.label})"
        )
# =========================================
# COMPARE
# =========================================

class CompareNode(ASTNode):

    def __init__(self, left, right):

        self.left = left

        self.right = right

    def __repr__(self):

        return f"CompareNode({self.left}, {self.right})"