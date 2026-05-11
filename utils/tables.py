class SymbolTable:
    def __init__(self):
        self.table = {}

    # =============================
    # Add symbol
    # =============================
    def add(self, symbol, address):

        if symbol in self.table:
            return False

        self.table[symbol] = address

        return True

    # =============================
    # Get symbol address
    # =============================
    def get(self, symbol):

        return self.table.get(symbol)

    # =============================
    # Check symbol exists
    # =============================
    def exists(self, symbol):

        return symbol in self.table

    # =============================
    # Remove symbol
    # =============================
    def remove(self, symbol):

        if symbol in self.table:
            del self.table[symbol]

    # =============================
    # Clear table
    # =============================
    def clear(self):

        self.table.clear()

    # =============================
    # Return all symbols
    # =============================
    def all(self):

        return self.table

    # =============================
    # Length
    # =============================
    def __len__(self):

        return len(self.table)

    # =============================
    # String representation
    # =============================
    def __str__(self):

        output = []

        for sym, addr in self.table.items():
            output.append(f"{sym} -> {addr}")

        return "\n".join(output)


# ==========================================
# OPCODE TABLE
# ==========================================

OPCODE_TABLE = {
    "LOAD": ("01", 2),
    "STORE": ("02", 2),
    "MOV": ("03", 2),
    "LDI": ("04", 2),

    "ADD": ("10", 2),
    "SUB": ("11", 2),
    "MUL": ("12", 2),
    "DIV": ("13", 2),

    "CMP": ("20", 2),

    "JMP": ("30", 1),
    "JZ": ("31", 1),
    "JNZ": ("32", 1),

    "PUSH": ("40", 1),
    "POP": ("41", 1),

    "NOP": ("F0", 0),
    "HALT": ("FF", 0),
}


# ==========================================
# REGISTERS
# ==========================================

REGISTERS = {
    f"R{i}" for i in range(8)
}


# ==========================================
# DIRECTIVES
# ==========================================

DIRECTIVES = {
    "START",
    "END",
    "DC",
    "DS",
    "ORG",
    "EQU",
}