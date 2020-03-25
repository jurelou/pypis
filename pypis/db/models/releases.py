from sqlalchemy import Column, DateTime, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from pypis.db.database import Base


class Release(Base):
    __tablename__ = "release"    

    id = Column(Integer, index=True)
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
    upload_time = Column(String)
    upload_time_iso_8601 = Column(String)
    url = Column(String)



    package_id = Column(Integer, ForeignKey('package.id'))
    package = relationship("Package", back_populates="releases")

