from dataclasses import dataclass
import struct
from .pointer import DeepPointer
from pymem.memory import allocate_memory

@dataclass
class ScrollsPickedUpData:
    items: list[int]

class ScrollsPickedUpMemory:
    def __init__(self, base_address: DeepPointer, process_handle) -> None:
        self.base_address = base_address
        self.process_handle = process_handle

    def read(self) -> ScrollsPickedUpData:
        raw_data = self.first_item_ptr.read_bytes(self.process_handle, self.size * 0x4)
        return ScrollsPickedUpData(struct.unpack(f"{self.size}i", raw_data))
    
    def write(self, data: ScrollsPickedUpData):
        if len(data.items) > self.count:
            self.reallocate()

        self.size_ptr.write_int(self.process_handle, len(data.items))
        self.first_item_ptr.write_bytes(self.process_handle, 
                                        struct.pack(f"{len(data.items)}i", *(data.items)), 
                                        len(data.items) * 0x4)

    def reallocate(self, new_array_size: int = 100):

        items_raw_ptr = DeepPointer.from_pointer(self.items_ptr, 0)
        items_raw_bytes = items_raw_ptr.read_bytes(self.process_handle, 0x20+0x4*self.size)

        self.items_ptr.free(self.process_handle)

        memory_adress = allocate_memory(self.process_handle, 0x20+new_array_size*0x4)
        self.items_ptr.write_longlong(self.process_handle, memory_adress)

        items_raw_ptr.write_bytes(self.process_handle, items_raw_bytes, 0x20+0x4*self.size)
        self.count_ptr.write_longlong(self.process_handle, new_array_size)

    @property
    def items_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.base_address, 0x10)

    @property
    def size_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.base_address, 0x18)

    @property 
    def size(self) -> int:
        return self.size_ptr.read_int(self.process_handle)

    @property
    def count_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.items_ptr, 0x18)

    @property 
    def count(self) -> int:
        return self.count_ptr.read_longlong(self.process_handle)
    
    @property
    def first_item_ptr(self) -> DeepPointer:
        return DeepPointer.from_pointer(self.items_ptr, 0x20)
    