class ChessGame:

    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.current_player = 'white'
        self.white_pieces = ['p', 'n', 'b', 'q', 'k', 'r']
        self.black_pieces = ['P', 'N', 'B', 'Q', 'K', 'R']
        self.castling_rights = {'white': {'king_side': True, 'queen_side': True},
                                'black': {'king_side': True, 'queen_side': True}}

    def _print_board(self):
        "Вторая версия доски"
        print("    a b c d e f g h")
        print("  +----------------")
        for i, row in enumerate(self.board, 1):
            print(f"{i} | {' '.join(row)}")
        print()

    def print_board(self):
        "Первая версия доски"
        st = '    '
        a=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
        # a.reverse()
        # st+= str(index_row)
        for i in a:
            st= st + str(i) + ' | '
        print(st)
        # print('--  --  --  --  --  --  --  --')
        for index_row, row in enumerate(self.board):
            # index_row= 7-index_row
            # print(' '.join(str(piece) for piece in row))

            # print(st)
            print('   --  --  --  --  --  --  --  --')
            st=''
            st= st + str(index_row +1) 
            for index, i in enumerate(row):
                # print(i)
                st= st+ ' | ' + i
            st+=' | '
            print(st)

    def is_valid_move(self, start, end):
        "Проверка на правильность хода"
        start_row, start_col = start
        end_row, end_col = end

        

        if not (1 <= start_row <= 8 and 1 <= start_col <= 8 and 1 <= end_row <= 8 and 1 <= end_col <= 8):
            print(1)
            return False  # Check if positions are within the board

        if self.is_occupied_by_own_piece(end) == False:
            # print(2)
            return False  # Cannot move to a position occupied by own piece

        piece = self.board[start_row - 1][start_col - 1].lower()

        if piece == ' ':
            return False

        if piece == 'p' and not self.valid_pawn_move(start, end):
            return False
        elif piece == 'r' and not self.valid_rook_move(start, end):
            return False
        elif piece == 'n' and not self.valid_knight_move(start, end):
            return False
        elif piece == 'b' and not self.valid_bishop_move(start, end):
            return False
        elif piece == 'q' and not self.valid_queen_move(start, end):
            return False
        elif piece == 'k' and not self.valid_king_move(start, end):
            return False

        return True
    def valid_pawn_move(self, start, end):
        "Проверка хода пешки"
        start_row, start_col = start
        end_row, end_col = end

        if self.current_player == 'white' and start_row==2 and end_row==4:
            return True
        if self.current_player == 'black' and start_row==7 and end_row==5:
            return True 

        direction = 1 if self.current_player == 'white' else -1

        # White pawn moves forward
        if start_col == end_col and start_row + direction == end_row and self.board[end_row - 1][end_col - 1] == ' ':
            return True
        # Black pawn moves forward
        elif start_col == end_col and start_row - direction == end_row and self.board[end_row - 1][end_col - 1] == ' ':
            return True
        # Pawn captures diagonally
        elif abs(start_col - end_col) == 1 and start_row + direction == end_row and self.board[end_row - 1][end_col - 1].islower() != self.board[start_row - 1][start_col - 1].islower():
            return True
        else:
            return False

    def valid_rook_move(self, start, end):
        "Check the rook's move"
        start_row, start_col = start
        end_row, end_col = end
        if self.board[end_row-1][end_col-1] in self.black_pieces and self.current_player == 'white':
            print()
            return True
        if self.board[end_row-1][end_col-1] in self.white_pieces and self.current_player == 'black':
            return True
        # Check if the move is either vertical or horizontal
        if start_row != end_row and start_col != end_col:
            return False

        # Determine the direction of movement
        row_direction = 0 if start_row == end_row else 1 if end_row > start_row else -1
        col_direction = 0 if start_col == end_col else 1 if end_col > start_col else -1

        # Check for obstacles in the path
        current_row, current_col = start_row + row_direction, start_col + col_direction
        while current_row != end_row or current_col != end_col:
            if self.board[current_row - 1][current_col - 1] != ' ':
                return False  # Obstacle in the path
            current_row += row_direction
            current_col += col_direction

        return True  # No obstacles in the path
    def valid_knight_move(self, start, end):
        "Проверка хода коня"
        start_row, start_col = start
        end_row, end_col = end

        # Knight moves in an "L" shape
        return (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2)

    def valid_bishop_move(self, start, end):
        "Check the bishop's move"
        start_row, start_col = start
        end_row, end_col = end
        if self.board[end_row-1][end_col-1] in self.black_pieces and self.current_player == 'white':
            print()
            return True
        if self.board[end_row-1][end_col-1] in self.white_pieces and self.current_player == 'black':
            return True
        # Check if the move is diagonal
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False

        # Determine the direction of movement
        row_direction = 1 if end_row > start_row else -1
        col_direction = 1 if end_col > start_col else -1

        # Check for obstacles in the diagonal path
        current_row, current_col = start_row + row_direction, start_col + col_direction
        while (current_row != end_row) and (current_col != end_col):
            if (current_row == end_row) and (current_col == end_col):
                break  # Reached the destination, allow capturing

            if self.board[current_row - 1][current_col - 1] != ' ':
                return False  # Obstacle in the path

            current_row += row_direction
            current_col += col_direction

        return True  # No obstacles in the path

    def valid_queen_move(self, start, end):
        "Проверка хода королевы"

        return self.valid_rook_move(start, end) or self.valid_bishop_move(start, end)

    def valid_king_move(self, start, end):
        "Проверка хода кораля"
        start_row, start_col = start
        end_row, end_col = end

        # King moves one square in any direction
        return abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1

    def is_occupied_by_own_piece(self, end):
        "Проверка на то что наш ход не будет приходить на нашу же фигуру"
        end_row, end_col = end
        # print(end)
        # print(self.board[end_row - 1][end_col - 1])
        if self.board[end_row - 1][end_col - 1] in self.black_pieces and self.current_player == 'black':
            return False
        if self.board[end_row - 1][end_col - 1] in self.white_pieces and self.current_player == 'white':
            return False
        # return self.board[end_row - 1][end_col - 1].islower() == (self.current_player == 'white')

    def make_move(self, start, end):
        if self.is_valid_move(start, end) and not self.is_occupied_by_own_piece(end):
            start_row, start_col = start
            end_row, end_col = end
            self.board[end_row - 1][end_col - 1] = self.board[start_row - 1][start_col - 1]
            self.board[start_row - 1][start_col - 1] = ' '
            self.switch_player()
        else:
            print("Invalid move. Try again.")

    def switch_player(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    # Additional rules (castling, en passant, checkmate, etc.) can be implemented here
     
    def check_end(self, start, end):
        "Проверка на то что короля съели"
        start_row, start_col = start
        end_row, end_col = end
        if self.board[end_row - 1][end_col - 1] == 'q':
            #СЪели белого короля
            return 'black', True
        elif self.board[end_row - 1][end_col - 1] == 'Q':
            #Сели белого короля
            return 'white', True 
        else:
            return '', False 
        
    #-----------------------------------------------------------------------------------------
    def is_checkmate(self):
        "Проверка на мат"
        king_position = self.find_king_position()

        # Check if the king is in check
        if not self.is_in_check(king_position):
            return False  # The king is not in check, no checkmate

        # Check if there are any legal moves to get out of check
        for i in range(8):
            for j in range(8):
                start = (king_position[0] + 1, king_position[1] + 1)
                end = (i + 1, j + 1)

                if self.is_valid_move(start, end) and not self.is_occupied_by_own_piece(end):
                    # There is at least one legal move
                    return False

        return True  # No legal moves found, checkmate

    def is_stalemate(self):
        king_position = self.find_king_position()

        # Check if the king is not in check
        if self.is_in_check(king_position):
            return False  # The king is in check, not stalemate

        # Check if there are any legal moves for the current player
        for i in range(8):
            for j in range(8):
                start = (i + 1, j + 1)

                if self.board[i][j].lower() in self.get_current_player_pieces():
                    for x in range(8):
                        for y in range(8):
                            end = (x + 1, y + 1)

                            if self.is_valid_move(start, end) and not self.is_occupied_by_own_piece(end):
                                # There is at least one legal move
                                return False

        return True  # No legal moves found for the current player, stalemate

    def is_in_check(self, king_position):
        # Check if the king is under threat
        for i in range(8):
            for j in range(8):
                start = (i + 1, j + 1)
                end = king_position

                if self.is_valid_move(start, end) and not self.is_occupied_by_own_piece(end):
                    return True

        return False

    def find_king_position(self):
        # Find the current player's king position
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if (self.current_player == 'white' and piece == 'k') or \
                        (self.current_player == 'black' and piece == 'K'):
                    return (i + 1, j + 1)

    def get_current_player_pieces(self):
        return self.white_pieces if self.current_player == 'white' else self.black_pieces   

def admission_defeat(start):
    if start.lower() == 's':
        return True
    else:
        return False


def get_user_input():
    """
    Получаем иныормацию от пользователя и возвращаем кориетж в понятном виде для алгоритма.
    То есть а2, а3 --> ((2, 1), (3, 1))
    """
    try:
        start = input("Enter the starting position (e.g., a2): ").lower()
        # if admission_defeat(start) == True:
        #     print(f'The game is over, the player has admitted defeat')
        #     exit()
        if start =='s':
            return 's'
        
        end = input("Enter the ending position (e.g., a4): ").lower()
        if end =='s':
            return 's'
        # if admission_defeat(end) == True:
        #     print(f'The game is over, the player has admitted defeat')
        #     exit()
        # print(len(end))
        
        if len(start) != 2 or len(end) != 2:
            return False
        
        return (int(start[1]), ord(start[0]) - ord('a') + 1), (int(end[1]), ord(end[0]) - ord('a') + 1)
    except:
        return False
def main():
    'Цикличный запуск нашей программы'
    game = ChessGame()

    while True:
        
        game.print_board()
        print(f"\n{game.current_player}'s turn:")
        print('Enter "s" to stop the game and admit defeat')
        result = get_user_input()
        if result == 's':
            print(f'The game is over, the player has admitted defeat')
            exit()
        if result == False:
            print("Incorrect data entry. Try again.")
            continue
        else:
            start, end = result
        # print(result)

        game.make_move(start, end)

        # result = game.check_end(start, end)
        # if result[1] == True:
        #     print(f"{result[0]} wen !!!")
        #     exit()

        # if game.is_stalemate():
        #     print("Stalemate! The game is a draw.")
        #     print(3)
        #     exit()

if __name__ == "__main__":
    main()