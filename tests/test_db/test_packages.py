import unittest

from fastapi.testclient import TestClient
from pypis.db.repositories.packages import PackagesRepository
from pypis.db.database import Base


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class TestPackagesRepository(unittest.TestCase):
    def setUp(self):

        _engine = create_engine("sqlite:///:memory:")
        session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
        session.configure(bind=_engine)

        Base.metadata.drop_all(bind=_engine)
        Base.metadata.create_all(bind=_engine)

        self.repo = PackagesRepository(session)

    def test_get_packages_00(self):

        repo = self.repo.get_packages()
        print("!!!!", repo)
