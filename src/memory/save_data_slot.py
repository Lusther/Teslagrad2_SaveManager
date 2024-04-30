from dataclasses import dataclass
from .triggers_set import TriggersSetData, TriggersSetMemory
from .map_shapes_unlocked import MapShapesUnlockedData, MapShapesUnlockedMemory
from .scrolls_picked_up import ScrollsPickedUpData, ScrollsPickedUpMemory
from .pointer import DeepPointer

from pymem.memory import allocate_memory

@dataclass
class SaveDataSlotData:
    respawn_scene: str
    partial_data: bytes
    scrolls_picked_up: ScrollsPickedUpData
    triggers_set: TriggersSetData
    map_shapes_unlocked: MapShapesUnlockedData

class SaveDataSlotMemory:
    def __init__(self, base_adress: DeepPointer, process_handle) -> None:

        self.base_adress = base_adress
        self.process_handle = process_handle

        self.scroll_picked_up_memory = ScrollsPickedUpMemory(self.scrolls_ptr, process_handle)
        self.triggers_set_memory = TriggersSetMemory(self.triggers_ptr, process_handle)
        self.map_shapes_unlocked_memory = MapShapesUnlockedMemory(self.map_ptr, process_handle)

    def read(self) -> SaveDataSlotData:

        respawn_scene_str_len = DeepPointer.from_pointer(self.respawn_scene_ptr, 0x10).read_int(self.process_handle)
        respawn_scene_str = DeepPointer.from_pointer(self.respawn_scene_ptr, 0x14).read_bytes(self.process_handle, respawn_scene_str_len*0x2).decode("utf-16")

        return SaveDataSlotData(
            respawn_scene=respawn_scene_str,
            partial_data=self.partial_data_ptr.read_bytes(self.process_handle, 0x30),
            scrolls_picked_up=self.scroll_picked_up_memory.read(),
            triggers_set=self.triggers_set_memory.read(),
            map_shapes_unlocked=self.map_shapes_unlocked_memory.read(),
        )

    def write(self, data: SaveDataSlotData):

        string_header = DeepPointer.from_pointer(self.respawn_scene_ptr, 0x0).read_bytes(self.process_handle, 0x10)
        DeepPointer.from_pointer(self.respawn_scene_ptr, 0x0).free(self.process_handle)
        new_adress = allocate_memory(self.process_handle, 0x14+len(data.respawn_scene)*0x2)
        self.respawn_scene_ptr.write_longlong(self.process_handle, new_adress)
        DeepPointer.from_pointer(self.respawn_scene_ptr, 0x00).write_bytes(self.process_handle, string_header, 0x10)
        DeepPointer.from_pointer(self.respawn_scene_ptr, 0x10).write_short(self.process_handle, len(data.respawn_scene))
        DeepPointer.from_pointer(self.respawn_scene_ptr, 0x14).write_bytes(self.process_handle, data.respawn_scene.encode("utf-16")[2:], len(data.respawn_scene)*0x2)

        self.partial_data_ptr.write_bytes(self.process_handle, data.partial_data, 0x30)
        self.scroll_picked_up_memory.write(data.scrolls_picked_up)
        self.triggers_set_memory.write(data.triggers_set)
        self.map_shapes_unlocked_memory.write(data.map_shapes_unlocked)
        pass

    @property
    def respawn_scene_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x30)

    @property
    def partial_data_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x38)

    @property
    def scrolls_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x80)
    
    @property
    def triggers_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x68)
    
    @property
    def map_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x70)