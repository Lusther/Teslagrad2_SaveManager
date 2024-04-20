from dataclasses import dataclass
from .triggers_set import TriggersSetData, TriggersSetMemory
from .map_shapes_unlocked import MapShapesUnlockedData, MapShapesUnlockedMemory
from .scrolls_picked_up import ScrollsPickedUpData, ScrollsPickedUpMemory
from .pointer import DeepPointer

@dataclass
class SaveDataSlotData:
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
        return SaveDataSlotData(
            partial_data=self.partial_data_ptr.read_bytes(self.process_handle, 0x38),
            scrolls_picked_up=self.scroll_picked_up_memory.read(),
            triggers_set=self.triggers_set_memory.read(),
            map_shapes_unlocked=self.map_shapes_unlocked_memory.read(),
        )

    def write(self, data: SaveDataSlotData):
        self.partial_data_ptr.write_bytes(self.process_handle, data.partial_data, 0x38)
        self.scroll_picked_up_memory.write(data.scrolls_picked_up)
        self.triggers_set_memory.write(data.triggers_set)
        self.map_shapes_unlocked_memory.write(data.map_shapes_unlocked)

    @property
    def partial_data_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x30)

    @property
    def scrolls_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x80)
    
    @property
    def triggers_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x68)
    
    @property
    def map_ptr(self):
        return DeepPointer.from_pointer(self.base_adress, 0x70)