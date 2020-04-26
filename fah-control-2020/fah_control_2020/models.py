from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, IPvAnyInterface, SecretStr


class FoldingPowerLevel(str, Enum):
    LIGHT = 'light'
    MEDIUM = 'medium'
    FULL = 'full'


class ClientStatus(str, Enum):
    ONLINE = 'online'
    OFFLINE = 'offline'
    UPDATING = 'updating'
    CONNECTING = 'connecting'
    SHUTDOWN = 'shutdown'

    ACTIVE = 'active'
    READY = 'ready'
    DUMP = 'dump'


class Identity(BaseModel):
    name: str
    team_id: int


class Client(BaseModel):
    name: str
    ip: IPvAnyInterface = '127.0.0.1'
    port: int = 36330
    password: SecretStr
    status: ClientStatus
    folding_power: FoldingPowerLevel
    identity: Identity


class SlotType(str, Enum):
    CPU = 'cpu'
    GPU = 'gpu'


class FoldingSlot(BaseModel):
    id: int
    type: SlotType
    options: dict = {}


class WorkStatus(str, Enum):
    RUNNING = 'running'
    PAUSED = 'paused'
    FINISHING = 'finishing'
    FINISHED = 'finished'
    UPLOADED = 'uploaded'

    FAILED = 'failed'
    ERROR = 'error'
    FAULTY = 'faulty'


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
