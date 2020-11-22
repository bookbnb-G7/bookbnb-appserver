import os
import pytest
import tempfile
from app.main import app
from app.db import Base, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

@pytest.fixture(scope="session", autouse=True)
def test_app():
	client = TestClient(app)
	
	db_fd, db_fname = tempfile.mkstemp()
	TESTING_DB_URL = "sqlite:///" + db_fname

	engine = create_engine(TESTING_DB_URL, connect_args={"check_same_thread": False})
	TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

	Base.metadata.create_all(bind=engine)

	def get_testing_db():
	    db = TestingSessionLocal()
	    try:
	        yield db
	    finally:
	        db.close()

	app.dependency_overrides[get_db] = get_testing_db

	yield client  # testing happens here


