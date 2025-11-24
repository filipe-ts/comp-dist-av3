import dataclasses
from typing import Any, Protocol


class SpyneContext(Protocol):
    udc: dict[str, Any]


@dataclasses.dataclass
class SPYNECONSTS:
    CONTAINER: str = "container"
