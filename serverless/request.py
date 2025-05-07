import dataclasses


@dataclasses.dataclass
class ServerlessRequest:
    id: int
    arrival_time: float
    function_id: int
    length: int
    cores: int
    container_mips: int
    container_ram: int
