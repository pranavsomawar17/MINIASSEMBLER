; ===== SMARTASM ADVANCED TEST =====

START 100

; Load immediate values
LDI R1, 10
LDI R2, 20

; Arithmetic
ADD R1, R2
SUB R2, R1
MUL R1, R2
DIV R2, R1

; Logical
AND R1, R2
OR R1, R2
XOR R1, R2
NOT R1

; Shift
SHL R1, 1
SHR R2, 1

; Memory usage
STORE R1, DATA1
LOAD R3, DATA1

; Stack operations
PUSH R1
POP R4

; Comparison
CMP R1, R2

; Conditional jumps
JZ ZERO_LABEL
JNZ NONZERO_LABEL

; Labels
ZERO_LABEL:
    LDI R5, 0
    JMP END_LABEL

NONZERO_LABEL:
    LDI R5, 1

END_LABEL:
    NOP

; Data section
DATA1: DC 5
ARRAY: DS 3

HALT
END