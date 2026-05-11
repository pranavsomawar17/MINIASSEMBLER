# backend/utils/helpers.py

import re

# =========================================
# SAFE STRING
# =========================================

def safe_string(value):

    # =====================================
    # LIST -> STRING
    # =====================================

    if isinstance(value, list):

        return " ".join(

            map(str, value)
        )

    # =====================================
    # NORMAL
    # =====================================

    return str(value)

# =========================================
# IS NUMBER
# =========================================

def is_number(value):

    try:

        int(value)

        return True

    except:

        return False

# =========================================
# CLEAN LINE
# =========================================

def clean_line(line):

    line = safe_string(line)

    # =====================================
    # REMOVE COMMENTS
    # =====================================

    if ";" in line:

        line = line.split(";")[0]

    return line.strip()

# =========================================
# SPLIT WORDS
# =========================================

def split_words(text):

    text = safe_string(text)

    return text.strip().split()

# =========================================
# FORMAT MACHINE CODE
# =========================================

def format_machine_code(

    address,

    opcode,

    operand=""
):

    operand = safe_string(operand)

    if operand:

        return (

            f"{address:03}  "

            f"{opcode}  "

            f"{operand}"
        )

    return (

        f"{address:03}  "

        f"{opcode}"
    )

# =========================================
# VALID IDENTIFIER
# =========================================

def is_valid_identifier(name):

    name = safe_string(name)

    pattern = r"^[A-Z_][A-Z0-9_]*$"

    return re.match(

        pattern,

        name
    ) is not None

# =========================================
# SAFE DIVIDE
# =========================================

def safe_divide(a, b):

    if b == 0:

        raise ZeroDivisionError(

            "Division by zero"
        )

    return a // b

# =========================================
# DEBUG MESSAGE
# =========================================

def debug_message(

    pc,

    instruction,

    registers=None
):

    instruction = safe_string(instruction)

    message = (

        f"[PC={pc}] "

        f"{instruction}"
    )

    if registers:

        register_text = []

        for key, value in registers.items():

            register_text.append(

                f"{key}={value}"
            )

        message += " | "

        message += ", ".join(

            register_text
        )

    return message

# =========================================
# MEMORY SNAPSHOT
# =========================================

def memory_snapshot(memory):

    lines = []

    for key, value in memory.items():

        lines.append(

            f"{key} = {value}"
        )

    return lines

# =========================================
# NORMALIZE SPACES
# =========================================

def normalize_spaces(text):

    text = safe_string(text)

    return " ".join(

        text.strip().split()
    )

# =========================================
# SAFE STRIP
# =========================================

def safe_strip(value):

    return safe_string(value).strip()

# =========================================
# SAFE LOWER
# =========================================

def safe_lower(value):

    return safe_string(value).lower()

# =========================================
# SAFE UPPER
# =========================================

def safe_upper(value):

    return safe_string(value).upper()