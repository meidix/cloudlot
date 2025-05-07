from core.entities import SimEntity
from core.mixins import InvokerAccessMixin


class Scheduler(SimEntity, InvokerAccessMixin):
    entity_type = "scheduler"

