from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Cell(Base):
    __tablename__ = 'cells'
    id = Column(Integer, primary_key=True)
    row = Column(Integer, nullable=False)
    column = Column(Integer, nullable=False)
    value = Column(String)
    users_puzzles_id = Column(Integer, ForeignKey('user_puzzles.id'))
    user_puzzles = relationship("User_puzzles", back_populates="cells")

class User_puzzles(Base):
    __tablename__ = 'user_puzzles'
    id = Column(Integer, primary_key=True)
    puzzle_id = Column(Integer, ForeignKey('puzzles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    cells = relationship("Cell", back_populates="user_puzzles")

class Clue(Base):
    __tablename__ = 'clues'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    direction = Column(String)
    text = Column(String)
    answer = Column(String)
    puzzle_id = Column(Integer, ForeignKey('puzzles.id'))
    puzzle = relationship("Puzzle", back_populates="clues")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

class Puzzle(Base):
    __tablename__ = 'puzzles'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    clues = relationship("Clue", back_populates="puzzle")  


# Create the database engine and tables
engine = create_engine('sqlite:///crossword.db')


Base.metadata.create_all(engine)

# Insert initial clues (up to 10th ID)
Session = sessionmaker(bind=engine)
session = Session()