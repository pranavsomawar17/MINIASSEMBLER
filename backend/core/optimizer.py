class Optimizer:

    def optimize(self, lines):

        suggestions = []

        for index, line in enumerate(lines):

            line = line.strip()

            # -------------------------------------
            # +0 optimization
            # -------------------------------------
            if "+ 0" in line:

                suggestions.append(

                    f"Line {index+1}: "

                    f"Remove '+ 0'"
                )

            # -------------------------------------
            # *1 optimization
            # -------------------------------------
            if "* 1" in line:

                suggestions.append(

                    f"Line {index+1}: "

                    f"Remove '* 1'"
                )

            # -------------------------------------
            # useless assignment
            # -------------------------------------
            if "= A" in line and line.startswith("A"):

                suggestions.append(

                    f"Line {index+1}: "

                    f"Redundant assignment"
                )

        return suggestions