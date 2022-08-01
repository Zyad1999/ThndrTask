
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from config.environment import DATABASE_ENDPOINT,DATABASE_NAME,DATABASE_PASSWORD,DATABASE_PORT,DATABASE_USERNAME

SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://'+DATABASE_USERNAME+':'+DATABASE_PASSWORD+'@'+DATABASE_ENDPOINT+':'+DATABASE_PORT+'/'+DATABASE_NAME

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
# meta = MetaData(engine)
# meta.reflect()
# meta.drop_all()
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()