#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CheckersGame.py
#  
#  Copyright 2013 [Natasha A Thomas, Vani S, Yedhu Krishnan]
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#   


import pygame
import sys
import time
import cv2
import cv

import numpy

numpy.set_printoptions(threshold=0, suppress=True)

# Class for representing Checkers Board
class CheckersBoard:
	board = []
	def __init__(self):
		# Representation of board as a list of lists (2D array type)
		self.board  = [[' ','b',' ','b',' ','b',' ','b'],
					   ['b',' ','b',' ','b',' ','b',' '],
					   [' ','b',' ','b',' ','b',' ','b'],
					   [' ',' ',' ',' ',' ',' ',' ',' '],
					   [' ',' ',' ',' ',' ',' ',' ',' '],
					   ['w',' ','w',' ','w',' ','w',' '],
					   [' ','w',' ','w',' ','w',' ','w'],
					   ['w',' ','w',' ','w',' ','w',' ']]
			  
	
	# Print the board on terminal
	def printboard(self):
		def print_line():
			print ('  ---------------------------------')
		column_list = '    a   b   c   d   e   f   g   h'
		row_num = 8
		for row in self.board:
			print_line()
			print (row_num)
			for col in row:
				print ('|', col)
			print ('|')
			row_num = row_num - 1
		print_line()
		print (column_list)
	
	# Make a non-capturing move
	def makemove(self, start_row, start_col, end_row, end_col):
		self.board[end_row][end_col] = self.board[start_row][start_col]
		self.board[start_row][start_col] = ' '
	
	# Make a capturing move
	def makecapturemove(self, start_row, start_col, end_row, end_col):
		self.board[end_row][end_col] = self.board[start_row][start_col]
		self.board[start_row][start_col] = ' '
		self.board[(start_row + end_row) / 2][(start_col + end_col) / 2] = ' '
	
	# Promote a piece to king
	def makeking(self, row, col):
		self.board[row][col] = self.board[row][col].upper()
	
	# Return the piece at given position
	def returnpiece(self, row, col):
		return self.board[row][col]
	
	# Return the whole board	
	def returnboard(self):
		return self.board

