from typing import Any, Optional, Dict, Union, List
from core.resources import Resource
from .provisioners import ResourceProvisioner
from .identities import IDPool
from .tags import SimulationTags


class SimEvent(object):
    def __init__(
        self,
        time: float,
        data: Any,
        tag: SimulationTags,
        source_uid: str,
        destination_uid: Optional[str] = None,
    ):
        self.time = time
        self.data = data
        self.tag = tag
        self.source = source_uid
        self.destination = destination_uid

    def get_sort_key(self):
        return self.time

    def get_data(self):
        return self.data


class SimEntity(object):
    entity_type: str = None

    def __str__(self):
        return self.uid

    def __init__(self):
        self.id = IDPool.new_id(self.__class__)
        self.uid = f"{self.__class__.__name__}#{self.id}"
        self._platform = None

    def start_entity(self):
        pass

    def stop_entity(self):
        pass

    def process_event(self, event: SimEvent):
        match event.tag:
            case _:
                pass

    def send(
        self, time: float, data: Any, tag: SimulationTags, destination_uid: Optional[str] = None
    ) -> None:
        event = SimEvent(time, data, tag, self.uid, destination_uid)
        if not hasattr(self, "_platform"):
            raise Exception(f"Entity Not registrered: {self.uid}")
        self._platform.add_event(event)


class ResourcedSimEntity(SimEntity):

    def get_available_cpu(self):
        return self.cpu_provisioner.get_total_available_capacity()

    def get_available_ram(self):
        pass

