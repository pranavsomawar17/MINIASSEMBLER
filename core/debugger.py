def debug(program):

    debug_info = []

    pc = 0

    for line in program:

        line = line.strip()

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
        # Ignore directives
        # =============================
        if (
            line.startswith("START")
            or line == "END"
        ):
            continue

        # =============================
        # Ignore data declarations
        # =============================
        if "DC" in line or "DS" in line:
            continue

        debug_info.append(
            f"PC {pc} -> {line}"
        )

        pc += 1

    return debug_info