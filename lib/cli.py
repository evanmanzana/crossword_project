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
        username = input(f"{Green}Enter your username:{Magenta} ")
        user = session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username=username)
            session.add(user)
            session.commit()
            print(f"{Green}New user {Reset}{Magenta}{username}{Reset}{Green} has been created! Welcome!{Reset}")
        else:
            print(f"{Blue}Welcome back, {Magenta}{username.upper()}{Reset}{Blue}!{Reset}")
        return user


    def display_user_puzzles(user, username):
        user_puzzles = session.query(User_puzzles).filter_by(user_id=user.id).all()

        if not user_puzzles:
            print(f"{Red}No puzzles found for user: {username}!{Reset}")
            print(f"{Blue}Start a new puzzle?{Reset}")
            decision = input(f"{Green}Yes{Reset}{Blue} or{Reset}{Red} No{Reset}{Blue}?{Reset}{Green} Y{Reset}{Blue}/{Reset}{Red}N{Reset}{Blue}:{Magenta} ")
            if decision == 'Y':
                create_new_puzzle(user)
        else:
            print(f"{Blue}Puzzles:{Reset}")
            for user_puzzle in user_puzzles:
                puzzle = session.query(Puzzle).filter_by(id=user_puzzle.puzzle_id).first()
                print(f"{Blue}- {Magenta}{puzzle.name}{Blue}: {Red}ID: {Magenta}{user_puzzle.id}{Reset}")

            puzzle_name = input(f"{Green}Enter the puzzle name OR ID to select:{Magenta} ")
            selected_user_puzzle = (

                session.query(User_puzzles)
                .join(Puzzle)
                .filter(User_puzzles.user_id == user.id, User_puzzles.id== puzzle_name)
            
                .first()
            )
            
            if selected_user_puzzle:
                selected_puzzle = session.query(Puzzle).filter_by(id=selected_user_puzzle.puzzle_id).first()
                current_puzzle = selected_puzzle
                print(f"\n{Red}Selected Puzzle: {selected_puzzle.name}{Reset}")

                # Retrieve clues for the selected puzzle
                clues = session.query(Clue).filter_by(puzzle_id=selected_user_puzzle.puzzle_id).all()
                print(f"\n{Red}Clues:{Reset}")
                for clue in clues:
                    print(f"{Magenta}{clue.number} {clue.direction}: {Cyan}{clue.text} {Green}({len(clue.answer)} letter word){Reset}")

                # Retrieve cells for the selected puzzle
                cells = session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id).all()

                # Create the grid
                grid = [[f'{Cyan}[   ]{Reset} ' for _ in range(5)] for _ in range(5)]

                # Fill in the grid with cell values
                for cell in cells:
                    if cell.row <= 5 and cell.column <= 5:
                        if cell.value is not None:
                            grid[cell.row - 1][cell.column - 1] = f'{Cyan}[{Magenta} {cell.value.upper()}{Cyan} ]{Reset}'

                # Print the crossword grid
                print(f"\n{Red}Your Puzzle:{Reset}")
                for row in grid:
                    for cell_value in row:
                        print(cell_value, end='\t')
                    print()

                while True:
                    print(f"\n{Blue}1. Edit Crossword")
                    print("2. Check Answers")
                    print("3. Delete Crossword from user")
                    print("4. Quit")
                    choice = input(f"{Green}Select an option (1-4):{Magenta} ")

                    if choice == '1':
                        display_grid(current_puzzle, selected_user_puzzle)
                        print(f"\n{Blue}---{Green} Select how you would like to edit{Blue} ---")
                        print(f"1. By row")
                        print("2. By column")
                        print("3. Quit")
                        edit_choice = input(f"{Green}Select an option (1-3):{Magenta} ")
                        if edit_choice == '1':
                            row = int(input(f"{Green}Enter the row to edit:{Magenta} "))
                            word = input(f"{Green}Enter your word:{Magenta} ")

                            if 1 <= row <= 5 and len(word) <= 5:
                                for i, letter in enumerate(word):
                                    cell = session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id, row=row, column=i + 1).first()
                                    if cell:
                                        cell.value = letter
                                    else:
                                        cell = Cell(users_puzzles_id=selected_user_puzzle.id, row=row, column=i + 1, value=letter)
                                        session.add(cell)
                                session.commit()
                                print(f"{Green}Crossword updated successfully!{Reset}")
                                display_grid(current_puzzle, selected_user_puzzle)
                                
                            
                            else:
                                print(f"{Red}Invalid row or word length. Please try again.{Reset}")

                        elif edit_choice == '2':
                            column = int(input(f"{Green}Enter the column to edit: {Magenta}"))
                            word = input(f"{Green}Enter your word: {Magenta}")

                            if 1 <= column <= 5 and len(word) <= 5:
                                for i, letter in enumerate(word):
                                    cell = session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id, row=i + 1, column=column).first()
                                    if cell:
                                        cell.value = letter
                                    else:
                                        cell = Cell(users_puzzles_id=selected_user_puzzle.id, row=i + 1, column=column, value=letter)
                                        session.add(cell)
                                session.commit()
                                print(f"{Green}Crossword updated successfully!{Reset}")
                                print(f"\n{Red}Updated Puzzle:{Reset}")
                                display_grid(current_puzzle, selected_user_puzzle)
                            else:
                                print(f"{Red}Invalid column or word length. Please try again.{Reset}")


                    elif choice == '2':
                        check_answers(current_puzzle, selected_user_puzzle)

                    elif choice == '3':
                        session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id).delete()
                        session.query(User_puzzles).filter_by(id=selected_user_puzzle.id).delete()
                        session.commit()
                        print(f"{Green}Crossword {Red}deleted {Green}successfully!{Reset}")
                        break

                    elif choice == '4':
                        break

            else:
                print(f"{Red}Invalid puzzle name. Please try again.{Reset}")



    def create_new_puzzle(user):
        puzzles = session.query(Puzzle).all()

        print("Available Puzzles:")
        for puzzle in puzzles:
            print(f"{Blue}- {Magenta}{puzzle.name}{Reset}")

        puzzle_name = input(f"{Green}Enter the puzzle name: {Magenta}")
        puzzle = session.query(Puzzle).filter(Puzzle.name == puzzle_name).first()

        if puzzle:
            user_puzzle = User_puzzles(user_id=user.id, puzzle_id=puzzle.id)
            session.add(user_puzzle)
            session.commit()
            print(f"{Blue}Puzzle '{Magenta}{puzzle_name}{Blue}' created.{Reset}")
            

            
            rows = 5
            columns = 5

            for row in range(1, rows + 1):
                for column in range(1, columns + 1):
                    cell = Cell(row=row, column=column, value=None, users_puzzles_id=user_puzzle.id)
                    session.add(cell)
                    session.commit()

            current_puzzle = puzzle  

        else:
            print(f"{Red}Invalid puzzle name. Please try again.")


    def display_grid(current_puzzle, selected_user_puzzle):
        
        if current_puzzle:
            
            # cells = session.query(Cell).filter_by(puzzle_id=current_puzzle.id).all()
            cells = session.query(Cell).filter_by(users_puzzles_id=selected_user_puzzle.id).all()
            clues = session.query(Clue).filter_by(puzzle_id=current_puzzle.id).all()


            print(f"\n{Red}Clues:{Reset}")
            for clue in clues:
                print(f"{Magenta}{clue.number} {clue.direction}: {Cyan}{clue.text}{Reset}")
            # print(f"{Blue}Selected Crossword: {Magenta}{current_puzzle.name}{Reset}")

            grid = [[f'{Cyan}[   ]{Reset} ' for _ in range(5)] for _ in range(5)]

            for cell in cells:
                if 1 <= cell.row <= 5 and 1 <= cell.column <= 5:
                    if cell.value is not None:
                        grid[cell.row - 1][cell.column - 1] = f'{Cyan}[{Magenta} {cell.value.upper()}{Cyan} ]{Reset}'

            print(f"{Red}Your Puzzle:{Reset}")
            for row in grid:
                for cell_value in row:
                    print(cell_value, end='\t')
                print()

        else:
            print(f"{Red}No crossword selected. Please select a crossword.")

    def delete_puzzle(user):
        puzzle_name = input(f"{Green}Enter the name of the puzzle to delete: {Magenta}{Reset}")
        user_puzzle = session.query(User_puzzles).join(Puzzle).filter(User_puzzles.user_id == user.id, Puzzle.name == puzzle_name).first()
        if user_puzzle:
            session.delete(user_puzzle)
            session.commit()
            print(f"{Green}Puzzle '{Magenta}{puzzle_name}{Green}' has been {Red}deleted{Green}.{Reset}")
        else:
            print(f"{Red}Puzzle '{Magenta}{puzzle_name}{Red}' not found for user '{Magenta}{user.username}{Red}'.{Reset}")


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
            obj_tst = {}
            key = 0
            for row in range(5):
                value = 0
                for column in range(5):
                    value += 1
                    if filled_cells[row+1][column+1] != " ":
                        if value in obj_tst.values():
                            
                            break
                        key += 1
                        if key <= 5:
                            obj_tst[key] = value
                            
               
           
                
            # {
            #     1: 3,
            #     2: 4,
            #     3: 5,
            #     4: 2,
            #     5: 1
            # }
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
                    column = [filled_cells.get(row, {}).get(obj_tst[down_index], ' ') for row in range(1, 6)]
                    word = ''.join(column).strip()
                    
                    
                    if word.lower() != clue.answer.lower() or not word:
                        correct = False

                if correct:
                    print(f'{Magenta}{clue.number} {clue.direction}: {Green}Correct{Reset}')
                else:
                    print(f'{Magenta}{clue.number} {clue.direction}: {Red}Incorrect{Reset}')

        else:
            print("No puzzle selected. Please select a puzzle.")





    # Entry point of the program
    if __name__ == '__main__':
        user = login_user()
        current_puzzle = None
        while True:
            print(f'''{Green}╔═╗╦═╗╔═╗╔═╗╔═╗{Cyan}╦ ╦╔═╗╦═╗╔╦╗{Green}
║  ╠╦╝║ ║╚═╗╚═╗{Cyan}║║║║ ║╠╦╝ ║║{Green}
╚═╝╩╚═╚═╝╚═╝╚═╝{Cyan}╚╩╝╚═╝╩╚══╩╝{Reset}''')
            print(f'{Blue}---------------------------')
            print(f"\n1. Start a new puzzle")
            print(f"2. Load a puzzle")
            print(f"3. Quit{Reset}")
            choice = input(f"{Green}Select an option (1-3):{Magenta} ")

            if choice == '1':
                create_new_puzzle(user)
        
            elif choice == '2':
                cell = Cell
                display_user_puzzles(user, username)
                puzzle_name = input(f"{Green}Enter puzzle to select:{Magenta} ")
                puzzle = session.query(Puzzle).filter_by(name=puzzle_name).first()
                if puzzle:
                    current_puzzle = puzzle
                    print(f"{Green}Puzzle '{Magenta}{puzzle_name}{Green}' selected!{Reset}")
                else:
                    print(f"{Red}Puzzle '{Magenta}{puzzle_name}{Red}' not found!{Reset}")

            elif choice == '3':
                break

        print("Goodbye!")
