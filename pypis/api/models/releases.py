from datetime import datetime
from typing import Optional

from pypis.api.models.base import BaseModel


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
    upload_time: datetime
    upload_time_iso_8601: datetime
    url: str
