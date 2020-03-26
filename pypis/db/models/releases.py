from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from pypis.db.database import Base


class Release(Base):
    __tablename__ = "release"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    version = Column(String)
    comment_text = Column(String)
    filename = Column(String, primary_key=True)
    has_sig = Column(String)
    md5_digest = Column(String, primary_key=True)
    sha256_digest = Column(String, primary_key=True)
    packagetype = Column(String)
    python_version = Column(String)
    requires_python = Column(String)
    size = Column(Integer)
    upload_time = Column(DateTime)
    upload_time_iso_8601 = Column(DateTime)
    url = Column(String)

    package_id = Column(Integer, ForeignKey("package.id"))
    package = relationship("Package", back_populates="releases")
