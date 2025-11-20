from datetime import datetime
from typing import Any, Optional, Dict

from pydantic import BaseModel


class RequestListScheme(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    user_id: int
    username: Optional[str]
    title: str
    description: str
    contact: Optional[str]
    meta: Optional[Dict[str, Any]]
    created_at: datetime
