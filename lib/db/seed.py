from sqlalchemy.orm import sessionmaker
from models import Cell, Clue, engine

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define the clues and answers

session.query(Clue).delete()
session.query(Cell).delete()


clues = [
    {"number": 1, "direction": "Across", "text": "Petty, paltry or puny", "answer": "SMALL"},
    {"number": 6, "direction": "Across", "text": "Place for outdoor furniture", "answer": "PATIO"},
    {"number": 7, "direction": "Across", "text": "What 'Happy Birthday' might be written in", "answer": "ICING"},
    {"number": 8, "direction": "Across", "text": "Things debated by expectant parents", "answer": "NAMES"},
    {"number": 9, "direction": "Across", "text": "Anderson who directed 2023's 'Asteroid City'", "answer": "WES"},
    {"number": 1, "direction": "Down", "text": "Go round and round", "answer": "SPIN"},
    {"number": 2, "direction": "Down", "text": "Colorful parrot", "answer": "MACAW"},
    {"number": 3, "direction": "Down", "text": "Once upon _____", "answer": "ATIME"},
    {"number": 4, "direction": "Down", "text": "They go from point A to point B", "answer": "LINES"},
    {"number": 5, "direction": "Down", "text": "Fireplace fodder", "answer": "LOGS"}
]

answer = [
    ["S", "M", "A", "L", "L"],
    ["P", "A" ,"T" ,"I" ,"O"],
    ["I", "C" ,"I" ,"N" ,"G"],
    ["N", "A" ,"M" ,"E" ,"S"],
    [" ", "W" ,"E" ,"S" ," "]
]


# Add the clues to the database
for clue_data in clues:
    clue = Clue(**clue_data)
    session.add(clue)

session.commit()

