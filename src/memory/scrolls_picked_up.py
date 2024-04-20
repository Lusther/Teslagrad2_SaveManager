from dataclasses import dataclass
import struct
from .pointer import DeepPointer

@dataclass
class ScrollsPickedUpData:
    items: list[int]

class ScrollsPickedUpMemory:
    def __init__(self, base_address: DeepPointer, process_handle) -> None:
        self.base_address = base_address
        self.process_handle = process_handle

    def read(self) -> ScrollsPickedUpData:
        raw_data = self.first_item_ptr.read_bytes(self.process_handle, self.size * 0x4)
        # raw_data = read_bytes(self.process_handle, self.first_item, self.size * 0x4)
        return ScrollsPickedUpData(struct.unpack(f"{self.size}i", raw_data))
    
    def write(self, data: ScrollsPickedUpData):
        self.size_ptr.write_int(self.process_handle, len(data.items))
        self.first_item_ptr.write_bytes(self.process_handle, 
                                        struct.pack(f"{len(data.items)}i", *(data.items)), 
                                        len(data.items) * 0x4)
        # write_int(self.process_handle, self.base_address + 0x18, len(data.items))
        # write_bytes(self.process_handle, self.first_item, struct.pack(f"{len(data.items)}i", *(data.items)), len(data.items) * 0x4)

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
    

    
