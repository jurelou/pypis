from sqlalchemy import Column, Integer, String

from pypis.db.database import Base


class Classifier(Base):
    __tablename__ = "classifier"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True)
    title = Column(String)
