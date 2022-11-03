import numpy as np
import pygame
import math

BLUE = (0,35,255)
BLACK = (1,1,1)
RED = (255,35,0)
YELLOW = (200,255,0)

ROW = 6
COLUMN = 7

def create_board(row, column):
    return np.zeros((row,column))

def is_valid_location(board, row, col):
    return board[row][col] == 0

def drop_piece(board, row, col, num):
	board[row][col] = num

def winning_move(board, num):
	for column in range(COLUMN-3): # Check horizontal row
		for row in range(ROW):
			if board[row][column] == num and board[row][column+1] == num and board[row][column+2] == num and board[row][column+3] == num:
				return True
	for column in range(COLUMN): # Check vertical columns
		for row in range(ROW-3):
			if board[row][column] == num and board[row+1][column] == num and board[row+2][column] == num and board[row+3][column] == num:
				return True
	for column in range(COLUMN-3): # Check positively sloped diaganols (bottom left to upper right)
		for row in range(ROW-3):
			if board[row][column] == num and board[row+1][column+1] == num and board[row+2][column+2] == num and board[row+3][column+3] == num:
				return True
	for column in range(COLUMN-3): # Check negatively sloped diaganols (upper left to bottom right)
		for row in range(3, ROW):
			if board[row][column] == num and board[row-1][column+1] == num and board[row-2][column+2] == num and board[row-3][column+3] == num:
				return True

def draw_board(board):
    for column in range(COLUMN):
        for row in reversed(range(ROW)):
            pygame.draw.rect(screen, BLUE, (column * size, (row + 1) * size, size, size))
            if board[row][column] == 1:
                pygame.draw.circle(screen, RED, (int((column + 0.5) * size), int((row + 1.5) * size)), RADIUS)
            elif board[row][column] == 2:
                pygame.draw.circle(screen, YELLOW, (int((column + 0.5) * size), int((row + 1.5) * size)), RADIUS)
            else:
                pygame.draw.circle(screen, BLACK, (int((column + 0.5) * size), int((row + 1.5) * size)), RADIUS)
    pygame.display.update()

GameBoard = create_board(ROW, COLUMN)

running = True
turns = 1
PLAYER_NUM = 2

pygame.init()

size = 50
width = COLUMN * size
height = (ROW + 1) * size
RADIUS = int(size / 2 - 5)

screen = pygame.display.set_mode((width, height))
pygame.display.update()

player = 1

draw_board(GameBoard)
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, size))
            posx = event.pos[0]
            if player == 1:
                pygame.draw.circle(screen, RED, (posx, int(size / 2)), RADIUS)
            elif player == 2: 
                pygame.draw.circle(screen, YELLOW, (posx, int(size / 2)), RADIUS)
        
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, size))
            posx = event.pos[0]
            try:
                column = int(math.floor(posx / size))
                for row in reversed(range(ROW)):
                    is_full_column = True # This is just an assumption
                    if is_valid_location(GameBoard, row, column):
                        drop_piece(GameBoard, row, column, player)
                        print(GameBoard)
                        if winning_move(GameBoard, player):
                            raise Exception(f"\nPlayer {player} wins\n")
                        is_full_column = False # Contradicts the assumption above if the program found a blank space in that column
                        break
                if is_full_column: # But if the assumption is still True
                    print(f"Column {column + 1} is full! Try again")
            except IndexError:
                print("The column you are specifying does not even exist!")
            except ValueError:
                print("You entered something invalid. Try again.")
            except Exception as error:
                print(error)
                running = False
                break

            draw_board(GameBoard)

            if player == 1:
                player = 2
            elif player == 2:
                player = 1
