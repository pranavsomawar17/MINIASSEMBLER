# =========================================
# SYMBOL TABLE
# =========================================

class SymbolTable:

    def __init__(self):

        self.table = {}

    # =====================================
    # ADD
    # =====================================

    def add(

        self,

        symbol,

        address
    ):

        self.table[symbol] = address

    # =====================================
    # GET
    # =====================================

    def get(self, symbol):

        return self.table.get(symbol)

    # =====================================
    # EXISTS
    # =====================================

    def exists(self, symbol):

        return symbol in self.table

    # =====================================
    # REMOVE
    # =====================================

    def remove(self, symbol):

        if symbol in self.table:

            del self.table[symbol]

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        self.table.clear()

    # =====================================
    # ITEMS
    # =====================================

    def items(self):

        return self.table.items()

    # =====================================
    # TO LIST
    # =====================================

    def to_list(self):

        result = []

        for symbol, address in self.table.items():

            result.append({

                "symbol": symbol,

                "address": address
            })

        return result


# =========================================
# LABEL TABLE
# =========================================

class LabelTable:

    def __init__(self):

        self.table = {}

    # =====================================
    # ADD
    # =====================================

    def add(

        self,

        label,

        address
    ):

        self.table[label] = address

    # =====================================
    # GET
    # =====================================

    def get(self, label):

        return self.table.get(label)

    # =====================================
    # EXISTS
    # =====================================

    def exists(self, label):

        return label in self.table

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        self.table.clear()

    # =====================================
    # TO LIST
    # =====================================

    def to_list(self):

        result = []

        for label, address in self.table.items():

            result.append({

                "label": label,

                "address": address
            })

        return result


# =========================================
# LITERAL TABLE
# =========================================

class LiteralTable:

    def __init__(self):

        self.table = {}

    # =====================================
    # ADD
    # =====================================

    def add(

        self,

        literal,

        value
    ):

        self.table[literal] = value

    # =====================================
    # GET
    # =====================================

    def get(self, literal):

        return self.table.get(literal)

    # =====================================
    # EXISTS
    # =====================================

    def exists(self, literal):

        return literal in self.table

    # =====================================
    # CLEAR
    # =====================================

    def clear(self):

        self.table.clear()

    # =====================================
    # TO LIST
    # =====================================

    def to_list(self):

        result = []

        for literal, value in self.table.items():

            result.append({

                "literal": literal,

                "value": value
            })

        return result


# =========================================
# OPCODE TABLE
# =========================================

OPCODE_TABLE = {

    "BEGIN": "00",

    "DECLARE": "01",

    "CONST": "02",

    "SET": "03",

    "LOAD": "04",

    "SAVE": "05",

    "ADD": "06",

    "SUB": "07",

    "MUL": "08",

    "DIV": "09",

    "SHOW": "0A",

    "READ": "0B",

    "CMP": "0C",

    "JL": "0D",

    "JG": "0E",

    "JE": "0F",

    "JMP": "10",

    "LABEL": "11",

    "HALT": "FF"
}