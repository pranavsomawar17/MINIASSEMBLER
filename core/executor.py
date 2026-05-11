class Executor:

    # =====================================================
    # INIT
    # =====================================================
    def __init__(self, symbol_table):

        # Registers
        self.registers = {
            f"R{i}": 0 for i in range(8)
        }

        # Memory
        self.memory = {}

        # Stack
        self.stack = []

        # Symbol table
        self.symbol_table = symbol_table

        # Program counter
        self.pc = 0

        # Flags
        self.zero_flag = False

        # Halt state
        self.halted = False

        # Loaded instructions
        self.program = []

        # Labels
        self.labels = {}

        # PC -> editor line mapping
        self.line_map = {}

        # Debug history
        self.history = []

    # =====================================================
    # LOAD PROGRAM
    # =====================================================
    def load(self, program):

        self.program = []

        self.labels = {}

        self.line_map = {}

        self.history = []

        self.pc = 0

        self.halted = False

        self.zero_flag = False

        self.stack = []

        # -----------------------------------------
        # Initialize memory
        # -----------------------------------------
        for sym, addr in self.symbol_table.items():

            self.memory[addr] = 0

        # -----------------------------------------
        # Parse program
        # -----------------------------------------
        for original_index, line in enumerate(program):

            line = line.strip()

            # Empty
            if not line:
                continue

            # Comment
            if line.startswith(";"):
                continue

            # Inline comments
            if ";" in line:
                line = line.split(";")[0].strip()

            # START / END
            if line.startswith("START") or line == "END":
                continue

            # -----------------------------------------
            # DC
            # -----------------------------------------
            if "DC" in line:

                if ":" in line:

                    label, rest = line.split(":", 1)

                    parts = rest.strip().split()

                    if len(parts) >= 2:

                        value = int(parts[1])

                        if label.strip() in self.symbol_table:

                            addr = self.symbol_table[
                                label.strip()
                            ]

                            self.memory[addr] = value

                continue

            # -----------------------------------------
            # DS
            # -----------------------------------------
            if "DS" in line:
                continue

            # -----------------------------------------
            # Label
            # -----------------------------------------
            if ":" in line:

                label, rest = line.split(":", 1)

                self.labels[label.strip()] = len(
                    self.program
                )

                if rest.strip():

                    self.line_map[
                        len(self.program)
                    ] = original_index

                    self.program.append(
                        rest.strip()
                    )

                continue

            # -----------------------------------------
            # Normal instruction
            # -----------------------------------------
            self.line_map[
                len(self.program)
            ] = original_index

            self.program.append(line)

    # =====================================================
    # GET VALUE
    # =====================================================
    def get_value(self, token):

        token = token.strip()

        # Register
        if token in self.registers:
            return self.registers[token]

        # Positive number
        if token.isdigit():
            return int(token)

        # Negative number
        if (
            token.startswith("-")
            and token[1:].isdigit()
        ):
            return int(token)

        # Symbol
        if token in self.symbol_table:

            addr = self.symbol_table[token]

            return self.memory.get(addr, 0)

        return 0

    # =====================================================
    # SAVE DEBUG STATE
    # =====================================================
    def save_state(self):

        snapshot = {

            "pc": self.pc,

            "registers": self.registers.copy(),

            "memory": self.memory.copy(),

            "stack": self.stack.copy(),

            "zero_flag": self.zero_flag,

            "halted": self.halted,
        }

        self.history.append(snapshot)

    # =====================================================
    # RESTORE PREVIOUS STATE
    # =====================================================
    def restore_previous(self):

        if not self.history:
            return

        snapshot = self.history.pop()

        self.pc = snapshot["pc"]

        self.registers = snapshot["registers"]

        self.memory = snapshot["memory"]

        self.stack = snapshot["stack"]

        self.zero_flag = snapshot["zero_flag"]

        self.halted = snapshot["halted"]

    # =====================================================
    # STEP EXECUTION
    # =====================================================
    def step(self):

        # Halted
        if self.halted:
            return

        # Program ended
        if self.pc >= len(self.program):

            self.halted = True
            return

        # Save debugger state
        self.save_state()

        # Current instruction
        line = self.program[self.pc]

        line = line.replace(",", " ")

        parts = line.split()

        if not parts:

            self.pc += 1
            return

        op = parts[0].upper()

        try:

            # ==========================================
            # LDI
            # ==========================================
            if op == "LDI":

                self.registers[parts[1]] = int(parts[2])

            # ==========================================
            # LOAD
            # ==========================================
            elif op == "LOAD":

                self.registers[parts[1]] = (
                    self.get_value(parts[2])
                )

            # ==========================================
            # STORE
            # ==========================================
            elif op == "STORE":

                reg = parts[1]

                dest = parts[2]

                if dest in self.symbol_table:

                    addr = self.symbol_table[dest]

                    self.memory[addr] = (
                        self.registers[reg]
                    )

            # ==========================================
            # MOV
            # ==========================================
            elif op == "MOV":

                self.registers[parts[1]] = (
                    self.get_value(parts[2])
                )

            # ==========================================
            # ADD
            # ==========================================
            elif op == "ADD":

                self.registers[parts[1]] += (
                    self.get_value(parts[2])
                )

            # ==========================================
            # SUB
            # ==========================================
            elif op == "SUB":

                self.registers[parts[1]] -= (
                    self.get_value(parts[2])
                )

            # ==========================================
            # MUL
            # ==========================================
            elif op == "MUL":

                self.registers[parts[1]] *= (
                    self.get_value(parts[2])
                )

            # ==========================================
            # DIV
            # ==========================================
            elif op == "DIV":

                divisor = self.get_value(parts[2])

                if divisor == 0:
                    raise Exception(
                        "Division by zero"
                    )

                self.registers[parts[1]] //= divisor

            # ==========================================
            # INC
            # ==========================================
            elif op == "INC":

                self.registers[parts[1]] += 1

            # ==========================================
            # DEC
            # ==========================================
            elif op == "DEC":

                self.registers[parts[1]] -= 1

            # ==========================================
            # AND
            # ==========================================
            elif op == "AND":

                self.registers[parts[1]] &= (
                    self.get_value(parts[2])
                )

            # ==========================================
            # OR
            # ==========================================
            elif op == "OR":

                self.registers[parts[1]] |= (
                    self.get_value(parts[2])
                )

            # ==========================================
            # XOR
            # ==========================================
            elif op == "XOR":

                self.registers[parts[1]] ^= (
                    self.get_value(parts[2])
                )

            # ==========================================
            # NOT
            # ==========================================
            elif op == "NOT":

                self.registers[parts[1]] = (
                    ~self.registers[parts[1]]
                )

            # ==========================================
            # SHL
            # ==========================================
            elif op == "SHL":

                self.registers[parts[1]] <<= (
                    self.get_value(parts[2])
                )

            # ==========================================
            # SHR
            # ==========================================
            elif op == "SHR":

                self.registers[parts[1]] >>= (
                    self.get_value(parts[2])
                )

            # ==========================================
            # PUSH
            # ==========================================
            elif op == "PUSH":

                self.stack.append(
                    self.registers[parts[1]]
                )

            # ==========================================
            # POP
            # ==========================================
            elif op == "POP":

                if not self.stack:

                    raise Exception(
                        "Stack underflow"
                    )

                self.registers[parts[1]] = (
                    self.stack.pop()
                )

            # ==========================================
            # CMP
            # ==========================================
            elif op == "CMP":

                self.zero_flag = (

                    self.get_value(parts[1])
                    ==
                    self.get_value(parts[2])

                )

            # ==========================================
            # JMP
            # ==========================================
            elif op == "JMP":

                label = parts[1]

                if label not in self.labels:

                    raise Exception(
                        f"Unknown label '{label}'"
                    )

                self.pc = self.labels[label]

                return

            # ==========================================
            # JZ
            # ==========================================
            elif op == "JZ":

                label = parts[1]

                if self.zero_flag:

                    if label not in self.labels:

                        raise Exception(
                            f"Unknown label '{label}'"
                        )

                    self.pc = self.labels[label]

                    return

            # ==========================================
            # JNZ
            # ==========================================
            elif op == "JNZ":

                label = parts[1]

                if not self.zero_flag:

                    if label not in self.labels:

                        raise Exception(
                            f"Unknown label '{label}'"
                        )

                    self.pc = self.labels[label]

                    return

            # ==========================================
            # NOP
            # ==========================================
            elif op == "NOP":

                pass

            # ==========================================
            # HALT
            # ==========================================
            elif op == "HALT":

                self.halted = True
                return

            # ==========================================
            # UNKNOWN
            # ==========================================
            else:

                raise Exception(
                    f"Unknown instruction: {op}"
                )

        except Exception as e:

            self.halted = True

            raise e

        # Next instruction
        self.pc += 1

    # =====================================================
    # RUN PROGRAM
    # =====================================================
    def run(self):

        while not self.halted:

            self.step()

    # =====================================================
    # RESET
    # =====================================================
    def reset(self):

        self.registers = {
            f"R{i}": 0 for i in range(8)
        }

        self.memory = {}

        self.stack = []

        self.pc = 0

        self.zero_flag = False

        self.halted = False

        self.history = []