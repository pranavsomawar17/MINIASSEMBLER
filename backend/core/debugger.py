# backend/core/debugger.py

class Debugger:

    def step(self, code, pc):

        if pc >= len(code):

            return {

                "done": True,

                "debug": "Execution finished"
            }

        line = code[pc]

        # =================================
        # SAFE STRING
        # =================================

        if isinstance(line, list):

            line = " ".join(

                map(str, line)
            )

        line = str(line)

        return {

            "done": False,

            "pc": pc + 1,

            "debug": f"[PC={pc}] {line}"
        }