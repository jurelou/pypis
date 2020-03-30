from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, sql
from sqlalchemy.orm import relationship

from pypis.db.database import Base


class Release(Base):
    __tablename__ = "release"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    version = Column(String)

    comment_text = Column(String)
    filename = Column(String)
    has_sig = Column(String, default=False)
    md5_digest = Column(String)
    sha256_digest = Column(String)
    packagetype = Column(String)
    python_version = Column(String)
    requires_python = Column(String)
    requires_dist = Column(String)
    upload_method = Column(String)
    size = Column(Integer)
    upload_time = Column(
        DateTime(timezone=False), nullable=False, server_default=sql.func.now()
    )
    upload_time_iso_8601 = Column(
        DateTime(timezone=False), nullable=False, server_default=sql.func.now()
    )
    url = Column(String)

    package_id = Column(Integer, ForeignKey("package.id"))
    package = relationship("Package", back_populates="releases")

    keywords = Column(String)
    platform = Column(String)

    author = Column(String)
    author_email = Column(String)

    maintainer = Column(String)
    maintainer_email = Column(String)

    md5_digest = Column(String)
    sha256_digest = Column(String)
    blake2_256_digest = Column(String)
