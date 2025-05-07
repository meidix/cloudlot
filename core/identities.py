from typing import Dict


class IDPool(object):
    id_pool: Dict[str, int] = {}

    @classmethod
    def new_id(cls, class_: object) -> int:
        key = class_.__class__.__name__
        if key in cls.id_pool.keys():
            cls.id_pool[key] = cls.id_pool[key] + 1
        else:
            cls.id_pool[key] = 1
        return cls.id_pool[key]
