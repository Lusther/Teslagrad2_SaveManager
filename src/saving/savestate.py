import pickle

from memory.save_data_slot import SaveDataSlotData

class Savestate():
    def __init__(self, save_data: SaveDataSlotData) -> None:
        self.save_data = save_data

class SavestateManager():
    def __init__(self) -> None:
        self.savestate_list = {}
        self.savestate_list_changed_callback_list = []

    def add_savestate(self, savestate_name: str, savestate_data: SaveDataSlotData):
        self.savestate_list[savestate_name] = savestate_data
        self.on_savestate_list_changed()

    def remove_savestate(self, savestate_name: str):
        self.savestate_list.pop(savestate_name)
        self.on_savestate_list_changed()

    def save(self, path: str = "savestates.pickle"):
        with open(path, 'wb') as save_file:
            pickle.dump(self.savestate_list, save_file)  

    def load(self, path: str = "savestates.pickle"):
        try:
            with open(path, 'rb') as save_file:
                self.savestate_list = pickle.load(save_file)
            self.on_savestate_list_changed()
        except FileNotFoundError:
            pass

    def get_savestate(self, savestate_name: str):
        return self.savestate_list[savestate_name]

    def on_savestate_list_changed(self):
        for callback in self.savestate_list_changed_callback_list:
            callback()

    def register_on_savestate_list_changed(self, callback):
        self.savestate_list_changed_callback_list.append(callback)