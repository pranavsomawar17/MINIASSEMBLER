# backend/core/executor.py

# =========================================
# EXECUTOR
# =========================================

class Executor:

    # =====================================
    # INIT
    # =====================================

    def __init__(self):

        self.reset()

    # =====================================
    # RESET
    # =====================================

    def reset(self):

        self.memory = {}

        self.output = []

        self.debug = []

        self.pc = 0

        self.last_result = 0

        self.zero_flag = False

    # =====================================
    # VALUE
    # =====================================

    def get_value(self, value):

        try:

            return int(value)

        except:

            return self.memory.get(

                value,

                0
            )

    # =====================================
    # FIND LABEL
    # =====================================

    def find_label(

        self,

        code,

        label
    ):

        for index, line in enumerate(code):

            line = str(line)

            if line.startswith(

                f"LABEL {label}"
            ):

                return index

        return -1

    # =====================================
    # RUN
    # =====================================

    def run(self, code):

        self.reset()

        while self.pc < len(code):

            line = str(code[self.pc]).strip()

            # =============================
            # EMPTY
            # =============================

            if not line:

                self.pc += 1

                continue

            parts = line.split()

            instruction = parts[0]

            # =============================
            # DEBUG
            # =============================

            self.debug.append(

                f"[PC={self.pc}] {line}"
            )

            # =================================
            # BEGIN
            # =================================

            if instruction in [

                "BEGIN",

                "HELLO"
            ]:

                pass

            # =================================
            # DECLARE
            # =================================

            elif instruction == "DECLARE":

                variable = parts[1]

                if variable not in self.memory:

                    self.memory[variable] = 0

            # =================================
            # SET
            # =================================

            elif instruction == "SET":

                variable = parts[1]

                value = self.get_value(

                    parts[2]
                )

                self.memory[variable] = value

            # =================================
            # ADD
            # =================================

            elif instruction == "ADD":

                left = self.get_value(

                    parts[1]
                )

                right = self.get_value(

                    parts[2]
                )

                self.last_result = (

                    left + right
                )

            # =================================
            # SUB
            # =================================

            elif instruction == "SUB":

                left = self.get_value(

                    parts[1]
                )

                right = self.get_value(

                    parts[2]
                )

                self.last_result = (

                    left - right
                )

            # =================================
            # MUL
            # =================================

            elif instruction == "MUL":

                left = self.get_value(

                    parts[1]
                )

                right = self.get_value(

                    parts[2]
                )

                self.last_result = (

                    left * right
                )

            # =================================
            # DIV
            # =================================

            elif instruction == "DIV":

                left = self.get_value(

                    parts[1]
                )

                right = self.get_value(

                    parts[2]
                )

                if right != 0:

                    self.last_result = (

                        left // right
                    )

            # =================================
            # SAVE
            # =================================

            elif instruction == "SAVE":

                variable = parts[1]

                self.memory[variable] = (

                    self.last_result
                )

            # =================================
            # CMP
            # =================================

            elif instruction == "CMP":

                left = self.get_value(

                    parts[1]
                )

                right = self.get_value(

                    parts[2]
                )

                self.zero_flag = (

                    left == right
                )

            # =================================
            # LABEL
            # =================================

            elif instruction == "LABEL":

                pass

            # =================================
            # JZ
            # =================================

            elif instruction == "JZ":

                target = parts[1]

                if self.zero_flag:

                    target_pc = self.find_label(

                        code,

                        target
                    )

                    if target_pc != -1:

                        self.pc = target_pc

                        continue

            # =================================
            # JNZ
            # =================================

            elif instruction == "JNZ":

                target = parts[1]

                if not self.zero_flag:

                    target_pc = self.find_label(

                        code,

                        target
                    )

                    if target_pc != -1:

                        self.pc = target_pc

                        continue

            # =================================
            # HOP
            # =================================

            elif instruction == "HOP":

                target = parts[1]

                target_pc = self.find_label(

                    code,

                    target
                )

                if target_pc != -1:

                    self.pc = target_pc

                    continue

            # =================================
            # SHOW
            # =================================

            elif instruction == "SHOW":

                variable = parts[1]

                value = self.get_value(

                    variable
                )

                self.output.append(

                    str(value)
                )

            # =================================
            # HALT
            # =================================

            elif instruction in [

                "HALT",

                "TERMINATE",

                "PAUSE"
            ]:

                break

            # =================================
            # NEXT
            # =================================

            self.pc += 1

        # =====================================
        # RETURN
        # =====================================

        return {

            "output": self.output,

            "memory": self.memory,

            "debug": self.debug,

            "registers": {

                "ACC": self.last_result,

                "PC": self.pc,

                "FLAG": self.zero_flag
            }
        }