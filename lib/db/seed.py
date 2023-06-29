from sqlalchemy.orm import sessionmaker
from models import Cell, Clue, engine, Puzzle, User, Base, User_puzzles

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define the clues and answers

session.query(Clue).delete()
session.query(Cell).delete()
session.query(Puzzle).delete()

# User.__table__.drop(engine)
# Puzzle.__table__.drop(engine)
# Clue.__table__.drop(engine)
# Cell.__table__.drop(engine)
# User_puzzles.__table__.drop(engine)

Base.metadata.create_all(engine)

puzzle_one = Puzzle(name = "puzzle1")
# puzzle_two = Puzzle(name= "puzzle2")
# puzzle_three = Puzzle(name= "puzzle3")


clues = [
    {"puzzle_id": 1, "number": 1, "direction": "Across", "text": "Petty, paltry or puny", "answer": "SMALL"},
    {"puzzle_id": 1, "number": 6, "direction": "Across", "text": "Place for outdoor furniture", "answer": "PATIO"},
    {"puzzle_id": 1, "number": 7, "direction": "Across", "text": "What 'Happy Birthday' might be written in", "answer": "ICING"},
    {"puzzle_id": 1, "number": 8, "direction": "Across", "text": "Things debated by expectant parents", "answer": "NAMES"},
    {"puzzle_id": 1, "number": 9, "direction": "Across", "text": "Anderson who directed 2023's 'Asteroid City'", "answer": "WES"},
    {"puzzle_id": 1, "number": 1, "direction": "Down", "text": "Go round and round", "answer": "SPIN"},
    {"puzzle_id": 1, "number": 2, "direction": "Down", "text": "Colorful parrot", "answer": "MACAW"},
    {"puzzle_id": 1, "number": 3, "direction": "Down", "text": "Once upon _____", "answer": "ATIME"},
    {"puzzle_id": 1, "number": 4, "direction": "Down", "text": "They go from point A to point B", "answer": "LINES"},
    {"puzzle_id": 1, "number": 5, "direction": "Down", "text": "Fireplace fodder", "answer": "LOGS"}
]


session.add(puzzle_one)

for clue_data in clues:
    clue = Clue(**clue_data)
    session.add(clue)


session.commit()


