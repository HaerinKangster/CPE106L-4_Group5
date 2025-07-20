import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(
    title="Select a text file",
    filetypes=[("Text Files", "*.txt")]
)

if file_path:
    print("Selected file:", file_path)
else:
    print("No file selected.")
