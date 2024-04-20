
from __future__ import annotations

from pymem.memory import read_ctype, read_short, read_int, read_bytes, write_bytes, write_short, write_int
from ctypes import c_void_p

class DeepPointer():
    def __init__(self, base_adress, *offsets) -> None:
        self.base_adress = base_adress
        self.offsets = offsets

    @classmethod
    def from_pointer(cls, pointer: DeepPointer, *offsets):
        return cls(pointer.base_adress, *(pointer.offsets), *(offsets))
        
    def deref_last_pointer(self, handle) -> DeepPointer:
        ptr = self.base_adress

        if len(self.offsets) == 0:
            return ptr
        
        for offset in self.offsets[:-1]:
            ptr = read_ctype(handle, ptr + offset, c_void_p())
        ptr = ptr + self.offsets[-1]
        return DeepPointer(ptr)

    def read_short(self, handle) -> int:
        return read_short(handle, self.deref_last_pointer(handle).base_adress)

    def read_int(self, handle) -> int:
        return read_int(handle, self.deref_last_pointer(handle).base_adress)

    def read_bytes(self, handle, bytes) -> bytes:
        return read_bytes(handle, self.deref_last_pointer(handle).base_adress, bytes)
    
    def write_short(self, handle, value):
        write_short(handle, self.deref_last_pointer(handle).base_adress, value)

    def write_int(self, handle, value):
        write_int(handle, self.deref_last_pointer(handle).base_adress, value)

    def write_bytes(self, handle, value, bytes):
        write_bytes(handle, self.deref_last_pointer(handle).base_adress, value, bytes)