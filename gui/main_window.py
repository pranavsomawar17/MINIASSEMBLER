import tkinter as tk
from tkinter import ttk
from core.assembler import Assembler
from core.executor import Executor

# ===== GRAPHITE THEME =====
BG = "#1e1e1e"
PANEL = "#252526"
BORDER = "#ffffff"

TEXT = "#d4d4d4"
DIM = "#888888"

FONT = ("Consolas", 11)


class SmartAssemblerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Assembler")
        self.root.geometry("1300x750")
        self.root.configure(bg=BG)

        self.executor = None
        self.history = []
        self.initialized = False
        self.symbol_table = {}

        self.setup_style()
        self.create_ui()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TNotebook", background=PANEL, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background="#2d2d2d",
            foreground=TEXT,
            padding=(10, 5),
            font=("Consolas", 10)
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", PANEL)],
            foreground=[("selected", TEXT)]
        )

    def create_ui(self):

        # ===== TOOLBAR =====
        toolbar = tk.Frame(self.root, bg=BG)
        toolbar.pack(fill="x", padx=12, pady=10)

        self.btn(toolbar, "Run", self.run_code)
        self.btn(toolbar, "|<| Previous", self.step_back)
        self.btn(toolbar, "Next |>|", self.step_forward)
        self.btn(toolbar, "Reset", self.reset)

        # ===== MAIN =====
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=12, pady=12)

        # 🔥 TRUE 50/50 FIX
        main.columnconfigure(0, weight=1, uniform="half")
        main.columnconfigure(1, weight=1, uniform="half")
        main.rowconfigure(0, weight=1)

        # ===== LEFT: EDITOR =====
        left = self.panel(main, "Code Editor")
        left.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        editor = tk.Frame(left, bg=PANEL)
        editor.pack(fill="both", expand=True, padx=16, pady=16)

        self.line_numbers = tk.Text(
            editor,
            width=4,
            bg="#2a2a2a",
            fg=DIM,
            state="disabled",
            font=FONT,
            bd=0,
            padx=6
        )
        self.line_numbers.pack(side="left", fill="y")

        self.text = tk.Text(
            editor,
            bg=PANEL,
            fg=TEXT,
            insertbackground=TEXT,
            font=FONT,
            bd=0,
            padx=14,
            pady=14
        )
        self.text.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(editor, command=self.sync_scroll)
        self.text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        self.text.bind("<MouseWheel>", self.on_scroll)
        self.text.bind("<KeyRelease>", self.update_line_numbers)

        self.update_line_numbers()
        self.text.tag_config("highlight", background="#3a3a3a")

        # ===== RIGHT SIDE =====
        right = tk.Frame(main, bg=BG)
        right.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)

        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=1)
        right.rowconfigure(1, weight=1)

        # ===== TOP RIGHT =====
        top = tk.Frame(right, bg=BG)
        top.grid(row=0, column=0, sticky="nsew")

        top.columnconfigure(0, weight=1, uniform="inner")
        top.columnconfigure(1, weight=1, uniform="inner")

        # REGISTER
        reg = self.panel(top, "Register")
        reg.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)

        reg_container = tk.Frame(reg, bg=PANEL)
        reg_container.pack(fill="both", expand=True, padx=16, pady=16)

        self.reg_labels = {}
        for i in range(8):
            lbl = tk.Label(
                reg_container,
                text=f"R{i} = 0",
                bg=PANEL,
                fg=TEXT,
                font=FONT
            )
            lbl.pack(anchor="w", pady=3)
            self.reg_labels[f"R{i}"] = lbl

        # MEMORY (READ ONLY)
        mem = self.panel(top, "Memory")
        mem.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)

        mem_container = tk.Frame(mem, bg=PANEL)
        mem_container.pack(fill="both", expand=True, padx=16, pady=16)

        self.mem = tk.Text(
            mem_container,
            bg=PANEL,
            fg=TEXT,
            font=FONT,
            bd=0,
            state="disabled"
        )
        self.mem.pack(side="left", fill="both", expand=True)

        scroll_mem = tk.Scrollbar(mem_container, command=self.mem.yview)
        self.mem.configure(yscrollcommand=scroll_mem.set)
        scroll_mem.pack(side="right", fill="y")

        # ===== OUTPUT =====
        bottom = self.panel(right, "Output Tables")
        bottom.grid(row=1, column=0, sticky="nsew", padx=12, pady=12)

        self.tabs = ttk.Notebook(bottom)

        self.output_tab = tk.Text(self.tabs, bg=PANEL, fg=TEXT, font=FONT, bd=0)
        self.machine_tab = tk.Text(self.tabs, bg=PANEL, fg=TEXT, font=FONT, bd=0)
        self.intermediate_tab = tk.Text(self.tabs, bg=PANEL, fg=TEXT, font=FONT, bd=0)
        self.optimize_tab = tk.Text(self.tabs, bg=PANEL, fg=TEXT, font=FONT, bd=0)

        self.tabs.add(self.output_tab, text="Output")
        self.tabs.add(self.machine_tab, text="Machine Code")
        self.tabs.add(self.intermediate_tab, text="Intermediate Code")
        self.tabs.add(self.optimize_tab, text="Optimization")

        self.tabs.pack(fill="both", expand=True, padx=12, pady=12)

    def panel(self, parent, title):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        tk.Label(frame, text=title, bg=PANEL, fg=TEXT, font=("Consolas", 12)).pack(pady=10)
        return frame

    def btn(self, parent, text, cmd):
        tk.Button(parent, text=text, command=cmd,
                  bg="#2d2d2d", fg=TEXT,
                  activebackground="#3a3a3a",
                  bd=1, padx=10, pady=5,
                  font=("Consolas", 10)).pack(side="left", padx=5)

    def sync_scroll(self, *args):
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    def on_scroll(self, event):
        self.text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.line_numbers.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    def update_line_numbers(self, event=None):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        lines = int(self.text.index("end-1c").split(".")[0])
        for i in range(1, lines + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")
        self.line_numbers.config(state="disabled")
        self.line_numbers.yview_moveto(self.text.yview()[0])

    def update_all(self):
        for r in self.executor.registers:
            self.reg_labels[r].config(text=f"{r} = {self.executor.registers[r]}")

        self.mem.config(state="normal")
        self.mem.delete("1.0", tk.END)
        for sym, addr in self.symbol_table.items():
            val = self.executor.memory.get(addr, 0)
            self.mem.insert(tk.END, f"{sym:<10} [{addr:03}] : {val}\n")
        self.mem.config(state="disabled")

        self.output_tab.delete("1.0", tk.END)
        self.output_tab.insert(tk.END, "Final Output:\n\n")
        for sym, addr in self.symbol_table.items():
            val = self.executor.memory.get(addr, 0)
            self.output_tab.insert(tk.END, f"{sym} = {val}\n")

    def init_execution(self):
        code = self.text.get("1.0", tk.END).strip().split("\n")
        assembler = Assembler()
        result = assembler.assemble(code)

        self.clear_tabs()

        if result.errors:
            for e in result.errors:
                self.output_tab.insert(tk.END, str(e) + "\n")
            return False

        self.machine_tab.insert(tk.END, "\n".join(result.machine_code))
        self.intermediate_tab.insert(tk.END, "\n".join(result.intermediate))

        self.executor = Executor(result.symbol_table)
        self.executor.load(code)

        self.history = []
        self.initialized = True
        self.symbol_table = result.symbol_table
        return True

    def run_code(self):
        if not self.init_execution():
            return
        while not self.executor.halted:
            self.executor.step()
        self.update_all()

    def step_forward(self):
        if not self.initialized:
            if not self.init_execution():
                return

        self.history.append({
            "pc": self.executor.pc,
            "registers": self.executor.registers.copy(),
            "memory": self.executor.memory.copy(),
            "flag": self.executor.zero_flag
        })

        self.executor.step()
        self.highlight_line()
        self.update_all()

    def step_back(self):
        if not self.history:
            return
        last = self.history.pop()
        self.executor.pc = last["pc"]
        self.executor.registers = last["registers"]
        self.executor.memory = last["memory"]
        self.executor.zero_flag = last["flag"]

        self.highlight_line()
        self.update_all()

    def reset(self):
        self.executor = None
        self.history = []
        self.initialized = False

        self.mem.config(state="normal")
        self.mem.delete("1.0", tk.END)
        self.mem.config(state="disabled")

        self.clear_tabs()

        for r in self.reg_labels:
            self.reg_labels[r].config(text=f"{r} = 0")

        self.text.tag_remove("highlight", "1.0", tk.END)

    def highlight_line(self):
        self.text.tag_remove("highlight", "1.0", tk.END)
        line = self.executor.pc + 1
        self.text.tag_add("highlight", f"{line}.0", f"{line}.end")
        self.text.see(f"{line}.0")

    def clear_tabs(self):
        self.output_tab.delete("1.0", tk.END)
        self.machine_tab.delete("1.0", tk.END)
        self.intermediate_tab.delete("1.0", tk.END)
        self.optimize_tab.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAssemblerGUI(root)
    root.mainloop()