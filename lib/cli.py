from sqlalchemy.orm import Session
from db.models import Cell, Clue, User, Puzzle, engine, User_puzzles

# Create a session
with Session(engine) as session:
    # Colors
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    White = "\033[37m"
    Reset = "\033[0m"

    def login_user():
        global username
        username = input("Enter your username: ")
        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username=username)
            session.add(user)
            session.commit()
            print(f"New user {username} has been created! Welcome!")
        else:
            print(f"Welcome back, {username}!")
        return user


    def display_user_puzzles(user, username):
        user_puzzles = session.query(User_puzzles).filter_by(user_id=user.id).all()

        if not user_puzzles:
            print(f"No puzzles found for user: {username}!")
            print("Start a new puzzle?")
            decision = input("Yes or No? Y/N: ")
            if decision == 'Y':
                create_new_puzzle(user)
        else:
            print("Puzzles:")
            for user_puzzle in user_puzzles:
                puzzle = session.query(Puzzle).filter_by(id=user_puzzle.puzzle_id).first()
                print(f"- {puzzle.name}")

            puzzle_name = input("Enter the puzzle name to select: ")
            selected_user_puzzle = (
                session.query(User_puzzles)
                .join(Puzzle)
                .filter(User_puzzles.user_id == user.id, Puzzle.name == puzzle_name)
                .first()
            )

            if selected_user_puzzle:
                selected_puzzle = session.query(Puzzle).filter_by(id=selected_user_puzzle.puzzle_id).first()
                current_puzzle = selected_puzzle
                print(f"\nSelected Puzzle: {selected_puzzle.name}")

                # Retrieve clues for the selected puzzle
                clues = session.query(Clue).filter_by(puzzle_id=selected_user_puzzle.puzzle_id).all()
                print("\nClues:")
                for clue in clues:
                    print(f"{Magenta}{clue.number} {clue.direction}: {Cyan}{clue.text}{Reset}")

                # Retrieve cells for the selected puzzle
                cells = session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id).all()

                # Create the grid
                grid = [['[   ] ' for _ in range(5)] for _ in range(5)]

                # Fill in the grid with cell values
                for cell in cells:
                    if cell.row <= 5 and cell.column <= 5:
                        if cell.value is not None:
                            grid[cell.row - 1][cell.column - 1] = f'[ {cell.value.upper()} ]'

                # Print the crossword grid
                print(f"\n{Magenta}Crossword:{Reset}")
                for row in grid:
                    for cell_value in row:
                        print(cell_value, end='\t')
                    print()

                while True:
                    print("\n1. Edit Crossword")
                    print("2. Check Answers")
                    print("3. Delete Crossword from user")
                    print("4. Quit")
                    choice = input("Select an option (1-4): ")

                    if choice == '1':
                        print("\n--- Select how you would like to edit ---")
                        print("1. By row")
                        print("2. By column")
                        print("3. Quit")
                        edit_choice = input("Select an option (1-3): ")
                        if edit_choice == '1':
                            row = int(input("Enter the row to edit: "))
                            word = input("Enter your word: ")

                            if 1 <= row <= 5 and len(word) <= 5:
                                for i, letter in enumerate(word):
                                    cell = session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id, row=row, column=i + 1).first()
                                    if cell:
                                        cell.value = letter
                                    else:
                                        cell = Cell(users_puzzles_id=selected_user_puzzle.id, row=row, column=i + 1, value=letter)
                                        session.add(cell)
                                session.commit()
                                print("Crossword updated successfully!")
                                print("\nUpdated Crossword Grid:")
                                display_grid(current_puzzle, selected_user_puzzle)
                            
                            else:
                                print("Invalid row or word length. Please try again.")

                        elif edit_choice == '2':
                            column = int(input("Enter the column to edit: "))
                            word = input("Enter your word: ")

                            if 1 <= column <= 5 and len(word) <= 5:
                                for i, letter in enumerate(word):
                                    cell = session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id, row=i + 1, column=column).first()
                                    if cell:
                                        cell.value = letter
                                    else:
                                        cell = Cell(users_puzzles_id=selected_user_puzzle.id, row=i + 1, column=column, value=letter)
                                        session.add(cell)
                                session.commit()
                                print("Crossword updated successfully!")
                                print("\nUpdated Crossword Grid:")
                                display_grid(current_puzzle, selected_user_puzzle)
                            else:
                                print("Invalid column or word length. Please try again.")


                    elif choice == '2':
                        check_answers(current_puzzle, selected_user_puzzle)

                    elif choice == '3':
                        session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id).delete()
                        session.query(User_puzzles).filter_by(id=selected_user_puzzle.id).delete()
                        session.commit()
                        print("Crossword deleted successfully!")
                        break

                    elif choice == '4':
                        break

            else:
                print("Invalid puzzle name. Please try again.")



    def create_new_puzzle(user):
        puzzles = session.query(Puzzle).all()

        print("Available Puzzles:")
        for puzzle in puzzles:
            print(f"- {puzzle.name}")

        puzzle_name = input("Enter the puzzle name: ")
        puzzle = session.query(Puzzle).filter(Puzzle.name == puzzle_name).first()

        if puzzle:
            user_puzzle = User_puzzles(user_id=user.id, puzzle_id=puzzle.id)
            session.add(user_puzzle)
            session.commit()
            print(f"Puzzle '{puzzle_name}' created.")
            

            
            rows = 5
            columns = 5

            for row in range(1, rows + 1):
                for column in range(1, columns + 1):
                    cell = Cell(row=row, column=column, value=None, users_puzzles_id=user_puzzle.id)
                    session.add(cell)
                    session.commit()

            current_puzzle = puzzle  

        else:
            print("Invalid puzzle name. Please try again.")


    def display_grid(current_puzzle, selected_user_puzzle):
        print(f'current puzzle: {current_puzzle}')
        if current_puzzle:
            
            # cells = session.query(Cell).filter_by(puzzle_id=current_puzzle.id).all()
            cells = session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id).all()
            clues = session.query(Clue).filter_by(puzzle_id=current_puzzle.id).all()


            print("\nClues:")
            for clue in clues:
                print(f"{Magenta}{clue.number} {clue.direction}: {Cyan}{clue.text}{Reset}")
            print(f"Selected Crossword: {current_puzzle.name}")

            grid = [['[  ]' for _ in range(5)] for _ in range(5)]

            for cell in cells:
                if 1 <= cell.row <= 5 and 1 <= cell.column <= 5:
                    if cell.value is not None:
                        grid[cell.row - 1][cell.column - 1] = f'[ {cell.value.upper()} ]'

            print("Crossword Grid:")
            for row in grid:
                for cell_value in row:
                    print(cell_value, end='\t')
                print()

        else:
            print("No crossword selected. Please select a crossword.")

    def delete_puzzle(user):
        puzzle_name = input("Enter the name of the puzzle to delete: ")
        user_puzzle = session.query(User_puzzles).join(Puzzle).filter(User_puzzles.user_id == user.id, Puzzle.name == puzzle_name).first()
        if user_puzzle:
            session.delete(user_puzzle)
            session.commit()
            print(f"Puzzle '{puzzle_name}' has been deleted.")
        else:
            print(f"Puzzle '{puzzle_name}' not found for user '{user.username}'.")


    def check_answers(current_puzzle, selected_user_puzzle):
        if current_puzzle:
            clues = session.query(Clue).filter_by(puzzle_id=current_puzzle.id).all()
            cells = session.query(Cell).join(User_puzzles).filter(User_puzzles.id == selected_user_puzzle.id).all()
            filled_cells = {}
            print("\n--- Checking Answers ---")

            across_index = 0


            down_index = 0

            for cell in cells:
                
                filled_cells.setdefault(cell.row, {})
                filled_cells[cell.row][cell.column] = str(cell.value)

            for clue in clues:
                correct = True
                if clue.direction == 'Across':
                    across_index += 1
                    
                    row = filled_cells.get(across_index)
                    
                    if row:
                        word = ''.join([row.get(column, ' ') for column in range(1, 6)]).strip()
                        
                        
                        if word.lower() != clue.answer.lower() or not word:
                            correct = False
                elif clue.direction == 'Down':
                    down_index += 1
                    column = [filled_cells.get(row, {}).get(down_index, ' ') for row in range(1, 6)]
                    word = ''.join(column).strip()
                    
                    
                    if word.lower() != clue.answer.lower() or not word:
                        correct = False

                if correct:
                    print(f'{Green}{clue.number} {clue.direction}: Correct{Reset}')
                else:
                    print(f'{Red}{clue.number} {clue.direction}: Incorrect{Reset}')

        else:
            print("No puzzle selected. Please select a puzzle.")





    # Entry point of the program
    if __name__ == '__main__':
        user = login_user()
        current_puzzle = None
        while True:
            print(f'''╔═╗╦═╗╔═╗╔═╗╔═╗╦ ╦╔═╗╦═╗╔╦╗
║  ╠╦╝║ ║╚═╗╚═╗║║║║ ║╠╦╝ ║║
╚═╝╩╚═╚═╝╚═╝╚═╝╚╩╝╚═╝╩╚══╩╝''')
            print(f'---------------------------')
            print("\n1. Start a new puzzle")
            print("2. Load a puzzle")
            print("3. Quit")
            choice = input("Select an option (1-3): ")

            if choice == '1':
                create_new_puzzle(user)
        
            elif choice == '2':
                cell = Cell
                display_user_puzzles(user, username)
                puzzle_name = input("Enter puzzle to select: ")
                puzzle = session.query(Puzzle).filter_by(name=puzzle_name).first()
                if puzzle:
                    current_puzzle = puzzle
                    print(f"Puzzle '{puzzle_name}' selected!")
                else:
                    print(f"Puzzle '{puzzle_name}' not found!")

            elif choice == '3':
                break

        print("Goodbye!")
