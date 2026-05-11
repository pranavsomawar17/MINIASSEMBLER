# backend/core/optimizer.py

from utils.diagnostics import Diagnostic


class Optimizer:

    def __init__(self):

        self.reset()

    # =====================================
    # RESET
    # =====================================

    def reset(self):

        self.suggestions = []

    # =====================================
    # ADD DIAGNOSTIC
    # =====================================

    def add(

        self,

        severity,

        line,

        message,

        suggestion
    ):

        diagnostic = Diagnostic(

            severity,

            line,

            message,

            suggestion
        )

        self.suggestions.append(

            diagnostic.to_dict()
        )

    # =====================================
    # SAFE STRING
    # =====================================

    def safe_string(self, line):

        # =============================
        # TOKEN LIST
        # =============================

        if isinstance(line, list):

            return " ".join(

                map(str, line)
            )

        # =============================
        # NORMAL STRING
        # =============================

        return str(line)

    # =====================================
    # OPTIMIZE
    # =====================================

    def optimize(self, lines):

        self.reset()

        optimized = []

        previous = None

        unreachable = False

        unreachable_reported = False

        declared = set()

        used = set()

        # =================================
        # MAIN LOOP
        # =================================

        for index, raw_line in enumerate(lines):

            line_number = index + 1

            # =============================
            # SAFE CONVERT
            # =============================

            line = self.safe_string(raw_line)

            stripped = line.strip()

            # =============================
            # EMPTY
            # =============================

            if not stripped:

                continue

            # =============================
            # DUPLICATE
            # =============================

            if (

                stripped == previous

                and

                not stripped.startswith("LABEL")

                and

                not stripped.startswith("DECLARE")
            ):

                self.add(

                    "OPTIMIZATION",

                    line_number,

                    "Duplicate instruction",

                    "Remove repeated instruction"
                )

                continue

            # =============================
            # SAVE PREVIOUS
            # =============================

            if not stripped.startswith("LABEL"):

                previous = stripped

            # =============================
            # UNREACHABLE
            # =============================

            if unreachable:

                if not unreachable_reported:

                    self.add(

                        "WARNING",

                        line_number,

                        "Unreachable code",

                        "Remove dead code"
                    )

                    unreachable_reported = True

            # =============================
            # HALT
            # =============================

            if stripped in [

                "HALT",

                "TERMINATE"
            ]:

                unreachable = True

            # =============================
            # DECLARE
            # =============================

            tokens = stripped.split()

            if (

                len(tokens) >= 2

                and

                tokens[0] == "DECLARE"
            ):

                declared.add(tokens[1])

            # =============================
            # VARIABLE USAGE
            # =============================

            for variable in declared:

                if variable in stripped:

                    used.add(variable)

            # =============================
            # REDUNDANT ADD
            # =============================

            if (

                len(tokens) >= 3

                and

                tokens[0] == "ADD"

                and

                tokens[-1] == "0"
            ):

                self.add(

                    "OPTIMIZATION",

                    line_number,

                    "Redundant addition",

                    "Remove +0"
                )

            # =============================
            # REDUNDANT SUB
            # =============================

            if (

                len(tokens) >= 3

                and

                tokens[0] == "SUB"

                and

                tokens[-1] == "0"
            ):

                self.add(

                    "OPTIMIZATION",

                    line_number,

                    "Redundant subtraction",

                    "Remove -0"
                )

            # =============================
            # REDUNDANT MUL
            # =============================

            if (

                len(tokens) >= 3

                and

                tokens[0] == "MUL"

                and

                tokens[-1] == "1"
            ):

                self.add(

                    "OPTIMIZATION",

                    line_number,

                    "Redundant multiplication",

                    "Remove *1"
                )

            # =============================
            # REDUNDANT DIV
            # =============================

            if (

                len(tokens) >= 3

                and

                tokens[0] == "DIV"

                and

                tokens[-1] == "1"
            ):

                self.add(

                    "OPTIMIZATION",

                    line_number,

                    "Redundant division",

                    "Remove /1"
                )

            # =============================
            # MULTIPLY ZERO
            # =============================

            if (

                len(tokens) >= 3

                and

                tokens[0] == "MUL"

                and

                tokens[-1] == "0"
            ):

                self.add(

                    "OPTIMIZATION",

                    line_number,

                    "Multiplication by zero",

                    "Replace result with 0"
                )

            # =============================
            # CONSTANT FOLDING
            # =============================

            try:

                if len(tokens) >= 3:

                    op = tokens[0]

                    a = int(tokens[1])

                    b = int(tokens[2])

                    result = None

                    if op == "ADD":

                        result = a + b

                    elif op == "SUB":

                        result = a - b

                    elif op == "MUL":

                        result = a * b

                    elif op == "DIV":

                        if b != 0:

                            result = a // b

                    if result is not None:

                        self.add(

                            "OPTIMIZATION",

                            line_number,

                            "Constant folding possible",

                            f"Replace with {result}"
                        )

            except:

                pass

            # =============================
            # KEEP
            # =============================

            optimized.append(stripped)

        # =================================
        # UNUSED VARIABLES
        # =================================

        for variable in declared:

            appearances = sum(

                variable in self.safe_string(line)

                for line in lines
            )

            if appearances <= 1:

                self.add(

                    "WARNING",

                    0,

                    f"Unused variable '{variable}'",

                    "Remove declaration"
                )

        # =================================
        # RETURN
        # =================================

        return optimized, self.suggestions