# Class for processing movements	
class Movement:
	# Make an object of CheckersBoard class
	checkers = CheckersBoard()
	whitesturn = False
	capture_list = []
	noncapture_list = []
	def __init__(self, board):
		self.checkers = board
		self.whitesturn = False	
		self.current_piece = 'b'
		self.opponent_piece = 'w'
		self.current_king = 'B'
		self.opponent_king = 'W'
		self.move_value = -1
		self.capture_value = -2
		
	def processmove(self, move):
		self.capture_list = []
		self.noncapture_list = []
		self.findturn()
		
		# Make a list (self.capture_list) of capturing moves
		self.make_capture_movelist()
		
		# print self.capture_list
		
		# If there is any capturing moves available, check if the input move is a capturing move
		if len(self.capture_list) > 0:
			invalid = True
			for capture_move in self.capture_list:
				if move == capture_move:
					invalid = False
			if invalid:
				print ('Not a capturing move')
				return
		else:
			self.make_noncapture_movelist()
			# print self.noncapture_list
		
		
		if len(move) == 5 and move[2] == '-':
			result = self.noncapturemove(move)
			if result:
				return True
			else:
				return False
		elif move[2] == 'x':
			result = self.capturemove(move)
			if result:
				return True
			else:
				return False
		else:
			print ('No such move')
			return False
	
	# Make a list (self.capture_list) of capturing moves
	def make_capture_movelist(self):
		#print self.current_piece	
		for row in range(0, 8):
			for col in range(0, 8):
				#print self.checkers.board[row][col],
				if self.checkers.board[row][col].lower() == self.current_piece:
					#print self.current_piece
					self.validcaptures(row, col, self.returncell(row, col), self.checkers.returnpiece(row, col))
		self.capture_list = [capture for capture in self.capture_list if len(capture) >= 5]
	
	
	def make_noncapture_movelist(self):
		#print self.current_piece
		for row in range(8):
				for col in range(8):
					if self.checkers.board[row][col].lower() == self.current_piece:
						#print self.current_piece
						self.validnoncaptures(row, col, self.returncell(row, col), self.checkers.returnpiece(row, col))
	
	# Function to check the currently playing & opponent piece 		
	def findturn(self):
			if self.whitesturn:
				self.current_piece = 'w'		# Currently playing piece
				self.opponent_piece = 'b'		# Opponent piece
				self.move_value = 1				# Valid difference value of (start_row - end_row) in non-capturing move
				self.capture_value = 2			# Valid difference value of (start_row - end_row) in capturing move
			else:
				self.current_piece = 'b'
				self.opponent_piece = 'w'
				self.move_value = -1
				self.capture_value = -2
			self.current_king = self.current_piece.upper()			
			self.opponent_king = self.opponent_piece.upper()
	
	# Check the validity of a non-capturing move
	def noncapturemove(self, move):
		(start_row, start_col) = self.processcell(move[0:2])
		(end_row, end_col) = self.processcell(move[3:5])
		
		if self.checkers.returnpiece(end_row, end_col) == ' ':
			if self.checkers.returnpiece(start_row, start_col) == self.current_piece:
				if (start_row - end_row) == self.move_value and abs(start_col - end_col) == 1:
					self.checkers.makemove(start_row, start_col, end_row, end_col)
					self.checkforking(end_row, end_col)
					self.whitesturn = not self.whitesturn
					return True
				else:
					print ('Invalid move')
					return False
			elif self.checkers.returnpiece(start_row, start_col) == self.current_king:
				if abs(start_row - end_row) == 1 and abs(start_col - end_col) == 1:
					self.checkers.makemove(start_row, start_col, end_row, end_col)
					self.checkforking(end_row, end_col)
					self.whitesturn = not self.whitesturn
					return True
			else:
				print ('Invalid move')
				return False
		else:
			print ('Invalid move')
			return False
					
	# Check the validity of a capturing move
	def capturemove(self, move):
		if len(move) >= 5:
			(start_row, start_col) = self.processcell(move[0:2])
			(end_row, end_col) = self.processcell(move[3:5])
			
			if (self.checkers.returnpiece(((start_row + end_row) / 2), ((start_col + end_col) / 2))).lower() == self.opponent_piece and move[2] == 'x':
				if self.checkers.returnpiece(start_row, start_col) == self.current_piece:
					if (start_row - end_row) == self.capture_value and abs(start_col - end_col) == 2:
						self.checkers.makecapturemove(start_row, start_col, end_row, end_col)
						self.checkforking(end_row, end_col)
						self.capturemove(move[3:])
					else:
						print ('Invalid capture')
				elif self.checkers.returnpiece(start_row, start_col) == self.current_king:
					if abs(start_row - end_row) == 2 and abs(start_col - end_col) == 2:
						self.checkers.makecapturemove(start_row, start_col, end_row, end_col)
						self.checkforking(end_row, end_col)
						self.capturemove(move[3:])
				else:
					print ('Invalid capture')
			else:
				print ('Invalid capture')
		else:
			self.whitesturn = not self.whitesturn
			return True
	
	# Check if any new kings are there on board		
	def checkforking(self, row, col):
		if (self.checkers.returnpiece(row, col) == 'w' and row == 0) or (self.checkers.returnpiece(row, col) == 'b' and row == 7):
			self.checkers.makeking(row, col)
			
	# Convert the Chess style cell representation to row and column number				
	def processcell(self, cell):
		col = ord(cell[0]) - 97
		row = 7 - (ord(cell[1]) - 49)
		return (row, col)
	
	# Return the cell representation	
	def returncell(self, row, col):
		return (chr(col + 97) +  chr((8 - row) + 48))
		
	def validnoncaptures(self, row, col, temp_move_string, piece):
		if piece == 'w':
			if row != 0:
				if 1 <= col <= 6:
					if self.checkers.returnpiece(row-1, col-1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row-1, col-1))
					if self.checkers.returnpiece(row-1, col+1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row-1, col+1))
				elif col == 0:
					if self.checkers.returnpiece(row-1, col+1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row-1, col+1))
				elif col == 7:
					if self.checkers.returnpiece(row-1, col-1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row-1, col-1))
		elif piece == 'b':
			if row != 7:
				if 1 <= col <= 6:
					if self.checkers.returnpiece(row+1, col-1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row+1, col-1))
					if self.checkers.returnpiece(row+1, col+1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row+1, col+1))
				elif col == 0:
					if self.checkers.returnpiece(row+1, col+1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row+1, col+1))
				elif col == 7:
					if self.checkers.returnpiece(row+1, col-1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row+1, col-1))
		elif piece == 'W' or piece == 'B':
			if row != 0:
				if 1 <= col <= 6:
					if self.checkers.returnpiece(row-1, col-1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row-1, col-1))
					if self.checkers.returnpiece(row-1, col+1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row-1, col+1))
				elif col == 0:
					if self.checkers.returnpiece(row-1, col+1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row-1, col+1))
				elif col == 7:
					if self.checkers.returnpiece(row-1, col-1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row-1, col-1))
			if row != 7:
				if 1 <= col <= 6:
					if self.checkers.returnpiece(row+1, col-1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row+1, col-1))
					if self.checkers.returnpiece(row+1, col+1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row+1, col+1))
				elif col == 0:
					if self.checkers.returnpiece(row+1, col+1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row+1, col+1))
				elif col == 7:
					if self.checkers.returnpiece(row+1, col-1) == ' ':
						self.noncapture_list.append(temp_move_string + '-' + self.returncell(row+1, col-1))		
					
	# Function to make a list of all valid captures available	
	def validcaptures(self, row, col, temp_move_string, piece):
		entered = False
		if piece == 'w':
			if row != 0 and row != 1:
				if 1 < col < 6:
					if self.checkers.returnpiece(row-1, col-1).lower() == self.opponent_piece and self.checkers.returnpiece(row-2, col-2) == ' ':
						move_string = temp_move_string + 'x' + (self.returncell(row-2, col-2))
						entered = True
						self.validcaptures(row-2, col-2, move_string, piece)
					if self.checkers.returnpiece(row-1, col+1).lower() == self.opponent_piece and self.checkers.returnpiece(row-2, col+2) == ' ':
						move_string = temp_move_string + 'x' + (self.returncell(row-2, col+2))
						entered = True
						self.validcaptures(row-2, col+2, move_string, piece)
				elif col == 0 or col == 1:
					if self.checkers.returnpiece(row-1, col+1).lower() == self.opponent_piece and self.checkers.returnpiece(row-2, col+2) == ' ':
						move_string = temp_move_string + 'x' + (self.returncell(row-2, col+2))
						entered = True
						self.validcaptures(row-2, col+2, move_string, piece)
				elif col == 6 or col == 7:
					if self.checkers.returnpiece(row-1, col-1).lower() == self.opponent_piece and self.checkers.returnpiece(row-2, col-2) == ' ':
						move_string = temp_move_string + 'x' + (self.returncell(row-2, col-2))
						entered = True
						self.validcaptures(row-2, col-2, move_string, piece)
					
		elif piece == 'b':
			if row != 6 and row != 7:
				if col > 1 and col < 6:
					if self.checkers.returnpiece(row+1, col+1).lower() == self.opponent_piece and self.checkers.returnpiece(row+2, col+2) == ' ':
						move_string = temp_move_string + 'x' + (self.returncell(row+2, col+2))
						entered = True
						self.validcaptures(row+2, col+2, move_string, piece) 
					if self.checkers.returnpiece(row+1, col-1).lower() == self.opponent_piece and self.checkers.returnpiece(row+2, col-2) == ' ':
						move_string = temp_move_string + 'x' + (self.returncell(row+2, col-2))
						entered = True
						self.validcaptures(row+2, col-2, move_string, piece)
				elif col == 0 or col == 1:
					if self.checkers.returnpiece(row+1, col+1).lower() == self.opponent_piece and self.checkers.returnpiece(row+2, col+2) == ' ':
						move_string = temp_move_string + 'x' + (self.returncell(row+2, col+2))
						entered = True
						self.validcaptures(row+2, col+2, move_string, piece)
				elif col == 6 or col == 7:
					if self.checkers.returnpiece(row+1, col-1).lower() == self.opponent_piece and self.checkers.returnpiece(row+2, col-2) == ' ':
						move_string = temp_move_string + 'x' + (self.returncell(row+2, col-2))
						entered = True
						self.validcaptures(row+2, col-2, move_string, piece)
					
		elif piece == 'B' or piece == 'W':
			if row != 0 and row != 1:
				if col > 1 and col < 6:
					if self.checkers.returnpiece(row-1, col-1).lower() == self.opponent_piece and self.checkers.returnpiece(row-2, col-2) == ' ' and temp_move_string.find(self.returncell(row-2, col-2)) == -1:
						move_string = temp_move_string + 'x' + (self.returncell(row-2, col-2))
						entered = True
						self.validcaptures(row-2, col-2, move_string, piece)
					if self.checkers.returnpiece(row-1, col+1).lower() == self.opponent_piece and self.checkers.returnpiece(row-2, col+2) == ' ' and temp_move_string.find(self.returncell(row-2, col+2)) == -1:
						move_string = temp_move_string + 'x' + (self.returncell(row-2, col+2))
						entered = True
						self.validcaptures(row-2, col+2, move_string, piece) 
				elif col == 0 or col == 1:
					if self.checkers.returnpiece(row-1, col+1).lower() == self.opponent_piece and self.checkers.returnpiece(row-2, col+2) == ' ' and temp_move_string.find(self.returncell(row-2, col+2)) == -1:
						move_string = temp_move_string + 'x' + (self.returncell(row-2, col+2))
						entered = True
						self.validcaptures(row-2, col+2, move_string, piece)
				elif col == 6 or col == 7:
					if self.checkers.returnpiece(row-1, col-1).lower() == self.opponent_piece and self.checkers.returnpiece(row-2, col-2) == ' ' and temp_move_string.find(self.returncell(row-2, col-2)) == -1:
						move_string = temp_move_string + 'x' + (self.returncell(row-2, col-2))
						entered = True
						self.validcaptures(row-2, col-2, move_string, piece) 
					
			if row != 6 and row != 7:
				if 1 < col < 6:
					if self.checkers.returnpiece(row+1, col+1).lower() == self.opponent_piece and self.checkers.returnpiece(row+2, col+2) == ' ' and temp_move_string.find(self.returncell(row+2, col+2)) == -1:
						move_string = temp_move_string + 'x' + (self.returncell(row+2, col+2))
						entered = True
						self.validcaptures(row+2, col+2, move_string, piece)
					if self.checkers.returnpiece(row+1, col-1).lower() == self.opponent_piece and self.checkers.returnpiece(row+2, col-2) == ' ' and temp_move_string.find(self.returncell(row+2, col-2)) == -1:
						move_string = temp_move_string + 'x' + (self.returncell(row+2, col-2))
						entered = True
						self.validcaptures(row+2, col-2, move_string, piece)
				elif col == 0 or col == 1:
					if self.checkers.returnpiece(row+1, col+1).lower() == self.opponent_piece and self.checkers.returnpiece(row+2, col+2) == ' ' and temp_move_string.find(self.returncell(row+2, col+2)) == -1:
						move_string = temp_move_string + 'x' + (self.returncell(row+2, col+2))
						entered = True
						self.validcaptures(row+2, col+2, move_string, piece)
				elif col == 6 or col == 7:
					if self.checkers.returnpiece(row+1, col-1).lower() == self.opponent_piece and self.checkers.returnpiece(row+2, col-2) == ' ' and temp_move_string.find(self.returncell(row+2, col-2)) == -1:
						move_string = temp_move_string + 'x' + (self.returncell(row+2, col-2))
						entered = True
						self.validcaptures(row+2, col-2, move_string, piece)
		if entered == False:
			self.capture_list.append(temp_move_string)
			return				
	
	def returnvalidcaptures(self):
		return self.capture_list

