"""
GUI for Image_Converter

Author: Jormungandr
"""
import tkinter as tk
import os

path = "./Photos/to_ascii-tize/"

m = tk.Tk()
lb = tk.Listbox(m)
x = 0
for roots, dirs, files in os.walk(path):
    for file in files:
        lb.insert(x, file.split(".")[0])
        print(file)
        x += 1
button1 = tk.Button()
lb.pack()
m.mainloop()
