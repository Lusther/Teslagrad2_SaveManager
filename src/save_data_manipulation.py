from pymem.memory import read_bytes, write_bytes, read_longlong
import pymem
import pymem.process
import ctypes

TESLAGRAD_2_PROCESS_NAME = "Teslagrad 2"
module = "GameAssembly.dll"
base_offset = 0x3199E90
offset_1 = 0xB8
offset_2 = 0x10


class Process:
    def __init__(self, process_name) -> None:
        self.process_name = process_name

        self.handle = pymem.Pymem(self.process_name).process_handle


    def get_module_adress(self, module_name: str) ->  ctypes.c_void_p:
        return pymem.process.module_from_name(self.handle, module_name).lpBaseOfDll


class Teslagrad2(Process):

    def __init__(self) -> None:
        super().__init__(TESLAGRAD_2_PROCESS_NAME)

    def get_current_data_slot_adress(self):

        base_address = self.get_module_adress(module)

        pt1 = read_longlong(self.handle, base_address + base_offset)
        pt2 = read_longlong(self.handle, pt1 + offset_1)
        pt3 = read_longlong(self.handle, pt2 + offset_2)

        return pt3

    def get_save_data(self) -> bytes:

        save_data_adress = self.get_current_data_slot_adress()
        return read_bytes(self.handle, save_data_adress + 0x30, 0x38)
    
    def write_save_data(self, data: bytes):

        save_data_adress = self.get_current_data_slot_adress()
        write_bytes(self.handle, save_data_adress + 0x30, data, 0x38)
