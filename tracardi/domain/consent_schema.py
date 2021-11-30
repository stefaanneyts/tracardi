from pydantic import BaseModel, validator
from typing import Dict
from uuid import UUID, uuid4
from datetime import datetime


class Revoke(BaseModel):
    revoke: datetime = None

# todo after second thought this should be removed after the removal of endpoint /consent/profile/{profile_id}
class ConsentSchema(BaseModel):
    __root__: Dict[str, Revoke] = {"consent-id": {"revoke": datetime.utcnow()}}

    @validator("__root__")
    def validate_root(cls, v):
        if len(v) != 1:
            raise ValueError("passed too many consents into request")
        return v

    @property
    def id(self):
        return list(self.__root__.items()).pop()[0]

    @property
    def content(self):
        return self.__root__
