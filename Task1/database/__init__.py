from sqlalchemy.orm import Session

from database import models
from database.db import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

db_session = SessionLocal() # created session can be used by importing db_session
