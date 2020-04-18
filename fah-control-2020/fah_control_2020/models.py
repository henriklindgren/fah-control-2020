from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, IPvAnyInterface, SecretStr


class ClientStatus(str, Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'


class Client(BaseModel):
    name: str
    ip: IPvAnyInterface = '127.0.0.1'
    port: int = 36330
    password: SecretStr
    status: ClientStatus


class Identity(BaseModel):
    name: str
    team_id: int


class SlotType(str, Enum):
    CPU = 'cpu'
    GPU = 'gpu'


class FoldingSlot(BaseModel):
    id: int
    type: SlotType
    options: dict = {}


class WorkStatus(str, Enum):
    RUNNING = 'running'


class PRCG(BaseModel):
    project: int
    run: int
    clone: int
    gen: int


class WorkUnit(BaseModel):
    status: WorkStatus
    progress: float
    prcg: PRCG
    eta: datetime
    time_per_frame: int
    base_credit: int
    core: str
    assigned: datetime
    timeout: datetime
    expiration: datetime
    work_server: IPvAnyInterface
    collection_server: IPvAnyInterface

    @property
    def estimated_credit(self) -> int:
        return self.base_credit + 1  # FIXME


class WorkQueue(BaseModel):
    units: List[WorkUnit]
