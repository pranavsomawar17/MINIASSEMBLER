"""
Advanced Two-Pass Assembler
Supports:
- Labels
- Symbol Table
- Intermediate Code
- Machine Code
- Error Handling
- Directives
- Branch Resolution
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


# =========================================================
# Symbol Table
# =========================================================

class SymbolTable:
    def __init__(self):
        self._table: dict[str, int] = {}

    # -----------------------------------------
    # Add symbol
    # -----------------------------------------
    def add(self, symbol: str, address: int) -> Optional[str]:

        if symbol in self._table:
            return f"Duplicate symbol '{symbol}'"

        self._table[symbol] = address

        return None

    # -----------------------------------------
    # Get symbol
    # -----------------------------------------
    def get(self, symbol: str) -> Optional[int]:

        return self._table.get(symbol)

    # -----------------------------------------
    # Update symbol
    # -----------------------------------------
    def update(self, symbol: str, value: int):

        self._table[symbol] = value

    # -----------------------------------------
    # Clear table
    # -----------------------------------------
    def clear(self):

        self._table.clear()

    # -----------------------------------------
    # Return all
    # -----------------------------------------
    def all(self) -> dict[str, int]:

        return dict(self._table)


# =========================================================
# Opcode Table
# =========================================================

OPCODE_TABLE: dict[str, tuple[str, int]] = {

    # Data Transfer
    "LOAD": ("01", 2),
    "SAVE": ("02", 2),
    "ASSIGN": ("03", 2),
    "LDI": ("04", 2),

    # Arithmetic
    "+": ("10", 2),
    "-": ("11", 2),
    "*": ("12", 2),
    "/": ("13", 2),

    "INC": ("14", 1),
    "DEC": ("15", 1),

    # Logical
    "AND": ("20", 2),
    "OR": ("21", 2),
    "XOR": ("22", 2),
    "NOT": ("23", 1),

    "SHL": ("24", 2),
    "SHR": ("25", 2),

    # Branch
    "HOP": ("30", 1),
    "JZ": ("31", 1),
    "JNZ": ("32", 1),

    "JN": ("33", 1),
    "JP": ("34", 1),
    "JC": ("35", 1),

    "CALL": ("36", 1),
    "RET": ("37", 0),

    # Stack
    "PUSH": ("40", 1),
    "POP": ("41", 1),

    # IO
    "IN": ("50", 2),
    "OUT": ("51", 2),

    # Compare
    "CMP": ("60", 2),

    # Misc
    "NOP": ("F0", 0),
    "HALT": ("FF", 0),
}

DIRECTIVE_TABLE = {
    "START",
    "END",
    "DC",
    "DS",
    "ORG",
    "EQU",
}

VALID_REGISTERS = {
    "R0", "R1", "R2", "R3",
    "R4", "R5", "R6", "R7",
    "SP", "PC", "FLAGS"
}


# =========================================================
# Error Helpers
# =========================================================

@dataclass
class AssemblerError:
    line_no: int
    raw_line: str
    message: str
    severity: str = "ERROR"

    def __str__(self):

        return (
            f"[{self.severity}] "
            f"Line {self.line_no}: "
            f"{self.message} "
            f"→ `{self.raw_line.strip()}`"
        )


# =========================================================
# Assembly Result
# =========================================================

@dataclass
class AssemblyResult:

    machine_code: list[str] = field(default_factory=list)

    intermediate: list[str] = field(default_factory=list)

    errors: list[AssemblerError] = field(default_factory=list)

    symbol_table: dict[str, int] = field(default_factory=dict)

    @property
    def ok(self):

        return not any(
            e.severity == "ERROR"
            for e in self.errors
        )


# =========================================================
# Assembler
# =========================================================

class Assembler:

    def __init__(self):

        self.symbol_table = SymbolTable()

        self.opcode_table = OPCODE_TABLE

        self.errors: list[AssemblerError] = []

        self.machine_code: list[str] = []

        self.intermediate: list[str] = []

    # =====================================================
    # ERROR
    # =====================================================

    def _err(
        self,
        line_no: int,
        raw: str,
        msg: str,
        severity="ERROR"
    ):

        self.errors.append(
            AssemblerError(
                line_no,
                raw,
                msg,
                severity
            )
        )

    # =====================================================
    # HELPERS
    # =====================================================

    @staticmethod
    def _normalize(line: str) -> str:

        return line.split(";")[0].strip()

    @staticmethod
    def _strip_label(parts):

        if parts and parts[0].endswith(":"):

            return (
                parts[0][:-1],
                parts[1:]
            )

        return None, parts

    @staticmethod
    def _is_immediate(token: str):

        try:
            int(token, 0)
            return True

        except:
            return False

    @staticmethod
    def _parse_immediate(token: str):

        return int(token, 0)

    # =====================================================
    # RESERVED CHECK
    # =====================================================

    def _is_reserved(self, token: str):

        token = token.upper()

        return (
            token in DIRECTIVE_TABLE
            or token in self.opcode_table
            or token in VALID_REGISTERS
        )

    # =====================================================
    # RESOLVE OPERAND
    # =====================================================

    def _resolve_operand(
        self,
        operand: str,
        line_no: int,
        raw: str
    ):

        # -----------------------------------------
        # Valid Register
        # -----------------------------------------
        if operand in VALID_REGISTERS:
            return operand

        # -----------------------------------------
        # Invalid Register Detection
        # R9, R10 etc
        # -----------------------------------------
        if (
            len(operand) >= 2
            and operand[0] == "R"
            and operand[1:].isdigit()
            and operand not in VALID_REGISTERS
        ):

            self._err(
                line_no,
                raw,
                f"Invalid register '{operand}'"
            )

            return "ERR"

        # -----------------------------------------
        # Immediate
        # -----------------------------------------
        if self._is_immediate(operand):

            return str(
                self._parse_immediate(operand)
            )

        # -----------------------------------------
        # Symbol
        # -----------------------------------------
        addr = self.symbol_table.get(operand)

        if addr is None:

            self._err(
                line_no,
                raw,
                f"Undefined symbol '{operand}'"
            )

            return "ERR"

        return str(addr)

    # =====================================================
    # PASS 1
    # =====================================================

    def pass1(self, program):

        lc = 100

        for i, raw_line in enumerate(program, start=1):

            line = self._normalize(raw_line)

            if not line:
                continue

            parts = line.split()

            if not parts:
                continue

            label, parts = self._strip_label(parts)

            # -----------------------------------------
            # Register label
            # -----------------------------------------
            if label:

                if self._is_reserved(label):

                    self._err(
                        i,
                        raw_line,
                        (
                            f"Reserved word '{label}' "
                            f"cannot be used as label"
                        )
                    )

                else:

                    err = self.symbol_table.add(
                        label,
                        lc
                    )

                    if err:
                        self._err(
                            i,
                            raw_line,
                            err
                        )

            if not parts:
                continue

            op = parts[0].upper()

            # -----------------------------------------
            # START
            # -----------------------------------------
            if op == "START":

                if (
                    len(parts) > 1
                    and self._is_immediate(parts[1])
                ):

                    lc = self._parse_immediate(
                        parts[1]
                    )

                continue

            # -----------------------------------------
            # END
            # -----------------------------------------
            elif op == "END":
                break

            # -----------------------------------------
            # EQU
            # -----------------------------------------
            elif op == "EQU":

                if (
                    label
                    and len(parts) >= 2
                    and self._is_immediate(parts[1])
                ):

                    self.symbol_table.update(
                        label,
                        self._parse_immediate(parts[1])
                    )

                continue

            # -----------------------------------------
            # ORG
            # -----------------------------------------
            elif op == "ORG":

                if (
                    len(parts) > 1
                    and self._is_immediate(parts[1])
                ):

                    lc = self._parse_immediate(
                        parts[1]
                    )

                continue

            # -----------------------------------------
            # DC
            # -----------------------------------------
            elif op == "DC":

                lc += 1

            # -----------------------------------------
            # DS
            # -----------------------------------------
            elif op == "DS":

                n = 1

                if (
                    len(parts) > 1
                    and self._is_immediate(parts[1])
                ):

                    n = self._parse_immediate(
                        parts[1]
                    )

                lc += n

            # -----------------------------------------
            # Instruction
            # -----------------------------------------
            elif op in self.opcode_table:

                lc += 1

            # -----------------------------------------
            # Unknown
            # -----------------------------------------
            else:

                self._err(
                    i,
                    raw_line,
                    f"Unknown opcode '{op}'"
                )

                lc += 1

    # =====================================================
    # PASS 2
    # =====================================================

    def pass2(self, program):

        lc = 100

        self.machine_code = []

        self.intermediate = []

        for i, raw_line in enumerate(program, start=1):

            line = self._normalize(raw_line)

            if not line:
                continue

            parts = line.split()

            if not parts:
                continue

            label, parts = self._strip_label(parts)

            if not parts:
                continue

            op = parts[0].upper()

            # -----------------------------------------
            # START
            # -----------------------------------------
            if op == "START":

                if (
                    len(parts) > 1
                    and self._is_immediate(parts[1])
                ):

                    lc = self._parse_immediate(
                        parts[1]
                    )

                continue

            # -----------------------------------------
            # END
            # -----------------------------------------
            elif op == "END":
                break

            # -----------------------------------------
            # EQU / ORG
            # -----------------------------------------
            elif op in ("EQU", "ORG"):

                if (
                    op == "ORG"
                    and len(parts) > 1
                ):

                    lc = self._parse_immediate(
                        parts[1]
                    )

                continue

            # -----------------------------------------
            # DC
            # -----------------------------------------
            elif op == "DC":

                if len(parts) < 2:

                    self._err(
                        i,
                        raw_line,
                        "DC requires a value"
                    )

                    lc += 1
                    continue

                value = parts[1]

                if not self._is_immediate(value):

                    self._err(
                        i,
                        raw_line,
                        f"Invalid constant '{value}'"
                    )

                # Machine code
                self.machine_code.append(
                    f"{lc:04X}  {int(value):02X}"
                )

                # Intermediate
                if label:

                    self.intermediate.append(
                        f"(DC, {label}, {value})"
                    )

                else:

                    self.intermediate.append(
                        f"(DC, {value})"
                    )

                lc += 1

                continue

            # -----------------------------------------
            # DS
            # -----------------------------------------
            elif op == "DS":

                n = 1

                if (
                    len(parts) > 1
                    and self._is_immediate(parts[1])
                ):

                    n = self._parse_immediate(
                        parts[1]
                    )

                for j in range(n):

                    self.machine_code.append(
                        f"{lc+j:04X}  00"
                    )

                self.intermediate.append(
                    f"(DS, {n})"
                )

                lc += n

                continue

            # -----------------------------------------
            # Instructions
            # -----------------------------------------
            elif op in self.opcode_table:

                hex_code, operand_count = (
                    self.opcode_table[op]
                )

                operands = parts[1:]

                operands = [
                    o.rstrip(",")
                    for o in operands
                ]

                # Operand count validation
                if len(operands) < operand_count:

                    self._err(
                        i,
                        raw_line,
                        (
                            f"'{op}' expects "
                            f"{operand_count} operand(s)"
                        )
                    )

                    lc += 1
                    continue

                # Resolve operands
                resolved = [

                    self._resolve_operand(
                        operand,
                        i,
                        raw_line
                    )

                    for operand in operands[:operand_count]
                ]

                # Machine code
                mc = (
                    f"{lc:04X}  "
                    f"{hex_code}"
                )

                if resolved:

                    mc += "  " + " ".join(resolved)

                self.machine_code.append(mc)

                # Intermediate
                self.intermediate.append(
                    f"({op}, {', '.join(operands[:operand_count])})"
                )

                lc += 1

            # -----------------------------------------
            # Invalid opcode
            # -----------------------------------------
            else:

                self._err(
                    i,
                    raw_line,
                    f"Unknown opcode '{op}'"
                )

                lc += 1

    # =====================================================
    # ASSEMBLE
    # =====================================================

    def assemble(
        self,
        program: list[str]
    ) -> AssemblyResult:

        # Reset
        self.symbol_table.clear()

        self.errors = []

        self.machine_code = []

        self.intermediate = []

        # Passes
        self.pass1(program)

        self.pass2(program)

        # Return result
        return AssemblyResult(

            machine_code=self.machine_code,

            intermediate=self.intermediate,

            errors=self.errors,

            symbol_table=self.symbol_table.all(),
        )