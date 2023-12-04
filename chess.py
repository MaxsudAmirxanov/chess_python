import pygame

class Chess:

    def __init__(self):

        """
        Initialize the chessboard with initial configurations.
        """
        
        self.board = [
            ["BR", "BH", "BB", "BQ", "BK", "BB", "BH", "BR"], #0
            ["BP", "BP", "BP", "BP", "BP", "BP", "BP", "BP"], #1
            [0, 0, 0, 0, 0, 0, 0, 0], #2
            [0, 0, 0, 0, 0, 0, 0, 0], #3
            [0, 0, 0, 0, 0, 0, 0, 0], #4
            [0, 0, 0, 0, 0, 0, 0, 0], #5
            ["WP", "WP", "WP", "WP", "WP", "WP", "WP", "WP"], #6
            ["WR", "WH", "WB", "WQ", "WK", "WB", "WH", "WR"], #7
        ]
        self.player1pieces = [] # Store player 1's eaten pieces
        self.player2pieces = [] # Store player 2's eaten pieces
        self.moves_log = []  # Store moves history
        self.white_king_altered = False  # Track if white king has moved
        self.black_king_altered = False  # Track if black king has moved
        self.white_king_check = False
        self.white_king_mated = False
        self.black_king_check = False
        self.black_king_mated = False

    def get_possible_pawn_moves(self, y, x, king ):

        """
        Get possible moves for a pawn at position (y, x).

        Args:
        - y (int): Row index of the pawn.
        - x (int): Column index of the pawn.
        - is_king (bool): Indicates if this function is used in self.king().

        Returns:
        - List: List of possible moves for the pawn. May include "transform" if the pawn reaches the opposite end of the board.
        """

        possible_moves = []
        piece_color = self.board[y][x][0]
        
        # Define pawn's movement based on its color
        if piece_color == "W":
            moves = [[y - 1, x - 1], [y - 1, x], [y - 1, x + 1]]
            if y == 6:  # First move for white
                moves.append([y - 2, x])
        else:
            moves = [[y + 1, x - 1], [y + 1, x], [y + 1, x + 1]]
            if y == 1:  # First move for black
                moves.append([y + 2, x])

        # Exclude certain moves 
        excluding_moves = [[y - 1, x], [y - 2, x], [y + 1, x], [y + 2, x]]
        for move in moves:
            new_y, new_x = move
            if 0 <= new_x <= 7:
                if ((bool(self.board[new_y][new_x]) and self.board[new_y][new_x][0] != piece_color) or king) and move not in excluding_moves:
                    move.append("attack")
                    possible_moves.append(move)
                elif not bool(self.board[new_y][new_x]) and move in excluding_moves:
                    move.append("free")
                    possible_moves.append(move)

        # Transformation when reaching the opposite end of the board
        if (y - 1 == 0 and piece_color == "W") or (y + 1 == 7 and piece_color == "B"):
            possible_moves.append("transform")

        return possible_moves
    
    def get_possible_rook_moves(self, y, x):

        """
        Get possible moves for a rook at position (y, x).

        Args:
        - y (int): Row index of the rook.
        - x (int): Column index of the rook.

        Returns:
        - List: List of possible moves for the rook.
        """

        possible_moves = []  # Store all possible moves for the rook
        rook_color = self.board[y][x][0]  # Identify the color of the rook

        # Check rows - horizontal movement
        for x_left in range(x - 1, -1, -1):  # Check left side
            current_piece = self.board[y][x_left]
            if bool(current_piece):
                if rook_color != current_piece[0]:  # Check for enemy pieces to attack
                    possible_moves.append([y, x_left, "attack"])
                break
            else:
                possible_moves.append([y, x_left, "free"])

        for x_right in range(x + 1, 8):  # Check right side
            current_piece = self.board[y][x_right]
            if bool(current_piece):
                if rook_color != current_piece[0]:  # Check for enemy pieces to attack
                    possible_moves.append([y, x_right, "attack"])
                break
            else:
                possible_moves.append([y, x_right, "free"])

        # Check columns - vertical movement
        for y_above in range(y - 1, -1, -1):  # Check above
            current_piece = self.board[y_above][x]
            if bool(current_piece):
                if rook_color != current_piece[0]:  # Check for enemy pieces to attack
                    possible_moves.append([y_above, x, "attack"])
                break
            else:
                possible_moves.append([y_above, x, "free"])

        for y_below in range(y + 1, 8):  # Check below
            current_piece = self.board[y_below][x]
            if bool(current_piece):
                if rook_color != current_piece[0]:  # Check for enemy pieces to attack
                    possible_moves.append([y_below, x, "attack"])
                break
            else:
                possible_moves.append([y_below, x, "free"])

        return possible_moves 
    
    def get_possible_knight_moves(self, y, x):

        """
        Get possible moves for a knight at position (y, x).

        Args:
        - y (int): Row index of the knight.
        - x (int): Column index of the knight.

        Returns:
        - List: List of possible moves for the knight.
        """

        possible_moves = []  # Store all possible moves for the knight
        knight_color = self.board[y][x][0]  # Identify the color of the knight
        moves = [
            (y + 1, x - 2), (y + 2, x - 1), (y + 2, x + 1), (y + 1, x + 2),
            (y - 1, x - 2), (y - 2, x - 1), (y - 2, x + 1), (y - 1, x + 2)
        ]  # Define all potential knight moves

        # Iterate through each potential move and check for its validity
        for move in moves:
            new_y, new_x = move
            # Ensure the move is within the board boundaries
            if 0 <= new_y <= 7 and 0 <= new_x <= 7:
                # Check if the destination cell is occupied
                if bool(self.board[new_y][new_x]):
                    # If occupied, check if it's an enemy piece to attack
                    if knight_color != self.board[new_y][new_x][0]:
                        possible_moves.append([new_y, new_x, "attack"])
                else:
                    # If the cell is empty, it's a valid free move
                    possible_moves.append([new_y, new_x, "free"])

        return possible_moves

    def get_possible_bishop_moves(self, y, x):

        """
        Get possible moves for a bishop at position (y, x).

        Args:
        - y (int): Row index of the bishop.
        - x (int): Column index of the bishop.

        Returns:
        - List: List of possible moves for the bishop.
        """

        possible_moves = []  # Store all possible moves for the bishop
        bishop_color = self.board[y][x][0]  # Identify the color of the bishop
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonal directions

        for direction in directions:  # Check each diagonal direction
            dx, dy = direction
            current_y, current_x = y + dy, x + dx

            while 0 <= current_y <= 7 and 0 <= current_x <= 7:
                if bool(self.board[current_y][current_x]):
                    if bishop_color != self.board[current_y][current_x][0]:  # Check for enemy pieces to attack
                        possible_moves.append([current_y, current_x, "attack"])
                    break
                else:
                    possible_moves.append([current_y, current_x, "free"])  # Add free move

                current_y += dy
                current_x += dx

        return possible_moves

    def get_possible_queen_moves(self, y, x):

        """
        Get possible moves for a queen at position (y, x).

        Args:
        - y (int): Row index of the queen.
        - x (int): Column index of the queen.

        Returns:
        - List: List of possible moves for the queen.
        """

        possible_moves = []  # Store all possible moves for the queen
        # Combine possible moves from rook and bishop movements
        possible_moves.extend(self.get_possible_rook_moves(y, x))
        possible_moves.extend(self.get_possible_bishop_moves(y, x))

        return possible_moves  
    
    def get_possible_king_moves(self, y, x, win ):
        """
        Get possible moves for a king at position (y, x).

        Args:
        - y (int): Row index of the king.
        - x (int): Column index of the king.

        Returns:
        - List: List of possible moves for the king.
        """

        possible_moves = []  # Store all possible moves for the king
        king_color = self.board[y][x][0]  # Determine the color of the king

        # Define all possible moves for the king in all directions
        all_moves = [
            (y + 1, x - 1), (y + 1, x), (y + 1, x + 1),
            (y, x - 1), (y, x + 1), (y - 1, x - 1), (y - 1, x), (y - 1, x + 1)
        ]

        for move in all_moves:
            new_y, new_x = move
            if 0 <= new_y <= 7 and 0 <= new_x <= 7:  # Check if the move is within the board boundaries
                if bool(self.board[new_y][new_x]):
                    # Determine if it's a valid attack move
                    if king_color != self.board[new_y][new_x][0]:
                        possible_moves.append([new_y, new_x, "attack"])
                else:
                    possible_moves.append([new_y, new_x, "free"])

        if win:
            return possible_moves

        # Excluding illegal moves by checking against possible enemy moves

        illegal_moves = []
        for row in range(8):
            for col in range(8):
                for move in possible_moves:
                    current_piece = self.board[row][col]
                    if bool(current_piece) and current_piece[0] != king_color:
                        enemy_piece = current_piece[1]
                        # Check if enemy piece can attack king, mark it as illegal
                        if enemy_piece != "K" and enemy_piece != "P" and move in self.get_possible_moves(row, col):
                            illegal_moves.append(move)
                        elif enemy_piece != "K" and enemy_piece == "P" and move in self.get_possible_pawn_moves(row, col,True):
                            illegal_moves.append(move)

        # Filter out illegal moves from the possible moves
        possible_moves = [move for move in possible_moves if move not in illegal_moves]

        # Mark if king's possible moves have been changed at least once
        if king_color == "W" and [y, x] == [7, 4] and len(possible_moves) != 0:
            self.white_king_altered = True
        elif king_color == "B" and [y, x] == [0, 4] and len(possible_moves) != 0:
            self.black_king_altered = True

        return possible_moves 
    
    def get_king_cootdinates(self,color):
            
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == color+"K":
                        return [i,j]


    def get_possible_moves(self, y, x):
        
        """
        Get possible moves for a piece at position (y, x).

        Args:
        - y (int): Row index of the piece.
        - x (int): Column index of the piece.

        Returns:
        - List: List of possible moves for the piece at (y, x).
        """

        piece = self.board[y][x]
        figures = {
            "P": lambda y, x: self.get_possible_pawn_moves(y, x, False),
            "R": self.get_possible_rook_moves,
            "H": self.get_possible_knight_moves,
            "B": self.get_possible_bishop_moves,
            "Q": self.get_possible_queen_moves,
            "K": lambda y, x: self.get_possible_king_moves(y,x,False)
        }

        
        if self.white_king_check:
            if piece[1] in figures:
                possible_moves = []
                for move in figures[piece[1]](y, x):
                    y,x = self.get_king_cootdinates("W")
                    if move in self.get_possible_king_moves(y,x,True):
                        possible_moves.append(move)
                return(possible_moves)
        elif self.black_king_check:
            if piece[1] in figures:
                possible_moves = []
                for move in figures[piece[1]](y, x):
                    y,x = self.get_king_cootdinates("B")
                    if move in self.get_possible_king_moves(y,x,True):
                        possible_moves.append(move)
                return(possible_moves)
            

        if piece[1] in figures:
            return figures[piece[1]](y, x)
        else:
            return []

    def move(self, y1, x1, y2, x2):

        """
        Move a piece from (y1, x1) to (y2, x2) if it's a valid move.

        Args:
        - y1 (int): Row index of the piece to move.
        - x1 (int): Column index of the piece to move.
        - y2 (int): Destination row index.
        - x2 (int): Destination column index.

        Returns:
        - bool: True if the move is successful, False otherwise.
        """

        def perform_move():
            # Update player pieces and move log
            if bool(self.board[y2][x2]):
                piece_color = self.board[y2][x2][0]
                if piece_color == "B":
                    self.player1pieces.append(self.board[y2][x2][0])
                else:
                    self.player2pieces.append(self.board[y2][x2][0])

            self.moves_log.append([self.board[y1][x1], x2, y2])

            # Execute the move on the board
            moved_piece = self.board[y1][x1]
            self.board[y2].pop(x2)
            self.board[y2].insert(x2, moved_piece)
            self.board[y1].pop(x1)
            self.board[y1].insert(x1, 0)

        possibles = self.get_possible_moves(y1, x1)

        if possibles and possibles[-1] == "transform" and ([y2, x2, "attack"] in possibles or [y2, x2, "free"] in possibles):
            perform_move()
            self.checkmated()
            # Promote the pawn to queen if it reaches the opposite end
            self.board[y2][x2] = self.board[y2][x2][0] + "Q"
            return True
        elif [y2, x2, "attack"] in possibles or [y2, x2, "free"] in possibles:
            perform_move()
            self.checkmated()
            return True
        else:
            return False
       
    def checkmated(self):

        y1, x1 = self.get_king_cootdinates("W")
        moves_king_white = self.get_possible_king_moves(y1,x1,True)
        y2, x2 = self.get_king_cootdinates("B")
        moves_king_black = self.get_possible_king_moves(y2, x2,True)

        if len(moves_king_white) == 0 and self.white_king_altered:
            self.white_king_check = True
            self.white_king_mate = True
            moves_king_white = self.get_possible_king_moves(y1, x1, True)
            for row in range(8):
                for col in range(8):
                    for move in moves_king_white:
                        current_piece = self.board[row][col]
                        if bool(current_piece) and current_piece[0] == "W" :
                            ally_piece = current_piece[1]
                            # Check if ally piece can defend king
                            if ally_piece != "K" and move in self.get_possible_moves(row, col):
                                self.white_king_mate = False
                                break
        else :
            self.white_king_check = False
            self.white_king_mate = False

        if len(moves_king_black) == 0 and self.black_king_altered:
            self.black_king_check = True
            self.black_king_mate = True
            moves_king_black = self.get_possible_king_moves(y1, x1, True)
            for row in range(8):
                for col in range(8):
                    for move in moves_king_white:
                        current_piece = self.board[row][col]
                        if bool(current_piece) and current_piece[0] == "B" :
                            ally_piece = current_piece[1]
                            # Check if ally piece can defend king
                            if ally_piece != "K" and move in self.get_possible_moves(row, col):
                                self.black_king_mate = False
                                break
        else :
            self.black_king_check = False
            self.black_king_mate = False

    def win(self):

        if self.white_king_check and self.white_king_mate and self.white_king_altered :
            return True  # Black wins because the white king is checkmated or stalemated
        elif self.black_king_check and self.black_king_mate and self.black_king_altered :
            return True  # White wins because the black king is checkmated or stalemated
        else:
            return False  # Game is still ongoing

