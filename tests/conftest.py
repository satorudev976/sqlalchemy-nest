import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tests.models import Base


@pytest.fixture(scope="session")
def session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})

    Base.metadata.create_all(bind=engine)

    yield sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.drop_all(engine)