# Class to analyze the game status	
class FindWinner:
	checkers = CheckersBoard()
	def __init__(self, board):
		self.checkers = board
		self.isgameover = False
		self.white_wins = False
		self.black_wins = False
	
	# Check if the game is over	
	def gameover(self):
		flag_black = False
		flag_white = False
		for row in self.checkers.returnboard():
			if (row.count('w') + row.count('W')) > 0:
				flag_white = True
			if (row.count('b') + row.count('B')) > 0:
				flag_black = True
		if not flag_black:
			self.white_wins = True
			return True
		if not flag_white:
			self.black_wins = True
			return True
		return False
	
	# Return winner piece's name	
	def winner(self):
		if self.black_wins:
			return 'Black'
		if self.white_wins:
			return 'White'

# Convert the move into standard Chess format [Examples: e5-d6, b2xd4]
def notation(move):
	if move.find('-') > 0:
		move = move.split('-')
		char = '-'
	elif move.find('x') > 0:
		move = move.split('x')
		char = 'x'
	movestring = ''
	for board_cell in move:
		row = int(board_cell[0])
		col = int(board_cell[1])
		movestring = movestring + (chr(col + 97) + chr((8 - row) + 48) + char)
	return movestring[:len(movestring) - 1]
	
# Return the predicted board state for the input board state
def predict(data):
	num_input_layers = 32
	num_hidden_layers = 150
	num_output_layers = 128
	layers = numpy.array([num_input_layers, num_hidden_layers, num_output_layers])
	nnet = cv2.ANN_MLP(layers)
	nnet.load("trained_data.xml")

	inputData = cv.CreateMat(1, 32, cv.CV_32FC1)
	outputData = cv.CreateMat(1, 128, cv.CV_32FC1)
	
	for i in range(32):
		cv.SetReal2D(inputData, 0, i, data[i])

	ipData = numpy.asarray(inputData)
	opData=numpy.asarray(outputData)
	predictions = numpy.empty_like(opData)
	nnet.predict(ipData, predictions)

	return predictions[0]

