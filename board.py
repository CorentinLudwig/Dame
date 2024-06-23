from const import *
import numpy as np
import pygame


class Board:
    def __init__(self, window, board) -> None:
        self.window = window
        self.board = board.copy()

    def mov(self, row, col, piece_selected):
        self.board[row, col] = self.board[piece_selected]
        self.board[piece_selected] = -1
            
    def take(self, row, col, piece_selected):
        self.board[row, col] = self.board[piece_selected]
        self.board[piece_selected] = -1
        row_piece, col_piece = piece_selected
        self.board[(row+row_piece)//2 , (col+col_piece)//2] = -1
    
    def draw_board(self):
        for row in range(board_size):
            for col in range(board_size):
                rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
                if (row + col) % 2 == 0:
                    color = WHITE
                else:
                    color = GRAY
                pygame.draw.rect(self.window, color, rect)
                
                if self.board[row, col] == 0:
                    pygame.draw.circle(self.window, WHITE, rect.center, tile_size // 2 - 5)
                elif self.board[row, col] == 1:
                    pygame.draw.circle(self.window, BLACK, rect.center, tile_size // 2 - 5)
    
    def select(self, row,col):
        rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
        if self.board[row, col] == 0:
            pygame.draw.circle(self.window, WHITE, rect.center, tile_size // 2)
        elif self.board[row, col] == 1:
            pygame.draw.circle(self.window, BLACK, rect.center, tile_size // 2)
            
    def mov_possible(self, row, col, piece_selected) -> bool:
        row_piece, col_piece = piece_selected
        color = self.board[piece_selected]
        
        if(color == 0):
            if row == row_piece-1 and (col == col_piece-1 or col == col_piece+1):
                return self.board[row, col] == -1
        elif(color == 1):
            if row == row_piece+1 and (col == col_piece-1 or col == col_piece+1):
                return self.board[row, col] == -1
        return False
    
    def take_possible(self, row, col, piece_selected) -> bool:
        row_piece, col_piece = piece_selected
        color = self.board[piece_selected]
        
        if(color == 0):
            if((row == row_piece-2 or row == row_piece+2) and (col == col_piece-2 or col == col_piece+2)): #prise de pion
                return self.board[(row+row_piece)//2 , (col+col_piece)//2] == 1 and self.board[row, col] == -1
        elif(color == 1):
            if((row == row_piece-2 or row == row_piece+2) and (col == col_piece-2 or col == col_piece+2)):
                return self.board[(row+row_piece)//2 , (col+col_piece)//2] == 0 and self.board[row, col] == -1
        return False
        
    def piece_can_take(self, piece) -> bool:
        row, col = piece
        color = self.board[row, col]
        
        if color == -1:
            return False
        
        color_take = (color + 1)%2

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row+dr < self.board.shape[0] and 0 <= new_col+dc < self.board.shape[1]:
                if self.board[new_row, new_col] == color_take and self.board[new_row+dr, new_col+dc] == -1:
                    return True
    
        return False

    def player_can_take(self, player)->bool:
        for row in range(board_size):
            for col in range(board_size):
                if self.board[row,col] == player:
                    if self.piece_can_take((row,col)):
                        return True
        return False