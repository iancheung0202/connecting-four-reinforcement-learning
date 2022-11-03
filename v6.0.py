import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

AI_1 = 0
AI_2 = 1

DEPTH = 4

EMPTY = 0
AI_1_PIECE = 1
AI_2_PIECE = 2

WINDOW_LENGTH = 4

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_available_row_in_column(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def check_winning_move(board, num):
	for column in range(COLUMN_COUNT-3): # Check horizontal row
		for row in range(ROW_COUNT):
			if board[row][column] == num and board[row][column+1] == num and board[row][column+2] == num and board[row][column+3] == num:
				return True
	for column in range(COLUMN_COUNT): # Check vertical columns
		for row in range(ROW_COUNT-3):
			if board[row][column] == num and board[row+1][column] == num and board[row+2][column] == num and board[row+3][column] == num:
				return True
	for column in range(COLUMN_COUNT-3): # Check positively sloped diaganols (bottom left to upper right)
		for row in range(ROW_COUNT-3):
			if board[row][column] == num and board[row+1][column+1] == num and board[row+2][column+2] == num and board[row+3][column+3] == num:
				return True
	for column in range(COLUMN_COUNT-3): # Check negatively sloped diaganols (upper left to bottom right)
		for row in range(3, ROW_COUNT):
			if board[row][column] == num and board[row-1][column+1] == num and board[row-2][column+2] == num and board[row-3][column+3] == num:
				return True

def count_windows(window, piece):
	score = 0
	opp_piece = AI_1_PIECE
	if piece == AI_1_PIECE:
		opp_piece = AI_2_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 50
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 20

	if window.count(opp_piece) == 4:
		score -= 90
	elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 40
	elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
		score -= 10

	return score

def score_position(board, piece):
	score = 0
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Horizontal
	for row in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[row,:])]
		for column in range(COLUMN_COUNT-3):
			window = row_array[column:column+WINDOW_LENGTH]
			score += count_windows(window, piece)

	## Vertical
	for column in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,column])]
		for row in range(ROW_COUNT-3):
			window = col_array[row:row+WINDOW_LENGTH]
			score += count_windows(window, piece)

	## Positive-sloped diagonal
	for row in range(ROW_COUNT-3):
		for column in range(COLUMN_COUNT-3):
			window = [board[row+i][column+i] for i in range(WINDOW_LENGTH)]
			score += count_windows(window, piece)

	# Negative-sloped diagonal
	for row in range(ROW_COUNT-3):
		for column in range(COLUMN_COUNT-3):
			window = [board[row+3-i][column+i] for i in range(WINDOW_LENGTH)]
			score += count_windows(window, piece)

	return score

def get_valid_locations(board):
	valid_locations = []
	for column in range(COLUMN_COUNT):
		if is_valid_location(board, column):
			valid_locations.append(column)
	return valid_locations

def pick_best_move(board, piece):
	valid_locations = get_valid_locations(board)
	best_score = -1000000
	best_column = []
	for column in valid_locations:
		row = get_available_row_in_column(board, column)
		temporary_board = board.copy() # Copy a board to test how it is when dropping the piece
		drop_piece(temporary_board, row, column, piece) # Drop the piece on the duplicate board
		score = score_position(temporary_board, piece) # Evaluate the score
		if score > best_score: # If we arrive at a better position
			best_score = score 
			best_column.clear()
			best_column.append(column)
		elif score == best_score:
			best_score = score
			best_column.append(column)
			
	return random.choice(best_column)

def draw_board(board):
	for column in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (column * box_size, (row + 1) * box_size, box_size, box_size))
			pygame.draw.circle(screen, BLACK, (int((column + 0.5) * box_size), int((row + 1.5) * box_size)), radius)
	
	for column in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):		
			if board[row][column] == AI_1_PIECE:
				pygame.draw.circle(screen, RED, (int((column + 0.5) * box_size), height-int((row + 0.5) * box_size)), radius)
			elif board[row][column] == AI_2_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int((column + 0.5) * box_size), height-int((row + 0.5) * box_size)), radius)
	pygame.display.update()

def minimax(board, depth, x, y, player_piece, maximizingPlayer):
	if player_piece == 1:
		piece = 1
		opp_piece = 2
	elif player_piece == 2:
		piece = 2
		opp_piece = 1

	valid_locations = get_valid_locations(board)
	terminal = check_winning_move(board, opp_piece) or check_winning_move(board, piece) or len(get_valid_locations(board)) == 0
	
	if terminal:
		if check_winning_move(board, piece):
			return (None, 100000)
		elif check_winning_move(board, opp_piece):
			return (None, -100000)
		else: # Game is over, no more valid moves
			return (None, 0)
	elif depth == 0:
			return (None, score_position(board, piece))

	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_available_row_in_column(board, col)
			temporary_board = board.copy()
			drop_piece(temporary_board, row, col, piece)
			new_score = minimax(temporary_board, depth - 1, x, y, piece, False)[1]
			if new_score > value:
				value = new_score
				column = col
			x = max(x, value)
			if x >= y:
				break
		return column, value

	elif not maximizingPlayer: 
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_available_row_in_column(board, col)
			temporary_board = board.copy()
			drop_piece(temporary_board, row, col, opp_piece)
			new_score = minimax(temporary_board, depth - 1, x, y, piece, True)[1]
			if new_score < value:
				value = new_score
				column = col
			y = min(y, value)
			if x >= y:
				break
		return column, value

board = create_board()
print_board(board)
game_over = False
first_move_done = False

pygame.init()
pygame.display.set_caption('Connecting four but with AI')
pygame.display.set_icon(pygame.image.load('Logo.png'))
myfont = pygame.font.SysFont("monospace", 75)

box_size = 100
radius = int(box_size/2 - 5)
width = COLUMN_COUNT * box_size
height = (ROW_COUNT+1) * box_size
size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

turn = random.randint(AI_1, AI_2)
while not game_over:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		pygame.display.update()
	
	if turn == AI_1:
		if not first_move_done:		
			drop_piece(board, 0, random.randint(0,6), AI_1_PIECE)
			first_move_done = True
			print_board(board)
			draw_board(board)
			turn += 1
		else:
			col = random.randint(0, COLUMN_COUNT-1)
			# col = pick_best_move(board, AI_1_PIECE)
			col, minimax_score = minimax(board, DEPTH, -math.inf, math.inf, turn + 1, True)
			if is_valid_location(board, col):
				row = get_available_row_in_column(board, col)
				drop_piece(board, row, col, AI_1_PIECE)
				if check_winning_move(board, AI_1_PIECE):
					label = myfont.render("RED AI wins!", 1, RED)
					screen.blit(label, (100,10))
					game_over = True
				print_board(board)
				draw_board(board)
				turn += 1
			
	if turn == AI_2 and not game_over:
		if not first_move_done:		
			drop_piece(board, 0, random.randint(0,6), AI_2_PIECE)
			first_move_done = True
			print_board(board)
			draw_board(board)
			turn -= 1
		else:
			col = random.randint(0, COLUMN_COUNT-1)
			# col = pick_best_move(board, AI_2_PIECE)
			col, minimax_score = minimax(board, DEPTH, -math.inf, math.inf, turn + 1, True)
			if is_valid_location(board, col):
				row = get_available_row_in_column(board, col)
				drop_piece(board, row, col, AI_2_PIECE)
				if check_winning_move(board, AI_2_PIECE):
					label = myfont.render("YELLOW AI wins!", 1, YELLOW)
					screen.blit(label, (20,10))
					game_over = True
				print_board(board)
				draw_board(board)
				turn -= 1

	if game_over:
		pygame.time.wait(5000)