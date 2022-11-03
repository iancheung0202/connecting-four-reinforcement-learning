import numpy as np
import pygame
import math
import random

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

def winning(board, num):
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

def opponent_move(board, num):
	while num > 0:
		for column in range(COLUMN-3): # Check horizontal row
			for row in range(ROW):
				if board[row][column] == 0 and board[row][column+1] == num and board[row][column+2] == num and board[row][column+3] == num:
					return [column, row]
				if board[row][column+1] == 0 and board[row][column] == num and board[row][column+2] == num and board[row][column+3] == num:
					return [column + 1, row]
				if board[row][column+2] == 0 and board[row][column] == num and board[row][column+1] == num and board[row][column+3] == num:
					return [column + 2, row]
				if board[row][column+3] == 0 and board[row][column] == num and board[row][column+1] == num and board[row][column+2] == num:
					return [column + 3, row]

		for column in range(COLUMN): # Check vertical columns
			for row in range(ROW-3):
				if board[row][column] == 0 and board[row+1][column] == num and board[row+2][column] == num and board[row+3][column] == num:
					return [column, row]
				if board[row+1][column] == 0 and board[row][column] == num and board[row+2][column] == num and board[row+3][column] == num:
					return [column, row + 1]
				if board[row+2][column] == 0 and board[row][column] == num and board[row+1][column] == num and board[row+3][column] == num:
					return [column, row + 2]
				if board[row+3][column] == 0 and board[row][column] == num and board[row+1][column] == num and board[row+2][column] == num:
					return [column, row + 3]

		for column in range(COLUMN-3): # Check positively sloped diaganols (bottom left to upper right)
			for row in range(ROW-3):
				if board[row][column] == 0 and board[row+1][column+1] == num and board[row+2][column+2] == num and board[row+3][column+3] == num:
					return [column, row]
				if board[row+1][column+1] == 0 and board[row][column] == num and board[row+2][column+2] == num and board[row+3][column+3] == num:
					return [column + 1, row + 1]
				if board[row+2][column+2] == 0 and board[row][column] == num and board[row+1][column+1] == num and board[row+3][column+3] == num:
					return [column + 2, row + 2]
				if board[row+3][column+3] == 0 and board[row][column] == num and board[row+1][column+1] == num and board[row+2][column+2] == num:
					return [column + 3, row + 3]

		for column in range(COLUMN-3): # Check negatively sloped diaganols (upper left to bottom right)
			for row in range(3, ROW):
				if board[row][column] == 0 and board[row-1][column+1] == num and board[row-2][column+2] == num and board[row-3][column+3] == num:
					return [column, row]
				if board[row-1][column+1] == 0 and board[row][column] == num and board[row-2][column+2] == num and board[row-3][column+3] == num:
					return [column + 1, row - 1]
				if board[row-2][column+2] == 0 and board[row][column] == num and board[row-1][column+1] == num and board[row-3][column+3] == num:
					return [column + 2, row - 2]
				if board[row-3][column+3] == 0 and board[row][column] == num and board[row-1][column+1] == num and board[row-2][column+2] == num:
					return [column + 3, row - 3]
				
		num -= 1
	
	return [random.randint(0, COLUMN-1), random.randint(0, ROW-1)]

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

font = pygame.font.SysFont("monospace", 35)

player = 1

draw_board(GameBoard)
while running:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# if event.type == pygame.MOUSEMOTION:
			# pygame.draw.rect(screen, BLACK, (0,0, width, size))
			# posx = event.pos[0]
			# if player == 1:
			# 	pygame.draw.circle(screen, RED, (posx, int(size / 2)), RADIUS)

			# elif player == 2: 
			#     pygame.draw.circle(screen, YELLOW, (posx, int(size / 2)), RADIUS)
		
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			while True:
				if running:
					searchingForNonFullColumns = True
					while searchingForNonFullColumns:
						coordinates = opponent_move(GameBoard, player)
						column = coordinates[0]
						row = coordinates[1]
						for row in reversed(range(ROW)):
							is_column_full = True
							if is_valid_location(GameBoard, row, column):
								drop_piece(GameBoard, row, column, player)
								print(GameBoard)
								if winning(GameBoard, player):
									label = font.render(f"Player {player} wins!!", 1, RED)
									screen.blit(label, (20,10))
									print(f"Player {player} won!")
									running = False
								is_column_full = False
								break
						if not is_column_full:
							break

				player += 1

				draw_board(GameBoard)

				if running:
					searchingForNonFullColumns = True
					while searchingForNonFullColumns:
						coordinates = opponent_move(GameBoard, player)
						column = coordinates[0]
						row = coordinates[1]
						for row in reversed(range(ROW)):
							is_column_full = True
							if is_valid_location(GameBoard, row, column):
								drop_piece(GameBoard, row, column, player)
								print(GameBoard)
								if winning(GameBoard, player):
									label = font.render(f"Player {player} wins!!", 1, YELLOW)
									screen.blit(label, (20,10))
									print(f"Player {player} won!")
									running = False
								is_column_full = False
								break
						if not is_column_full:
							break

					player = 1
					draw_board(GameBoard)

				if not running:
					pygame.time.wait(2000)
					break