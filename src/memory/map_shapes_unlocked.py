from dataclasses import dataclass
from .pointer import DeepPointer
from pymem.memory import allocate_memory
from .string import to_string_bytes

@dataclass
class MapShapesUnlockedData:
    items: list[str]

class MapShapesUnlockedMemory:
    def __init__(self, base_address, process_handle) -> None:
        self.process_handle = process_handle
        self.base_address = base_address

    def read(self) -> MapShapesUnlockedData:
        string_list = []
        for ptr in self.all_items_ptr:
            string_length = DeepPointer.from_pointer(ptr, 0x10).read_int(self.process_handle)
            # string_length = read_int(self.process_handle, ptr + 0x10)
            string_data = DeepPointer.from_pointer(ptr, 0x14).read_bytes(self.process_handle, string_length * 0x2)
            # string_data = read_bytes(self.process_handle, ptr + 0x14, string_length * 0x2)
            
            string = string_data.decode("utf-16")
            string_list.append(string)

        return MapShapesUnlockedData(string_list)
    
    def write(self, data: MapShapesUnlockedData):
        # self.size_ptr.write_int(self.process_handle, len(data.items))
        # # write_int(self.process_handle, self.base_address + 0x18, len(data.items))
        # for trigger, ptr in zip(data.items, self.all_items_ptr):

        #     DeepPointer.from_pointer(ptr, 0x10).write_int(self.process_handle, len(trigger))
        #     # write_int(self.process_handle, ptr+0x10, len(trigger))
        #     DeepPointer.from_pointer(ptr, 0x14).write_bytes(self.process_handle, trigger.encode("utf-16")[2:], len(trigger) * 0x2)
        #     # write_bytes(self.process_handle, ptr+0x14, trigger.encode("utf-16")[2:], len(trigger) * 0x2)

        string_header = DeepPointer.from_pointer(self.first_item_ptr, 0x0).read_bytes(self.process_handle, 0x10)

        if len(data.items) > self.count:
            old_items_size = 0x20+0x8*self.count
            old_items_content = DeepPointer.from_pointer(self.items_ptr, 0x0).read_bytes(self.process_handle, old_items_size)
            DeepPointer.from_pointer(self.items_ptr, 0x00).free(self.process_handle)
            new_items_adress = allocate_memory(self.process_handle, 0x20+0x8*300)
            self.items_ptr.write_longlong(self.process_handle, new_items_adress)
            DeepPointer.from_pointer(self.items_ptr, 0x0).write_bytes(self.process_handle, old_items_content, old_items_size)
            self.count_ptr.write_longlong(self.process_handle, 300)

        for item_ptr in self.all_items_ptr[:self.size]:
            DeepPointer.from_pointer(item_ptr, 0x0).free(self.process_handle)
        
        self.size_ptr.write_int(self.process_handle, len(data.items))

        for new_string, item_ptr in zip(data.items, self.all_items_ptr):
            new_adress = allocate_memory(self.process_handle, 0x14+len(new_string)*0x2)
            item_ptr.write_longlong(self.process_handle, new_adress)
            DeepPointer.from_pointer(item_ptr, 0x00).write_bytes(self.process_handle, string_header, 0x10)
            DeepPointer.from_pointer(item_ptr, 0x10).write_int(self.process_handle, len(new_string))
            DeepPointer.from_pointer(item_ptr, 0x14).write_bytes(self.process_handle, new_string.encode("utf-16")[2:], len(new_string)*0x2)

        

    @property
    def items_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.base_address, 0x10)
        # return read_ctype(self.process_handle, self.base_address + 0x10, c_void_p())

    @property
    def size_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.base_address, 0x18)
        # return read_int(self.process_handle, self.base_address + 0x18)

    @property 
    def size(self) -> int:
        return self.size_ptr.read_int(self.process_handle)

    @property
    def count_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.items_ptr, 0x18)
        # return read_short(self.process_handle, self.items + 0x18)

    @property 
    def count(self) -> int:
        return self.count_ptr.read_longlong(self.process_handle)
    
    @property
    def first_item_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.items_ptr, 0x20)
        # return self.items + 0x20
    
    @property
    def all_items_ptr(self) -> list[DeepPointer]:
        return [DeepPointer.from_pointer(self.items_ptr, offset) 
                for offset in range(0x20, 0x20 + self.size * 0x8, 0x8)]