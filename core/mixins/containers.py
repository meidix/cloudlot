from .base import BaseSimEntityAccessMixin


class ContainerAccessMixin(BaseSimEntityAccessMixin):

    def get_containers(self):
        self.check_entity_access()
        return self._platform.get_entity('container')