from sqlalchemy import create_engine
def get_database():
    return create_engine('postgresql://pyuser:dikkeberta@vichogent.be:40035/dep')
# base = declarative_base()
# pg_conn = pg_engine.connect()
# metadata = MetaData(pg_engine)  
    
# Session = sessionmaker(bind=pg_engine)
# pg_session = Session()
# base.metadata.create_all(pg_engine)

