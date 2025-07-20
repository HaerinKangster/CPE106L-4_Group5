import unittest
from oxo_logic import TicTacToeGame


class TestTicTacToeGame(unittest.TestCase):
    
    def setUp(self):
        self.game = TicTacToeGame()
    
    def test_new_game(self):
        self.game.new_game()
        self.assertEqual(self.game.board, [' '] * 9)
        self.assertEqual(self.game.current_player, 'X')
        self.assertFalse(self.game.game_over)
        self.assertIsNone(self.game.winner)
        self.assertEqual(self.game.moves_count, 0)
    
    def test_is_valid_move(self):
        self.assertTrue(self.game.is_valid_move(0))
        self.assertTrue(self.game.is_valid_move(8))
        self.assertFalse(self.game.is_valid_move(-1))
        self.assertFalse(self.game.is_valid_move(9))
        
        self.game.board[0] = 'X'
        self.assertFalse(self.game.is_valid_move(0))
    
    def test_make_move(self):
        result = self.game.make_move(0, 'X')
        self.assertTrue(result)
        self.assertEqual(self.game.board[0], 'X')
        self.assertEqual(self.game.moves_count, 1)
        
        result = self.game.make_move(0, 'O')
        self.assertFalse(result)
        self.assertEqual(self.game.moves_count, 1)
    
    def test_check_winner_row(self):
        self.game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.assertEqual(self.game.check_winner(), 'X')
        
        self.game.board = [' ', ' ', ' ', 'O', 'O', 'O', ' ', ' ', ' ']
        self.assertEqual(self.game.check_winner(), 'O')
    
    def test_check_winner_column(self):
        self.game.board = ['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ']
        self.assertEqual(self.game.check_winner(), 'X')
    
    def test_check_winner_diagonal(self):
        self.game.board = ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
        self.assertEqual(self.game.check_winner(), 'X')
        
        self.game.board = [' ', ' ', 'O', ' ', 'O', ' ', 'O', ' ', ' ']
        self.assertEqual(self.game.check_winner(), 'O')
    
    def test_check_winner_draw(self):
        self.game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', 'O']
        self.game.moves_count = 9
        self.assertEqual(self.game.check_winner(), 'Draw')
    
    def test_check_winner_no_winner(self):
        self.game.board = ['X', 'O', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.game.moves_count = 2
        self.assertIsNone(self.game.check_winner())
    
    def test_find_winning_move(self):
        self.game.board = ['X', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        move = self.game._find_winning_move('X')
        self.assertEqual(move, 2)
        
        self.game.board = [' ', ' ', ' ', 'O', 'O', ' ', ' ', ' ', ' ']
        move = self.game._find_winning_move('O')
        self.assertEqual(move, 5)
    
    def test_random_move(self):
        self.game.board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', ' ']
        move = self.game._random_move()
        self.assertEqual(move, 8)
        
        self.game.board = ['X'] * 9
        move = self.game._random_move()
        self.assertIsNone(move)
    
    def test_update_game_state(self):
        self.game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
        self.game.update_game_state()
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.winner, 'X')
    
    def test_get_game_stats(self):
        self.game.make_move(0, 'X')
        self.game.make_move(1, 'O')
        stats = self.game.get_game_stats()
        
        self.assertEqual(stats['moves_made'], 2)
        self.assertFalse(stats['game_over'])
        self.assertIsNone(stats['winner'])
        self.assertEqual(len(stats['board_state']), 9)
    
    def test_save_and_load_game(self):
        self.game.make_move(0, 'X')
        self.game.make_move(1, 'O')
        self.game.current_player = 'X'
        
        self.assertTrue(self.game.save_game("test_save.json"))
        
        new_game = TicTacToeGame()
        self.assertTrue(new_game.load_game("test_save.json"))
        
        self.assertEqual(new_game.board, self.game.board)
        self.assertEqual(new_game.current_player, self.game.current_player)
        self.assertEqual(new_game.moves_count, self.game.moves_count)


if __name__ == '__main__':
    unittest.main()