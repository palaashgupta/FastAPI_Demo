from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


### SQLITE3 Database
SQL_ALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'  #SQLITE3 Database
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False}) # sqlite3 Database


### PostgreSQL Database
#SQL_ALCHEMY_DATABASE_URL = 'postgresql://postgres:#####%40123@localhost/TodopplicationDatabase' #PostgreSQL Database
#engine = create_engine(SQL_ALCHEMY_DATABASE_URL) #PostgreSQL Database

### MySQL Database
#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:####%40123@127.0.0.1:3306/todoapplicationdatabase' #MySQL Database
#engine = create_engine(SQLALCHEMY_DATABASE_URL) #MySQL Database

SessionLocal = sessionmaker(autocommit = False, autoflush=False , bind = engine)

Base = declarative_base()
