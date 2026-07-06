import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.signal.models import Signal
from app.domain.signal.repositories import SignalRepository
from app.domain.signal.schemas import SignalCreate, SignalUpdate

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    from app.infrastructure.database.base import BaseModel
    BaseModel.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    BaseModel.metadata.drop_all(bind=engine)


def test_create_signal(db):
    repo = SignalRepository(db)
    data = SignalCreate(
        title="Test Signal",
        platform="wechat",
        url="https://example.com",
        hot_score=100,
    )
    signal = repo.create(data)
    assert signal.id is not None
    assert signal.title == "Test Signal"
    assert signal.platform == "wechat"


def test_get_signal(db):
    repo = SignalRepository(db)
    signal = repo.get(1)
    assert signal is not None
    assert signal.title == "Test Signal"


def test_list_signals(db):
    repo = SignalRepository(db)
    signals, total = repo.list()
    assert total == 1
    assert len(signals) == 1


def test_update_signal(db):
    repo = SignalRepository(db)
    signal = repo.get(1)
    data = SignalUpdate(title="Updated Signal", hot_score=200)
    updated = repo.update(signal, data)
    assert updated.title == "Updated Signal"
    assert updated.hot_score == 200


def test_delete_signal(db):
    repo = SignalRepository(db)
    signal = repo.get(1)
    repo.delete(signal)
    assert repo.get(1) is None
