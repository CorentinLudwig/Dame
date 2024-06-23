import pygame
import numpy as np
from const import *
from board import *

pygame.init()


def get_cell(pos):
    x, y = pos
    col = x // tile_size
    row = y // tile_size
    return row, col


window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Dame")
clock = pygame.time.Clock()

window.fill(BLACK)


board = Board(window, board1)
board.draw_board()

is_piece_selected = False
piece_selected = (None,None)
running = True
player = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row, col = get_cell(mouse_pos)
            print(f'Clicked row: {row}, col: {col}')
            if(is_piece_selected):
                if(board.mov_possible(row,col,piece_selected) and not board.player_can_take(player)):
                    board.mov(row,col,piece_selected)
                    player = (player + 1)%2
                elif(board.take_possible(row,col,piece_selected)):
                    board.take(row,col,piece_selected)
                    piece_selected = (row,col)
                    while(board.piece_can_take(piece_selected)):
                        board.draw_board()
                        board.select(piece_selected[0], piece_selected[1])
                        pygame.display.flip()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = pygame.mouse.get_pos()  
                                row, col = get_cell(mouse_pos)
                                if(board.take_possible(row,col,piece_selected)):
                                    board.take(row,col,piece_selected)
                                    piece_selected = (row,col)
                    player = (player + 1)%2
                else:
                    if board.player_can_take(player):
                        print('prise obligatoir')
                    print('mouvement impossible')
                board.draw_board()
                is_piece_selected = False
                piece_selected = (None,None)
            else:
                if(board.board[row,col] == player):
                    board.select(row,col)
                    is_piece_selected = True
                    piece_selected = (row,col)

    pygame.display.flip()
    
pygame.quit()