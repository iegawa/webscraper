from dotenv.main import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
import os


load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")

Base = declarative_base()

def db_connect():
    return create_engine(
        'postgresql+psycopg2://'+USERNAME+':'+PASSWORD+'@'+HOST+':'+PORT+'/'+DATABASE
    )
    
def create_table(engine):
    Base.metadata.create_all(engine)

class Books(Base):
    __tablename__="books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    stars = Column(Integer)
    price = Column(Float)
    availability = Column(Boolean)
    category = Column(String)

def insert_data(file):
    engine = db_connect()
    create_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    csv_data = pd.read_csv(file)
    csv_list = csv_data.values.tolist()
    try:
        for column in csv_list:
            book_item = Books(**{
                'availability' : column[0],
                'category' : column[1],
                'price' : column[2],
                'stars' : column[3],
                'title' : column[4],
            })
            session.add(book_item)
            session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
    return

if __name__ == "__main__":
    file = "/home/fabiana/CaseTecnico/webscraper/books.csv"
    insert_data(file)