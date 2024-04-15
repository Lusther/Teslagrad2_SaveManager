import tkinter as tk
from save_data_manipulation import Teslagrad2


teslagrad = Teslagrad2()

def quicksave_event():
    global data
    data = teslagrad.get_save_data()
    print(data)

def quickload_event():
    global data
    teslagrad.write_save_data(data)

# Create the main window
root = tk.Tk()
root.title("Teslagrad 2 Training Tool")

# Configure window size
root.geometry("400x100")

# Create the buttons
button1 = tk.Button(root, text="QuickSave", command=quicksave_event)
button2 = tk.Button(root, text="QuickLoad", command=quickload_event)

# Place the buttons in a grid layout
button1.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
button2.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

# Configure grid to make buttons span the whole window
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

# Start the Tkinter event loop
root.mainloop()
