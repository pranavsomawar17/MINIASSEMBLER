macros = {
    "INCR": ["LOAD {0}", "ADD 1", "STORE {0}"]
}

def expand(program):
    expanded = []
    for line in program:
        parts = line.split()
        if parts and parts[0] in macros:
            for stmt in macros[parts[0]]:
                expanded.append(stmt.format(parts[1]))
        else:
            expanded.append(line)
    return expanded