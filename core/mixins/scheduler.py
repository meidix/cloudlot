from .base import BaseSimEntityAccessMixin


class SchedulerAccessMixin(BaseSimEntityAccessMixin):

    def get_scheduler(self):
        self.check_entity_access()
        return self._platform.get_entity("scheduler")
