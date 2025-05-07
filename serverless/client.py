from typing import List
from core.entities import SimEntity
from core.mixins import SchedulerAccessMixin

from .tags import ClientTags
from .request import ServerlessRequest


class Client(SimEntity, SchedulerAccessMixin):
    entity_type = "client"

    def __init__(self, request_list: List[ServerlessRequest]):
        super().__init__()
        self.request_list = request_list

    def start_entity(self):
        scheduler = self.get_scheduler()
        for request in self.request_list:
            self.send(request.arrival_time, request, ClientTags.SCHEDULE_INVOCATION, scheduler.uid)
