import tkinter as tk
from gui.main_window import SmartAssemblerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartAssemblerGUI(root)
    root.mainloop()