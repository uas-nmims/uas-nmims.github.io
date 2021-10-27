CHECKERS USING ARTIFICIAL NEURAL NETWORKS
-----------------------------------------

The program CheckersGame.py is the graphical interface developed for the game of Checkers. The program is written in python. The game can be played in 2 modes:

>> Single Player  	- The human player plays RED and the computer plays WHITE
>> Two Player		- Between two human players

In single player game, the computer moves are made by predicting the move by analyzing the current board position from an existing trained data (TrainedData/trained_data.xml). The trained data is created by implementing a neural network and training it with 300000+ sample moves


HOW TO PLAY?
------------
Note that the game always starts with RED pieces.

TO MAKE A NON CAPTURING MOVE
----------------------------
1. Click on the cell containing the piece to be moved
2. Click on the destination square

TO MAKE A CAPTURING MOVE
------------------------
1. Click on the cell containing the piece to be moved
2. Double click on the destination cell

Examples: 
|  Suppose you want to make a capturing move 6x11
|  
|  1. Single click on cell 6
|  2. Double click on cell 11
|  
|  Suppose you want to make a capturing move 1x5x9, then
|  
|  1. Single click on cell 1
|  2. Single click on cell 5
|  3. Double click on cell 9


The cell numbering is as follows:

	WHITE'S SIDE
	---------------------------------
	|   | 1 |   | 2 |   | 3 |   | 4 |
	---------------------------------
	| 5 |   | 6 |   | 7 |   | 8 |   |
	---------------------------------
	|   | 9 |   | 10|   | 11|   | 12|
	---------------------------------
	| 13|   | 14|   | 15|   | 17|   |
	---------------------------------
	|   | 18|   | 19|   | 20|   | 21|
	---------------------------------
	| 22|   | 23|   | 24|   | 25|   |
	---------------------------------
	|   | 26|   | 27|   | 28|   | 29|
	---------------------------------
	| 30|   | 31|   | 32|   | 33|   |
	---------------------------------
	RED'S SIDE
	
				
						
