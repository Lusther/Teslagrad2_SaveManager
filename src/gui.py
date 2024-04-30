import tkinter as tk
import pymem
from memory.save_data_slot import SaveDataSlotMemory
from memory.pointer import DeepPointer
from saving.savestate import SavestateManager
from tkinter.ttk import Combobox

def quicksave_event():
    global data
    data = save_data_slot_memory.read()
    print(data)

def quickload_event():
    global data
    save_data_slot_memory.write(data)

    print("Quickload Successful !")

def create_savestate():
    data = save_data_slot_memory.read()
    savestate_manager.add_savestate(selected_var.get(), data)

def load_savestate():
    save_data_slot = savestate_manager.get_savestate(selected_var.get())
    save_data_slot_memory.write(save_data_slot)

def on_closing():
    savestate_manager.save()
    root.destroy()


def update_options():
    # Get the new options from somewhere, for example, a list
    new_options = list(savestate_manager.savestate_list.keys())
    
    # Update the values of the Combobox
    combobox['values'] = new_options
    
    # Set the current selection to the first option
    combobox.current(0)

TESLAGRAD_2_PROCESS_NAME = "Teslagrad 2"
MODULE_NAME = "GameAssembly.dll"

savestate_manager = SavestateManager()
savestate_manager.register_on_savestate_list_changed(update_options)


process_handle = pymem.Pymem(TESLAGRAD_2_PROCESS_NAME).process_handle
module_adress = pymem.process.module_from_name(process_handle, MODULE_NAME).lpBaseOfDll
save_data_slot_memory = SaveDataSlotMemory(DeepPointer(module_adress, 0x3199E90, 0xB8, 0x10), process_handle)


# Create the main window
root = tk.Tk()
root.title("Teslagrad 2 Training Tool")

# Configure window size
root.geometry("400x100")

# Create the buttons
button1 = tk.Button(root, text="QuickSave", command=quicksave_event)
button2 = tk.Button(root, text="QuickLoad", command=quickload_event)
button3 = tk.Button(root, text="Load Savestate", command=load_savestate)
button4 = tk.Button(root, text="Create Savestate", command=create_savestate)

selected_var = tk.StringVar() 
combobox = Combobox(root, textvariable=selected_var)

combobox['values'] = list(savestate_manager.savestate_list.keys())
print()

# Place the buttons in a grid layout
button1.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
button2.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

combobox.grid(row=1, column=0)
button3.grid(row=1, column=1)
button4.grid(row=2, column=1)

# Configure grid to make buttons span the whole window
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)

savestate_manager.load()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter event loop
root.mainloop()
