from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from pypis.db.database import Base

association_table = Table(
    "association",
    Base.metadata,
    Column("package", Integer, ForeignKey("package.id")),
    Column("classifier", Integer, ForeignKey("classifier.id")),
)


class Classifier(Base):
    __tablename__ = "classifier"

    id = Column(Integer, primary_key=True)
    title = Column(String)


class Package(Base):
    __tablename__ = "package"

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