class Game:

    def __init__(self, chess):

        """
        Initialize the game instance.

        Args:
        - chess: Chess object to manage game logic.
        """

        self.chess = chess
        self.screen = pygame.display.set_mode((640, 800))  # Set up game window
        pygame.display.set_caption("Chess Game")  # Set window title
        icon = pygame.image.load("final_project/chess/images/icon.png")
        pygame.display.set_icon(icon)  # Set window icon
        self.background = pygame.image.load("final_project/chess/images/background.png")  # Load background image
        #self.font = pygame.font.Font("final_project/chess/images/TitilliumWeb-Regular.ttf", 40) # Initialize font
        self.clock = pygame.time.Clock()  # Manage game time
        self.running = True  # Flag to keep the game running
        self.target = False  # Flag to track if a piece is selected
        self.selection = True  # Flag to track player's selection ability
        self.turn = "W"  # Current player turn
        self.x1 = 0  # Store x-coordinate of the selected piece
        self.y1 = 0  # Store y-coordinate of the selected piece


    def render_game(self):

        """
        Render the current state of the chessboard on the screen.
        """
        
        rows = range(160,800,80)
        cols = range(0,640,80)
        """if self.target and self.chess.board[self.y1][self.x1][1] == "B" :
            rows = range(799,160,-80)
            cols = range(639,0,-80)"""

        # Loop through the board coordinates and render the pieces
        for row in rows:  # Iterate through rows
            for col in cols:  # Iterate through columns
                # Get the piece at the current coordinates
                piece = self.chess.board[row // 80 - 2][col // 80]
                if self.target and [row // 80 - 2,col // 80] == [self.y1,self.x1]:
                    piece_img = pygame.image.load("final_project/chess/images/" + piece + ".png")
                    pygame.mouse.get_pos()
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    self.screen.blit(piece_img, (x-40, y-40))
                else:
                    if piece != 0 :
                        # Load and display the piece image on the screen
                        piece_img = pygame.image.load("final_project/chess/images/" + piece + ".png")
                        self.screen.blit(piece_img, (col, row))
                

    def render_possibles(self, x1, y1):
        
        """
        Renders the possible moves for a selected piece.

        Args:
        - x1 (int): Column index of the selected piece.
        - y1 (int): Row index of the selected piece.
        """

        # Iterate through possible moves for the selected piece
        for move in self.chess.get_possible_moves(y1, x1):
            y = move[0]
            x = move[1]
            if move != "transform" and self.chess.board[y][x] != "WK" and self.chess.board[y][x] != "BK":
                # Display images indicating possible moves on the screen
                image_path = "final_project/chess/images/" + move[2] + ".png"
                position = (move[1] * 80, (move[0] + 2) * 80)  # Adjusting position for rendering
                self.screen.blit(pygame.image.load(image_path), position)

    def datagui(self):

        pass



    def run(self):

        """
        Executes the main game loop.
        """

        start_time = pygame.time.get_ticks()  # Start time

        while self.running:
            
            # Calculate elapsed time
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) // 1000  # in seconds

            # Setting up the game screen
            self.screen.blit(self.background, (0, 0))
            self.render_game()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.selection and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.x1 = event.pos[0] // 80
                    self.y1 = event.pos[1] // 80 - 2
                    if self.chess.board[self.y1][self.x1] != 0 and self.chess.board[self.y1][self.x1][0] == self.turn:
                        self.target = True
                        self.selection = False
                elif not self.selection and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x2 = event.pos[0] // 80
                    y2 = event.pos[1] // 80 - 2
                    if self.chess.move(self.y1, self.x1, y2, x2):
                        self.target = False
                        self.selection = True
                        self.turn = "B" if self.turn == "W" else "W"
                    else:
                        self.target = False
                        self.selection = True
        
            if self.target:
                self.render_possibles(self.x1, self.y1)

            if self.chess.win():
                print(self.turn + " wins")
                self.running = False

            # Displaying the timer
            #timer_text = self.font.render("Time: {elapsed_time}", True, (255, 255, 255))
            #self.screen.blit(timer_text, (10, 10))

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

# Create a Chess instance
chess = Chess()

# Create a ChessGame instance and run the game
game = Game(chess)
game.run()