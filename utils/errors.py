from utils.tables import REGISTERS, DIRECTIVES


def check_errors(program, symbol_table, opcode):

    errors = []

    for line_no, raw in enumerate(program, start=1):

        line = raw.strip()

        # =============================
        # Ignore empty lines
        # =============================
        if not line:
            continue

        # =============================
        # Ignore comments
        # =============================
        if line.startswith(";"):
            continue

        # Remove inline comments
        if ";" in line:
            line = line.split(";")[0].strip()

        # =============================
        # Handle labels
        # =============================
        if ":" in line:

            _, line = line.split(":", 1)

            line = line.strip()

            if not line:
                continue

        parts = line.replace(",", " ").split()

        if not parts:
            continue

        op = parts[0].upper()

        # =============================
        # Skip directives
        # =============================
        if op in DIRECTIVES:
            continue

        # =============================
        # Invalid opcode
        # =============================
        if op not in opcode:

            errors.append(
                f"Line {line_no}: Invalid opcode '{op}'"
            )

            continue

        # =============================
        # Register validation
        # =============================
        for token in parts[1:]:

            if token.startswith("R"):

                if token not in REGISTERS:

                    errors.append(
                        f"Line {line_no}: Invalid register '{token}'"
                    )

        # =============================
        # Undefined symbols
        # =============================
        if op in {"LOAD", "STORE", "JMP", "JZ", "JNZ"}:

            target = parts[-1]

            if (
                not target.isdigit()
                and target not in symbol_table
            ):

                errors.append(
                    f"Line {line_no}: Undefined symbol '{target}'"
                )

        # =============================
        # Division by zero
        # =============================
        if op == "DIV":

            if len(parts) >= 3:

                if parts[2] == "0":

                    errors.append(
                        f"Line {line_no}: Division by zero"
                    )

    return errors