# Convert the 2-D board into 1-D list to pass to the Neural Prediction Program
def make_row(board):
	piece_val = {' ': 0, 'b': 1, 'B': -1, 'w': 2, 'W': -2}
	int_board = list()
	for i in range(8):
		for j in range(8):
			if (i + j) % 2 == 1:
				int_board.append(piece_val[board[i][j]])
	return int_board

# Return the best move for the white	
def predict_move(move_list, temp_prediction, move_object):
	prediction = []
	for value in temp_prediction:
		prediction.append(0)
		prediction.append(value)	
	
	move_value = []
	splitchar = move_list[0][2]
	for move in move_list:
		smove = move.split(splitchar)
		(row, col) = move_object.processcell(smove[len(smove) - 1])
		if prediction[64 + row * 7 + col] > prediction[192 + row * 7 + col]:
			move_value.append(prediction[64 + row * 7 + col])
		else:
			move_value.append(prediction[192 + row * 7 + col])

	good_moves = []
	maxval = max(move_value)
	for i in range(len(move_list)):
		if move_value[i] == maxval:
			good_moves.append(move_list[i])

	if len(good_moves) == 1:
		return good_moves[0]
	else:
		move_value = []
		for move in good_moves:
			smove = move.split(splitchar)
			(row, col) = move_object.processcell(smove[0])
			if prediction[64 + row * 7 + col] < prediction[192 + row * 7 + col]:
				move_value.append(prediction[64 + row * 7 + col])
			else:
				move_value.append(prediction[192 + row * 7 + col])
		#print move_value
		minval = min(move_value)
		for i in range(len(good_moves)):
			if move_value[i] == minval:
				return good_moves[i]
			
