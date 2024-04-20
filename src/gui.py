import tkinter as tk
import pymem
from memory.save_data_slot import SaveDataSlotMemory
from memory.pointer import DeepPointer

TESLAGRAD_2_PROCESS_NAME = "Teslagrad 2"
MODULE_NAME = "GameAssembly.dll"

process_handle = pymem.Pymem(TESLAGRAD_2_PROCESS_NAME).process_handle
module_adress = pymem.process.module_from_name(process_handle, MODULE_NAME).lpBaseOfDll
save_data_slot_memory = SaveDataSlotMemory(DeepPointer(module_adress, 0x3199E90, 0xB8, 0x10), process_handle)

def quicksave_event():
    global data
    data = save_data_slot_memory.read()
    print(data)

def quickload_event():
    global data
    save_data_slot_memory.write(data)

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
