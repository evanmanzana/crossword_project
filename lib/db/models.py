from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Cell(Base):
    __tablename__ = 'cells'

    id = Column(Integer, primary_key=True)
    row = Column(Integer)
    column = Column(Integer)
    value = Column(String)

class Clue(Base):
    __tablename__ = 'clues'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    direction = Column(String)
    text = Column(String)
    answer = Column(String)

# Create the database engine and tables
engine = create_engine('sqlite:///crossword.db')
Base.metadata.create_all(engine)

# Insert initial clues (up to 10th ID)
Session = sessionmaker(bind=engine)
session = Session()

# clues_count = session.query(Clue).count()
# if clues_count == 0:
#     for i in range(1, 11):
#         clue = Clue(number=i, direction='', text='', answer='')
#         session.add(clue)
#     session.commit()
