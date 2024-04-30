from .pointer import DeepPointer

STRING_PREFIX = [0xF0, 0x7A, 0x68, 0xC1, 0x45, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

def to_string_bytes(str) -> str:
    str_bytes = bytearray(STRING_PREFIX)
    str_bytes.extend(len(str).to_bytes(4, byteorder='little'))
    str_bytes.extend(str.encode("utf-16")[2:])
    return str_bytes

# class StringMemory:
#     def __init__(self, base_address: DeepPointer, handle) -> None:
#         self.handle = handle
#         self.base_address = base_address

#     def read(self) -> str:
#         return self.first_char_ptr.read_bytes(self.handle, self.count * 0x2).decode("utf-16")
    
#     def write(self, string: str):
#         self.first_char_ptr.write_bytes()

#     @ 
#     def count_ptr(self) -> DeepPointer:
#         return DeepPointer.from_pointer(self.base_address, 0x10)
    
#     @property
#     def first_char_ptr(self) -> DeepPointer:
#         return DeepPointer.from_pointer(self.base_address, 0x14)
    
#     @property
#     def count(self) -> int:
#         return self.count_ptr.read_int(self.handle)
    
