from dataclasses import dataclass
from .pointer import DeepPointer

@dataclass
class TriggersSetData:
    items: list[str]

class TriggersSetMemory:
    def __init__(self, base_address, process_handle) -> None:
        self.process_handle = process_handle
        self.base_address = base_address

    def read(self) -> TriggersSetData:
        string_list = []
        for ptr in self.all_items_ptr:
            string_length = DeepPointer.from_pointer(ptr, 0x10).read_int(self.process_handle)
            # string_length = read_int(self.process_handle, ptr + 0x10)
            string_data = DeepPointer.from_pointer(ptr, 0x14).read_bytes(self.process_handle, string_length * 0x2)
            # string_data = read_bytes(self.process_handle, ptr + 0x14, string_length * 0x2)
            
            string = string_data.decode("utf-16")
            string_list.append(string)

        return TriggersSetData(string_list)
    
    def write(self, data: TriggersSetData):
        self.size_ptr.write_int(self.process_handle, len(data.items))
        # write_int(self.process_handle, self.base_address + 0x18, len(data.items))
        for trigger, ptr in zip(data.items, self.all_items_ptr):

            DeepPointer.from_pointer(ptr, 0x10).write_int(self.process_handle, len(trigger))
            # write_int(self.process_handle, ptr+0x10, len(trigger))
            DeepPointer.from_pointer(ptr, 0x14).write_bytes(self.process_handle, trigger.encode("utf-16")[2:], len(trigger) * 0x2)
            # write_bytes(self.process_handle, ptr+0x14, trigger.encode("utf-16")[2:], len(trigger) * 0x2)

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
        return self.count_ptr.read_short(self.process_handle)
    
    @property
    def first_item_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.items_ptr, 0x20)
        # return self.items + 0x20
    
    @property
    def all_items_ptr(self) -> list[DeepPointer]:
        return [DeepPointer.from_pointer(self.items_ptr, offset) 
                for offset in range(0x20, 0x20 + self.size * 0x8, 0x8)]
        
    