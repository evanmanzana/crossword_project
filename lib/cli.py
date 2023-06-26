from sqlalchemy.orm import Session
from db.models import Cell, Clue, engine

# Create a session
with Session(engine) as session:

    # colors
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    White = "\033[37m"
    Reset = "\033[0m"

    # display crossword grid with clues and filled cell
    def display_grid():
        # Retrieve cells from the database
        cells = session.query(Cell).all()
        # Retrieve clues from the database
        clues = session.query(Clue).all()

        # Create the grid
        grid = [[' ' for _ in range(5)] for _ in range(5)]

        # Fill in the grid with cell values
        for cell in cells:
            if cell.row <= 5 and cell.column <= 5:
                grid[cell.row - 1][cell.column - 1] = cell.value.upper()

        # Print the crossword grid
        for row in grid:
            for cell_value in row:
                print(cell_value, end='\t')
            print()

        # Print the clues
        print("\nClues:")
        for clue in clues:
            print(f'{Magenta}{clue.number} {clue.direction}: {Cyan}{clue.text}{Reset}')

    def check_answers():

        clues = session.query(Clue).all()

        cells = session.query(Cell).all()

        
        filled_cells = {}

        print("\n--- Checking Answers ---")

        for cell in cells:
            filled_cells.setdefault(cell.row, [' ' for _ in range(5)])  # Initialize the row if not already present
            filled_cells[cell.row][cell.column - 1] = str(cell.value)  # Convert cell value to string

        for clue in clues:
            correct = True
            if clue.direction == 'Across':
                row = filled_cells.get(clue.number)
                if row:
                    cell_values = ''.join(row)
                    if cell_values.lower() != clue.answer.lower():
                        correct = False
            elif clue.direction == 'Down':
                column = [filled_cells.get(i, [' '])[clue.number - 1] for i in range(1, 6)]  # Updated range to include row 5
                cell_values = ''.join(column)
                if cell_values.lower() != clue.answer.lower():
                    correct = False

            if correct:
                print(f'{Green} {clue.number} {clue.direction}: Correct{Reset}')
            else:
                print(f'{Red} {clue.number} {clue.direction}: Incorrect{Reset}')
                

    # Entry point of the program
    if __name__ == '__main__':
        while True:
            print(f'''╔═╗╦═╗╔═╗╔═╗╔═╗╦ ╦╔═╗╦═╗╔╦╗
║  ╠╦╝║ ║╚═╗╚═╗║║║║ ║╠╦╝ ║║
╚═╝╩╚═╚═╝╚═╝╚═╝╚╩╝╚═╝╩╚══╩╝''')
            print(f'---------------------------')
            # print(f'      {Magenta}-{Cyan}+{Magenta}-{Cyan}+{Magenta}- {Blue}CROSSWORD {Magenta}-{Cyan}+{Magenta}-{Cyan}+{Magenta}-{Reset}')
            display_grid()
            print("\n1. Edit Crossword")
            print("2. Check Answers")
            print("3. Quit")
            choice = input("Select an option (1-3): ")

            if choice == '1':
                print("\n--- Select how you would like to edit ---")
                print("\n1. By row")
                print("2. By column")
                print("3. Quit")
                second_choice = input("Select an option (1-3): ")

                if second_choice == '1':
                    row = int(input("Enter the row to edit: "))
                    word = input("Enter your word: ")

                    if row == 5:
                        column = 2
                        if len(word) == 3:
                            for i, letter in enumerate(word):
                                cell = session.query(Cell).filter_by(row=row, column=column+i).first()
                                if cell:
                                    cell.value = letter
                                else:
                                    cell = Cell(row=row, column=column+i, value=letter)
                                    session.add(cell)
                            session.commit()
                        else:
                            print("Invalid word length. Please enter a 3-letter word.")
                    else:
                        column = int(input("Enter the starting column to edit: "))
                        word_length = len(word)
                        if 1 <= column <= 5 and word_length <= 5 - column + 1:
                            for i, letter in enumerate(word):
                                cell = session.query(Cell).filter_by(row=row, column=column+i).first()
                                if cell:
                                    cell.value = letter
                                else:
                                    cell = Cell(row=row, column=column+i, value=letter)
                                    session.add(cell)
                            session.commit()
                        else:
                            print("Invalid row or word length. Please try again.")

                elif second_choice == '2':
                    column = int(input("Enter the column to edit: "))
                    word = input("Enter your word: ")

                    if column != 1 and column != 5 and len(word) == 3:
                        for i, letter in enumerate(word):
                            if i < 3:
                                cell = session.query(Cell).filter_by(row=i+1, column=column).first()
                                if cell:
                                    cell.value = letter
                                else:
                                    cell = Cell(row=i+1, column=column, value=letter)
                                    session.add(cell)
                            else:
                                print("Invalid word length. Please enter a 3-letter word.")
                                break
                        session.commit()
                    else:
                        print("Invalid column or word length. Please try again.")
                elif second_choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")


        print("Goodbye!")
