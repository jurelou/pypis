from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from pypis.db.database import Base

association_table = Table(
    "association",
    Base.metadata,
    Column("package", Integer, ForeignKey("package.id")),
    Column("classifier", Integer, ForeignKey("classifier.id")),
)


class Package(Base):
    __tablename__ = "package"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    author = Column(String)
    author_email = Column(String)

    description = Column(String)
    description_content_type = Column(String)

    classifiers = relationship("Classifier", secondary=association_table)

    releases = relationship("Release", back_populates="package")
    home_page = Column(String)
    license = Column(String)
    package_url = Column(String)
    project_url = Column(String)
    summary = Column(String)
    version = Column(String)
    platform = Column(String)
    maintainer = Column(String)

    maintainer_email = Column(String)

    bugtrack_url = Column(String)
    docs_url = Column(String)
    download_url = Column(String)

    requires_python = Column(String)
    requires_dist = Column(String)

    metadata_version = Column(String)
    protocol_version = Column(String)
    comment = Column(String)
