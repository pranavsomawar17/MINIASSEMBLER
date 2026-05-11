class Diagnostic:

    def __init__(

        self,

        severity,

        line,

        message,

        suggestion=""
    ):

        self.severity = severity

        self.line = line

        self.message = message

        self.suggestion = suggestion

    # =====================================
    # TO DICT
    # =====================================

    def to_dict(self):

        return {

            "severity": self.severity,

            "line": self.line,

            "message": self.message,

            "suggestion": self.suggestion
        }

    # =====================================
    # STRING
    # =====================================

    def __str__(self):

        return (

            f"[{self.severity}] "

            f"Line {self.line}: "

            f"{self.message}"
        )