from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor

class AsmHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        self.keyword_format = QTextCharFormat()
        self.keyword_format.setForeground(QColor("#569CD6"))

        self.register_format = QTextCharFormat()
        self.register_format.setForeground(QColor("#4EC9B0"))

        self.comment_format = QTextCharFormat()
        self.comment_format.setForeground(QColor("#6A9955"))

        self.keywords = ["LDI","LOAD","STORE","ADD","SUB","MUL","DIV",
                         "CMP","JMP","JZ","JNZ","HALT"]

    def highlightBlock(self, text):
        # keywords
        for word in self.keywords:
            if word in text:
                i = text.find(word)
                self.setFormat(i, len(word), self.keyword_format)

        # registers
        for i in range(8):
            reg = f"R{i}"
            if reg in text:
                idx = text.find(reg)
                self.setFormat(idx, len(reg), self.register_format)

        # comments
        if ";" in text:
            idx = text.find(";")
            self.setFormat(idx, len(text)-idx, self.comment_format)