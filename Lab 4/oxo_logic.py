import random
import json
import os


class TicTacToeGame:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'  # Human player always starts
        self.game_over = False
        self.winner = None
        self.moves_count = 0
        
    def new_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.moves_count = 0
        print("New game started! You are X, computer is O.")
        
    def display_board(self):
        print("\n Current Board:")
        print(" " + " | ".join([str(i) if self.board[i] == ' ' else self.board[i] for i in range(0, 3)]))
        print("-----------")
        print(" " + " | ".join([str(i) if self.board[i] == ' ' else self.board[i] for i in range(3, 6)]))
        print("-----------")
        print(" " + " | ".join([str(i) if self.board[i] == ' ' else self.board[i] for i in range(6, 9)]))
        print()
        
    def is_valid_move(self, position):
        return 0 <= position <= 8 and self.board[position] == ' '
        
    def make_move(self, position, player):
        if self.is_valid_move(position):
            self.board[position] = player
            self.moves_count += 1
            return True
        return False
        
    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        
        for combo in winning_combinations:
            if (self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' '):
                return self.board[combo[0]]
                
        if self.moves_count == 9:
            return 'Draw'
            
        return None
        
    def player_move(self):
        while True:
            try:
                position = int(input("Enter your move (0-8): "))
                if self.make_move(position, 'X'):
                    break
                else:
                    print("Invalid move! Position already taken or out of range.")
            except ValueError:
                print("Please enter a valid number (0-8).")
                
    def computer_move(self):
        print("Computer's turn...")
        
        # Strategy: Try to win, then block player, then random
        move = self._find_winning_move('O') or self._find_winning_move('X') or self._random_move()
        
        if move is not None:
            self.make_move(move, 'O')
            print(f"Computer chooses position {move}")
        
    def _find_winning_move(self, player):
        for i in range(9):
            if self.board[i] == ' ':
                # Try the move
                self.board[i] = player
                if self.check_winner() == player:
                    self.board[i] = ' '  # Undo the move
                    return i
                self.board[i] = ' '  # Undo the move
        return None
        
    def _random_move(self):
        available_moves = [i for i in range(9) if self.board[i] == ' ']
        return random.choice(available_moves) if available_moves else None
        
    def update_game_state(self):
        result = self.check_winner()
        if result:
            self.game_over = True
            self.winner = result
            
    def save_game(self, filename="saved_game.json"):
        try:
            game_state = {
                'board': self.board,
                'current_player': self.current_player,
                'game_over': self.game_over,
                'winner': self.winner,
                'moves_count': self.moves_count
            }
            
            with open(filename, 'w') as file:
                json.dump(game_state, file, indent=2)
            print(f"Game saved to {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
            
    def load_game(self, filename="saved_game.json"):
        try:
            if not os.path.exists(filename):
                print(f"Save file {filename} not found.")
                return False
                
            with open(filename, 'r') as file:
                game_state = json.load(file)
                
            # Validate loaded data
            if len(game_state['board']) != 9:
                raise ValueError("Invalid board size")
                
            self.board = game_state['board']
            self.current_player = game_state.get('current_player', 'X')
            self.game_over = game_state.get('game_over', False)
            self.winner = game_state.get('winner', None)
            self.moves_count = game_state.get('moves_count', 0)
            
            print(f"Game loaded from {filename}")
            return True
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
            
    def get_game_stats(self):
        return {
            'moves_made': self.moves_count,
            'game_over': self.game_over,
            'winner': self.winner,
            'board_state': self.board.copy()
        }
        
    def play(self):
        print("Welcome to Tic-Tac-Toe!")
        print("Positions are numbered 0-8 as shown:")
        print(" 0 | 1 | 2 ")
        print("-----------")
        print(" 3 | 4 | 5 ")
        print("-----------")
        print(" 6 | 7 | 8 ")
        
        while not self.game_over:
            self.display_board()
            
            if self.current_player == 'X':
                self.player_move()
            else:
                self.computer_move()
                
            self.update_game_state()
            
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            
        self.display_board()
        if self.winner == 'Draw':
            print("It's a draw!")
        elif self.winner == 'X':
            print("Congratulations! You won!")
        else:
            print("Computer wins! Better luck next time!")


def main():
    game = TicTacToeGame()
    
    while True:
        print("\n" + "="*40)
        print("TIC-TAC-TOE GAME")
        print("="*40)
        print("1. New Game")
        print("2. Load Game")
        print("3. Save Game") 
        print("4. Exit")
        print("-"*40)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            game.new_game()
            game.play()
            
        elif choice == '2':
            filename = input("Enter filename to load (default: saved_game.json): ").strip()
            if not filename:
                filename = "saved_game.json"
            if game.load_game(filename):
                if not game.game_over:
                    game.play()
                else:
                    print("Loaded game is already finished!")
                    game.display_board()
            
        elif choice == '3':
            filename = input("Enter filename to save (default: saved_game.json): ").strip()
            if not filename:
                filename = "saved_game.json"
            game.save_game(filename)
            
        elif choice == '4':
            print("Thanks for playing!")
            break
            
        else:
            print("Invalid choice! Please enter 1-4.")


if __name__ == "__main__":
    main()