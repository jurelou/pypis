from pydantic import BaseConfig, BaseModel
from datetime import datetime
from typing import Dict, List, Optional


class ReleaseCreate(BaseModel):
    version: str
    comment_text: str
    filename: str
    has_sig: bool
    md5_digest: str
    sha256_digest: str

    packagetype: str
    python_version: str
    requires_python: Optional[str]
    size: int
    upload_time: str
    upload_time_iso_8601: str
    url: str
    class Config(BaseConfig):
        allow_population_by_field_name = True
        orm_mode = True
