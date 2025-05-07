from .base import BaseSimEntityAccessMixin


class ClientAccessMixin(BaseSimEntityAccessMixin):

    def get_client(self):
        self.check_entity_access()
        return self._platform.get_entity("client")
