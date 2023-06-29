from sqlalchemy.orm import sessionmaker
from models import Cell, Clue, engine, Puzzle, User, Base, User_puzzles

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Define the clues and answers

session.query(Clue).delete()
# session.query(Cell).delete()
session.query(Puzzle).delete()

# User.__table__.drop(engine)
# Puzzle.__table__.drop(engine)
# Clue.__table__.drop(engine)
# Cell.__table__.drop(engine)
# User_puzzles.__table__.drop(engine)

Base.metadata.create_all(engine)

puzzle_one = Puzzle(name = "puzzle1")
puzzle_two = Puzzle(name= "puzzle2")
puzzle_three = Puzzle(name= "puzzle3")


clues = [
    {"puzzle_id": 1, "number": 1, "direction": "Across", "text": "Petty, paltry or puny", "answer": "SMALL"},
    {"puzzle_id": 1, "number": 6, "direction": "Across", "text": "Place for outdoor furniture", "answer": "PATIO"},
    {"puzzle_id": 1, "number": 7, "direction": "Across", "text": "What 'Happy Birthday' might be written in", "answer": "ICING"},
    {"puzzle_id": 1, "number": 8, "direction": "Across", "text": "Things debated by expectant parents", "answer": "NAMES"},
    {"puzzle_id": 1, "number": 9, "direction": "Across", "text": "Anderson who directed 2023's 'Asteroid City'", "answer": "~WES~"},
    {"puzzle_id": 1, "number": 1, "direction": "Down", "text": "Go round and round", "answer": "SPIN~"},
    {"puzzle_id": 1, "number": 2, "direction": "Down", "text": "Colorful parrot", "answer": "MACAW"},
    {"puzzle_id": 1, "number": 3, "direction": "Down", "text": "Once upon _____", "answer": "ATIME"},
    {"puzzle_id": 1, "number": 4, "direction": "Down", "text": "They go from point A to point B", "answer": "LINES"},
    {"puzzle_id": 1, "number": 5, "direction": "Down", "text": "Fireplace fodder", "answer": "LOGS~"},
    {"puzzle_id": 2, "number": 1, "direction": "Across", "text": "Tai ___", "answer": "~~CHI"},
    {"puzzle_id": 2, "number": 4, "direction": "Across", "text": "A question of time", "answer": "~WHEN"},
    {"puzzle_id": 2, "number": 5, "direction": "Across", "text": "With 6-Across, morning meal", "answer": "BREAK"},
    {"puzzle_id": 2, "number": 6, "direction": "Across", "text": "With 5-Across, basketball play", "answer": "FAST~"},
    {"puzzle_id": 2, "number": 7, "direction": "Across", "text": "Device that may direct you somewhere", "answer": "GPS~~"},
    {"puzzle_id": 2, "number": 1, "direction": "Down", "text": "Game that can begin 1. e4 e5", "answer": "CHESS"},
    {"puzzle_id": 2, "number": 2, "direction": "Down", "text": "Spiciness", "answer": "HEAT~"},
    {"puzzle_id": 2, "number": 3, "direction": "Down", "text": "Squid squirt", "answer": "INK~~"},
    {"puzzle_id": 2, "number": 4, "direction": "Down", "text": "Conclude filming", "answer": "~WRAP"},  
    {"puzzle_id": 2, "number": 5, "direction": "Down", "text": "Roald Dahl book, The ___", "answer": "~~BFG"},
    {"puzzle_id": 3, "number": 1, "direction": "Across", "text": "They hire law school grads", "answer": "FIRMS"},
    {"puzzle_id": 3, "number": 6, "direction": "Across", "text": "Expression that rarely translates literally", "answer": "IDIOM"},
    {"puzzle_id": 3, "number": 7, "direction": "Across", "text": "Ted ___, hit Apple TV+ comedy", "answer": "LASSO"},
    {"puzzle_id": 3, "number": 8, "direction": "Across", "text": "Part of the face", "answer": "CHEEK"},
    {"puzzle_id": 3, "number": 9, "direction": "Across", "text": "Animal in a merry-go-round, to a kid", "answer": "HORSY"},
    {"puzzle_id": 3, "number": 1, "direction": "Down", "text": "Steal", "answer": "FILCH"},
    {"puzzle_id": 3, "number": 2, "direction": "Down", "text": "Its license plate bears the slogan, Famous Potatoes", "answer": "IDAHO"},
    {"puzzle_id": 3, "number": 3, "direction": "Down", "text": "Early ___ (morning person)", "answer": "RISER"},
    {"puzzle_id": 3, "number": 4, "direction": "Down", "text": "Red Sea parter", "answer": "MOSES"},  
    {"puzzle_id": 3, "number": 5, "direction": "Down", "text": "Like Californias air during fire season", "answer": "SMOKY"},
]

session.add(puzzle_one)
session.add(puzzle_two)
session.add(puzzle_three)


for clue_data in clues:
    clue = Clue(**clue_data)
    session.add(clue)


session.commit()


