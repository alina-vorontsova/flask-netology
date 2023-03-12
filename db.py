from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker 


engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5431/flask')

Session = sessionmaker(bind=engine)
