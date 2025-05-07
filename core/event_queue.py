from typing import Optional, List, Dict, Tuple, Any

from .entities import SimEvent


class EventQueue(object):
    def __init__(self):
        self._data: Dict[float, List[SimEvent]] = dict()

    def __len__(self):
        return len(self._data)

    def put(self, event: SimEvent):
        if event.time in self._data.keys():
            self._data[event.time].append(event)
        else:
            self._data[event.time] = [event]

    def get_next(self, time: float) -> List[SimEvent]:
        return self._data.pop(time, [])