def home_screen(screen, clock):
	done = False
	while True:
		clock.tick(50)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
		if event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				x = pos[0]
				y = pos[1]				
				if 220 <= x <=420 and 320 <= y <= 350:	
					return False
				elif 220 <= x <= 420 and 365 <= y <= 500:
					return True
		screen.fill([0, 0, 0])
		
		# Display title "Checkers"
		
		font = pygame.font.SysFont("arial", 172)
		text = font.render('checkers',True,(10,200,50),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)-200
		screen.blit(text, textRect)

		# Display text "Play now"
		font = pygame.font.SysFont("arial", 50)
		text = font.render('play now',True,(255,0,0),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)+10
		screen.blit(text, textRect)

		# Display text "Quit"
		font = pygame.font.SysFont("arial", 50)
		text = font.render('quit',True,(255,0,0),(0,0,0))	
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = (screen.get_rect().centery)+150
		screen.blit(text, textpos)

		pygame.display.update()
		pygame.display.flip()
	return True
	
def select_player(screen, clock):
	while True:	
		clock.tick(50)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					x = pos[0]
					y = pos[1]				
					if 220 <= x <=500 and 200 <= y <= 280:	
						return False
					elif 220 <= x <= 500 and 365 <= y <= 500:
						return True

		screen.fill([0, 0, 0])

		font = pygame.font.SysFont("arial", 172)
		text = font.render('checkers',True,(10,200,50),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)-200
		screen.blit(text, textRect)

		font = pygame.font.SysFont("arial", 50)
		text = font.render('single player',True,(255,0,0),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)-50
		screen.blit(text, textRect)
		
		font = pygame.font.SysFont("arial", 50)
		text = font.render('two player',True,(255,0,0),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)+100
		screen.blit(text, textRect)

		pygame.display.update()
		pygame.display.flip()
	return True
		
