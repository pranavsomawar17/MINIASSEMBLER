def optimize(program):

    optimized = []

    logs = []

    i = 0

    while i < len(program):

        line = program[i].strip()

        # =============================
        # Ignore empty lines
        # =============================
        if not line:

            i += 1
            continue

        # =============================
        # Remove comments
        # =============================
        if line.startswith(";"):

            i += 1
            continue

        # =============================
        # Remove MOV R1, R1
        # =============================
        if line.startswith("MOV"):

            parts = line.replace(",", " ").split()

            if len(parts) >= 3:

                if parts[1] == parts[2]:

                    logs.append(
                        f"Removed redundant instruction: {line}"
                    )

                    i += 1
                    continue

        # =============================
        # Remove ADD/SUB by zero
        # =============================
        if (
            line.startswith("ADD")
            or line.startswith("SUB")
        ):

            parts = line.replace(",", " ").split()

            if len(parts) >= 3:

                if parts[2] == "0":

                    logs.append(
                        f"Removed useless arithmetic: {line}"
                    )

                    i += 1
                    continue

        # =============================
        # Remove duplicate NOP
        # =============================
        if line == "NOP":

            if optimized and optimized[-1] == "NOP":

                logs.append(
                    "Removed duplicate NOP"
                )

                i += 1
                continue

        # =============================
        # Constant folding
        # =============================
        if i + 1 < len(program):

            next_line = program[i + 1].strip()

            if (
                line.startswith("LDI")
                and next_line.startswith("ADD")
            ):

                p1 = line.replace(",", " ").split()
                p2 = next_line.replace(",", " ").split()

                if (
                    len(p1) >= 3
                    and len(p2) >= 3
                    and p1[1] == p2[1]
                    and p2[2].isdigit()
                ):

                    value = int(p1[2]) + int(p2[2])

                    new_instr = (
                        f"LDI {p1[1]}, {value}"
                    )

                    optimized.append(new_instr)

                    logs.append(
                        f"Constant folded: {line} + {next_line}"
                    )

                    i += 2
                    continue

        optimized.append(line)

        i += 1

    return optimized, logs