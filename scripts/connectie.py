from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
# get credentials from api\db\credentials.env file
load_dotenv(r"C:\Users\jarno\Desktop\hogent\jaar 3\sem 1\Data project 2\DEP2G02\api\db\credentials.env")
password = os.getenv('DBPASSWD')
db_user = os.getenv('DBUSER')
host = os.getenv('DBHOST')
port = os.getenv('DBPORT')
def get_database():
    # print(f'postgresql://{str(db_user)}:{str(password)}@{host}:{port}/dep')
    return create_engine(f'postgresql://{str(db_user)}:{str(password)}@{host}:{port}/dep').connect()
# base = declarative_base()
# pg_conn = pg_engine.connect()
# metadata = MetaData(pg_engine)  
    
# Session = sessionmaker(bind=pg_engine)
# pg_session = Session()
# base.metadata.create_all(pg_engine)

