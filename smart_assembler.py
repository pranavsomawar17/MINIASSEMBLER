import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# ------------------ SIMPLE ASSEMBLER LOGIC ------------------

class Assembler:
    def __init__(self):
        self.opcode = {"LOAD": "01", "ADD": "02", "STORE": "03"}
        self.symbol_table = {}
        self.errors = []
        self.intermediate = []
        self.machine_code = []
        self.debug_steps = []
        self.optimization_log = []

    def reset(self):
        self.symbol_table.clear()
        self.errors.clear()
        self.intermediate.clear()
        self.machine_code.clear()
        self.debug_steps.clear()
        self.optimization_log.clear()

    def suggest(self, word):
        for op in self.opcode:
            if word[0] == op[0]:
                return op
        return None

    def optimize(self, program):
        optimized = []
        for line in program:
            if "ADD 0" in line:
                self.optimization_log.append(f"Removed redundant '{line}'")
                continue
            optimized.append(line)
        return optimized

    def pass1(self, program):
        lc = 100
        for line in program:
            parts = line.split()
            if len(parts) == 3:  # declarative
                self.symbol_table[parts[0]] = lc
            lc += 1

    def pass2(self, program):
        lc = 100
        acc = 0

        for i, line in enumerate(program):
            parts = line.split()

            if parts[0] in self.opcode:
                if parts[1] not in self.symbol_table:
                    self.errors.append(f"Line {i+1}: Undefined symbol {parts[1]}")
                    continue

                code = f"{lc} {self.opcode[parts[0]]} {self.symbol_table[parts[1]]}"
                self.machine_code.append(code)
                self.intermediate.append(f"({parts[0]}, {parts[1]})")

                # Debug simulation
                if parts[0] == "LOAD":
                    acc = 5
                elif parts[0] == "ADD":
                    acc += 10
                elif parts[0] == "STORE":
                    pass

                self.debug_steps.append(f"{parts[0]} {parts[1]} → ACC = {acc}")

            elif parts[0] not in ["START", "END"]:
                suggestion = self.suggest(parts[0])
                msg = f"Line {i+1}: Invalid opcode {parts[0]}"
                if suggestion:
                    msg += f" (Did you mean {suggestion}?)"
                self.errors.append(msg)

            lc += 1

    def assemble(self, code):
        self.reset()
        program = [line.strip() for line in code.split("\n") if line.strip()]

        program = self.optimize(program)
        self.pass1(program)
        self.pass2(program)


# ------------------ GUI ------------------

class SmartAssemblerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SmartASM - Intelligent Assembler")
        self.setGeometry(100, 100, 1200, 700)

        self.assembler = Assembler()
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        # LEFT: Code Editor
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Courier", 12))
        self.editor.setPlaceholderText("Write your MiniASM code here...")

        # RIGHT: Tabs
        self.tabs = QTabWidget()

        self.symbol_tab = QTableWidget()
        self.symbol_tab.setColumnCount(2)
        self.symbol_tab.setHorizontalHeaderLabels(["Symbol", "Address"])

        self.intermediate_tab = QTextEdit()
        self.machine_tab = QTextEdit()
        self.error_tab = QTextEdit()
        self.debug_tab = QTextEdit()
        self.optimize_tab = QTextEdit()

        self.tabs.addTab(self.symbol_tab, "Symbol Table")
        self.tabs.addTab(self.intermediate_tab, "Intermediate")
        self.tabs.addTab(self.machine_tab, "Machine Code")
        self.tabs.addTab(self.error_tab, "Errors")
        self.tabs.addTab(self.debug_tab, "Debug")
        self.tabs.addTab(self.optimize_tab, "Optimization")

        main_layout.addWidget(self.editor, 2)
        main_layout.addWidget(self.tabs, 3)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Toolbar
        toolbar = self.addToolBar("Toolbar")

        run_btn = QAction("Run", self)
        run_btn.triggered.connect(self.run_code)

        step_btn = QAction("Step", self)
        step_btn.triggered.connect(self.step_debug)

        optimize_btn = QAction("Optimize", self)
        optimize_btn.triggered.connect(self.run_code)

        load_btn = QAction("Load", self)
        load_btn.triggered.connect(self.load_file)

        save_btn = QAction("Save", self)
        save_btn.triggered.connect(self.save_file)

        toolbar.addAction(run_btn)
        toolbar.addAction(step_btn)
        toolbar.addAction(optimize_btn)
        toolbar.addAction(load_btn)
        toolbar.addAction(save_btn)

        # Status bar
        self.statusBar().showMessage("Ready")

    def run_code(self):
        code = self.editor.toPlainText()
        self.assembler.assemble(code)

        self.update_symbol_table()
        self.intermediate_tab.setText("\n".join(self.assembler.intermediate))
        self.machine_tab.setText("\n".join(self.assembler.machine_code))
        self.error_tab.setText("\n".join(self.assembler.errors))
        self.debug_tab.setText("\n".join(self.assembler.debug_steps))
        self.optimize_tab.setText("\n".join(self.assembler.optimization_log))

        self.statusBar().showMessage("Execution Completed")

    def step_debug(self):
        self.debug_tab.append("Step execution not fully implemented (demo)")

    def update_symbol_table(self):
        self.symbol_tab.setRowCount(len(self.assembler.symbol_table))
        for i, (sym, addr) in enumerate(self.assembler.symbol_table.items()):
            self.symbol_tab.setItem(i, 0, QTableWidgetItem(sym))
            self.symbol_tab.setItem(i, 1, QTableWidgetItem(str(addr)))

    def load_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if fname:
            with open(fname, "r") as f:
                self.editor.setText(f.read())

    def save_file(self):
        fname, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if fname:
            with open(fname, "w") as f:
                f.write(self.editor.toPlainText())


# ------------------ RUN ------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartAssemblerGUI()
    window.show()
    sys.exit(app.exec_())