def black_wins(screen, clock):
	done = False
	while True:
		clock.tick(50)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				return True
		
		screen.fill([0, 0, 0])
		font = pygame.font.SysFont("arial", 40)
		text = font.render(' GAME OVER',True,(255,0,0),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)-50
		screen.blit(text, textRect)
					
		font = pygame.font.SysFont("arial", 30)
		text = font.render('RED WINS',True,(255,0,0),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)+10
		screen.blit(text, textRect)

		pygame.display.update()
		pygame.display.flip()
	return True

def white_wins(screen, clock):
	while True:
		clock.tick(50)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			if event.type == pygame.MOUSEBUTTONDOWN:
				return True
		
		screen.fill([0, 0, 0])
		font = pygame.font.SysFont("arial", 40)
		text = font.render(' GAME OVER',True,(255,0,0),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)-50
		screen.blit(text, textRect)
					
		font = pygame.font.SysFont("arial", 30)
		text = font.render('WHITE WINS',True,(255,0,0),(0,0,0))	
		textRect = text.get_rect()
		textRect.centerx = screen.get_rect().centerx
		textRect.centery = (screen.get_rect().centery)+10
		screen.blit(text, textRect)

		pygame.display.update()
		pygame.display.flip()
	return True

def main(): 
	# Colors defined for GUI Board
	black 		= (  0,   0,   0)
	green 		= (  0, 255,   0)
	white 		= (255, 255, 255)
	dark_red	= (200,   0,   0)
	red 		= (255,   0,   0)
	gray 		= (200, 200, 200)
	king_white 	= (180, 180, 180)
	king_red 	= (80,    0,   0) 
	
	while True:
		# Set width and height of each cell in the board
		(width, height) = (80, 80)
		pygame.init()
		size = [640, 640]
		screen = pygame.display.set_mode(size)
		pygame.display.set_caption("Checkers")	 
		clock = pygame.time.Clock()
		
		game_complete = False
		# Read option from home screen (Play Now or Quit)
		quit_game = home_screen(screen, clock)
		if quit_game:
			return
			
		two_player = select_player(screen, clock)

		first_click = False
		temp_row = -1
		temp_column = -1

		checkers = CheckersBoard()
		move = Movement(checkers)
		win = FindWinner(checkers)
		checkers.printboard()	
		board = checkers.returnboard()
		input_move = ''	
		game_winner = ''

		
		while True:
			# Find whose turn is next
			move.findturn()
			
			# Predict the white's move if it is not a two player game
			if move.whitesturn and not two_player:
				time.sleep(1)
				move.capture_list = []
				move.make_capture_movelist()
				if len(move.capture_list) > 0:
					move_list = move.capture_list
					print (move_list)
				else:
					move.noncapture_list = []
					move.make_noncapture_movelist()
					move_list = move.noncapture_list
					print (move_list)
				predicted_board = predict(make_row(checkers.returnboard()))
				input_move = predict_move(move_list, predicted_board, move)
				print (input_move)
				move.processmove(input_move)
				
			# Allow user to move black (and white if it is a two player game)
			else:
				for event in pygame.event.get(): 
					if event.type == pygame.QUIT:
						return
					if event.type == pygame.MOUSEBUTTONDOWN:
						pos = pygame.mouse.get_pos()
						# If click is outside the board
						if pos[0] > 640:
							continue
						# Change the x y screen coordinates to column and row
						column = 7 - pos[0] //  width
						row = 7 - pos[1] //  height
						print (row, column)
						
						if board[row][column] == 'b' or board[row][column] == 'w' or board[row][column] == 'B' or board[row][column] == 'W':
							first_click = True
							piece = board[row][column]
							(temp_row, temp_column) = (row, column)
							input_move = str(temp_row) + str(temp_column)
						elif first_click == True and board[row][column] == ' ':
							if row == temp_row and column == temp_column:
								input_move = notation(input_move)
								move.processmove(input_move)
								input_move = ''
							if abs(temp_column - column) == abs(temp_row - row) == 1:
								first_click = False
								char = '-'
								input_move = input_move + char + str(row) + str(column)
								input_move = notation(input_move)
								move.processmove(input_move)
								input_move = ''
							else:
								char = 'x'
								input_move = input_move + char + str(row) + str(column)
						(temp_row, temp_column) = (row, column)	
						
			checkers.printboard()
			if win.gameover():
				print (win.winner(), 'wins!')
				game_winner = win.winner()
				break
					
			# Fill the whole screen with black color
			screen.fill(black)
			# Draw the Checkers Board and pieces
			for row in range(8):
				for column in range(8):
					if (row + column) % 2 == 0:
						color = white
					else:
						color = black
					board_row = 7 - row
					board_column = 7 - column
					pygame.draw.rect(screen, color, [width * column, height * row, width, height])
					if (board_row, board_column) == (temp_row, temp_column):
						pygame.draw.rect(screen, green, [width * column, height * row, width, height])
					if board[board_row][board_column] == 'b':
						pygame.draw.circle(screen, dark_red, [(width * column + width * (column + 1)) / 2, (height * row + height * (row + 1)) / 2], 30, 0)
					elif board[board_row][board_column] == 'w':
						pygame.draw.circle(screen, gray, [(width * column + width * (column+1)) / 2,(height * row + height * (row+1)) / 2], 30, 0)
					elif board[board_row][board_column] == 'B':
						pygame.draw.circle(screen, dark_red, [(width * column + width * (column+1)) / 2,(height * row + height * (row+1)) / 2], 30, 0)
						pygame.draw.circle(screen, king_red, [(width * column + width * (column+1)) / 2,(height * row + height * (row+1)) / 2], 25, 0)
					elif board[board_row][board_column] == 'W':
						pygame.draw.circle(screen, gray, [(width * column + width * (column+1)) / 2,(height * row + height * (row+1)) / 2], 30, 0)
						pygame.draw.circle(screen, king_white, [(width * column + width * (column+1)) / 2,(height * row + height * (row+1)) / 2], 25, 0)
						
			#pygame.draw.rect(screen, gray, [650, 10, 340, 620])				
			clock.tick(20)
			pygame.display.flip()
		
		if game_winner == 'Black':
			while black_wins(screen, clock):
				break
		elif game_winner == 'White':
			while white_wins(screen, clock):
				break
				
	pygame.quit()

if __name__ == '__main__':
	main()

