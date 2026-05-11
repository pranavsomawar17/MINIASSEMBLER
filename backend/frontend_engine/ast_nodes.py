# =========================================
# PROGRAM CONTROL
# =========================================

class BeginNode:

    def __str__(self):

        return "BeginNode()"


class EndNode:

    def __str__(self):

        return "EndNode()"


class HaltNode:

    def __str__(self):

        return "HaltNode()"


# =========================================
# MEMORY
# =========================================

class VariableNode:

    def __init__(self, name):

        self.name = name

    def __str__(self):

        return f"VariableNode(name={self.name})"


class ConstantNode:

    def __init__(self, name, value):

        self.name = name

        self.value = value

    def __str__(self):

        return (

            f"ConstantNode("
            f"name={self.name}, "
            f"value={self.value})"
        )


class MovNode:

    def __init__(self, variable, value):

        self.variable = variable

        self.value = value

    def __str__(self):

        return (

            f"MovNode("
            f"variable={self.variable}, "
            f"value={self.value})"
        )


class LoadNode:

    def __init__(self, variable):

        self.variable = variable

    def __str__(self):

        return (

            f"LoadNode("
            f"variable={self.variable})"
        )


class StoreNode:

    def __init__(self, variable):

        self.variable = variable

    def __str__(self):

        return (

            f"StoreNode("
            f"variable={self.variable})"
        )


# =========================================
# ARITHMETIC
# =========================================

class AddNode:

    def __init__(self, left, right):

        self.left = left

        self.right = right

    def __str__(self):

        return (

            f"AddNode("
            f"left={self.left}, "
            f"right={self.right})"
        )


class SubNode:

    def __init__(self, left, right):

        self.left = left

        self.right = right

    def __str__(self):

        return (

            f"SubNode("
            f"left={self.left}, "
            f"right={self.right})"
        )


class MulNode:

    def __init__(self, left, right):

        self.left = left

        self.right = right

    def __str__(self):

        return (

            f"MulNode("
            f"left={self.left}, "
            f"right={self.right})"
        )


class DivNode:

    def __init__(self, left, right):

        self.left = left

        self.right = right

    def __str__(self):

        return (

            f"DivNode("
            f"left={self.left}, "
            f"right={self.right})"
        )


# =========================================
# INPUT OUTPUT
# =========================================

class PrintNode:

    def __init__(self, variable):

        self.variable = variable

    def __str__(self):

        return (

            f"PrintNode("
            f"variable={self.variable})"
        )


class ReadNode:

    def __init__(self, variable):

        self.variable = variable

    def __str__(self):

        return (

            f"ReadNode("
            f"variable={self.variable})"
        )


# =========================================
# COMPARISON
# =========================================

class CompareNode:

    def __init__(self, left, right):

        self.left = left

        self.right = right

    def __str__(self):

        return (

            f"CompareNode("
            f"left={self.left}, "
            f"right={self.right})"
        )


# =========================================
# FLOW CONTROL
# =========================================

class JumpNode:

    def __init__(self, condition, label):

        self.condition = condition

        self.label = label

    def __str__(self):

        return (

            f"JumpNode("
            f"condition={self.condition}, "
            f"label={self.label})"
        )


class LabelNode:

    def __init__(self, name):

        self.name = name

    def __str__(self):

        return (

            f"LabelNode("
            f"name={self.name})"
        )