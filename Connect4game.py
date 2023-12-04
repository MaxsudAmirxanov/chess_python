#Authors Ulu Musazada, Ilham Bakhishov, Marya Tikhomirova and Hasan Azizli

import random

class Connect4:
    def __init__(self):
        self.rows = 6
        self.columns = 7
        self.grid = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]

    def recommendcolumn(self):
        available_columns = [col for col in range(1, self.columns + 1) if self.grid[0][col - 1] == ' ']
        if available_columns:
            recommended_column = random.choice(available_columns)
            print(f"Recommended column to play: {recommended_column}")
            return recommended_column
        else:
            print("No available columns to play.")
            return None
    
    def recommendcolumnlongestalignment(self, color):
        availablecolumns = [col for col in range(1, self.columns + 1) if self.grid[0][col - 1] == ' ']
        maxalignmentlength = 0
        recommendedcolumn = None

        for column in availablecolumns:
            for row in range(self.rows, 0, -1):
                if self.grid[row - 1][column - 1] == ' ':
                    alignmentlength, _ = self.longestalignment(column, row, color)
                    if alignmentlength > maxalignmentlength:
                        maxalignmentlength = alignmentlength
                        recommendedcolumn = column
        if recommendedcolumn is not None:
            print(f"Recommended column to play: {recommendedcolumn} for the longest alignment.")
        else:
            print("No available columns to play.")

        return recommendedcolumn
     
    #Exercise5
    def droppingdisc(self, column, color):
        row = self.findingemptyrow(column)
        if row is not None:
            self.grid[row][column - 1] = color
            print(f"{color} disc dropped in column {column}.")
            return True
        else:
            print(f"Column {column} is full. Choose another column.")
            return False
        
    def findingemptyrow(self, column):
        for row in range(self.rows - 1, -1, -1):
            if self.grid[row][column - 1] == ' ':
                return row
        return None
    
    def longestalignmentlength(self, column, row):
        color = self.grid[row][column - 1]

        horizontallength = self.check_direction(column, row, 1, 0, color)

        verticallength = self.check_direction(column, row, 0, 1, color)

        diagonal1length = self.check_direction(column, row, 1, 1, color)

        diagonal2length = self.check_direction(column, row, 1, -1, color)

        return max(horizontallength, verticallength, diagonal1length, diagonal2length)
    
    def check_direction(self, column, row, delta_x, delta_y, color):
        length = 1  # Start with the current disc
        current_column, current_row = column + delta_x, row + delta_y

        while 0 <= current_column < self.columns and 0 <= current_row < self.rows:
            if self.grid[current_row][current_column - 1] == color:
                length += 1
                current_column += delta_x
                current_row += delta_y
            else:
                break

        return length
     
    def displayinggrid(self):
        col_numbers_top = ' '.join(map(str, range(1, self.columns + 1)))
        print(f'   {col_numbers_top}')


        for i, row in zip(range(self.rows, 0, -1), self.grid):
            row_numbers_left = f' {i}  '
            row_numbers_right = f'{i}'
            discs = [f'(*)' if disc == 'R' else 'o' if disc == 'Y' else ' ' for disc in row]
            print(row_numbers_left + ' '.join(discs) + row_numbers_right)


        col_numbers_bottom = ' '.join(map(str, range(1, self.columns + 1)))
        print(f'   {col_numbers_bottom}')
#Exercise4.
    def ismovevalid(self, column):
        if 1 <= column <= self.columns:
            if self.grid[0][column - 1] == ' ':
                return True
            else:
                return False
        else:
            return False

    def cleargridfull(self):
        if all(self.grid[0][i] != ' ' for i in range(self.columns)):
            self.grid = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
            print("Grid cleared because all columns are full.")
            

#Exercise 1
connect4_game = Connect4()

#Exercise 2
connect4_game.cleargridfull

#Exercise 3
connect4_game.displayinggrid()

#Exercise 4 is given in code itself

#Exercise 5 Example usage
connect4_game.droppingdisc(5, 'R')
connect4_game.displayinggrid()

#Exercise 6 Example usage
column, row = 5, 4
alignment_length = Connect4.longestalignmentlength(self,column,row)
print(f"Longest alignment length at ({column}, {row}): {alignment_length}")
#Exercise 7 
recommended_column = connect4_game.recommend_random_column()

#Exercise 8 Example usage
recommended_column = connect4_game.recommend_column_with_longest_alignment('Y') #recommends a column with the longest alignment of yellow discs
