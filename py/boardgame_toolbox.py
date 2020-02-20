"""
Monte Carlo Tree Search project
* BoardGame class
* Tic_Tac_Toe_Board class
"""

import numpy as np
import matplotlib.pyplot as plt

class BoardGame:
	def __init__(self,initBoard):
		self.board = initBoard

	def getAllPossibleStates(self):
		pass

class Tic_Tac_Toe_Board(BoardGame):
	def __init__(self,initBoard=None,nPlayers=2,emptyValue=-9):
		BoardGame.__init__(self,initBoard)
		self.playerIDList = list(range(1,nPlayers+1))
		self.nextPlayerID = [-13]+self.playerIDList[1:]+[self.playerIDList[0]]
		self.emptyValue = emptyValue
		if self.board is None:
			self.board = np.ones((3,3))*self.emptyValue

	def getAllPossibleStates(self,playerId):
		empty_pos = np.nonzero(self.board==self.emptyValue)
		if len(empty_pos[0])==0:
			return []
		else:
			allPossibleStates = []
			for newpos in zip(*empty_pos):
				temp_board = np.array(self.board)
				temp_board[newpos] = playerId
				allPossibleStates +=[temp_board]
			return allPossibleStates

	def simulateRandomPlay(self,startingPlayerID):
		simul_boardGame = Tic_Tac_Toe_Board(self.board)
		simul_playerID = int(startingPlayerID)
		while not simul_boardGame.hasEnded() and simul_boardGame.getWinner()==0:
			#simul_boardGame.showBoard()
			allPossibleStates = simul_boardGame.getAllPossibleStates(simul_playerID)
			simul_boardGame.board = allPossibleStates[np.random.choice(list(range(len(allPossibleStates))))]
			simul_playerID = self.nextPlayerID[simul_playerID]
		#simul_boardGame.showBoard()
		return simul_boardGame.getWinner()

	def hasEnded(self):
		empty_pos = np.nonzero(self.board==self.emptyValue)
		if len(empty_pos[0])==0:
			return True
		else:
			return False

	def getWinner(self):
		B = np.array(self.board)
		size,_ = B.shape

		#look in rows
		for i in range(size):
			s = B[i,:]
			for id_ in self.playerIDList:
				#if (s==np.ones(size)*id_).all():
				if np.sum(s==np.ones(size)*id_)==size:
					return id_

		#look in colonns
		for j in range(size):
			s = B[:,j]
			for id_ in self.playerIDList:
				#if (s==np.ones(size)*id_).all():
				if np.sum(s==np.ones(size)*id_)==size:
					return id_		

		#look in diagonal
		s = np.diag(B)
		for id_ in self.playerIDList:
			#if (s==np.ones(size)*id_).all():
			if np.sum(s==np.ones(size)*id_)==size:
				return id_		

		#look in diagonal
		for i in range(len(B)): 
			row = B[i,:]
			B[i,:]=row[::-1] 
		s = np.diag(B)
		for id_ in self.playerIDList:
			#if (s==np.ones(size)*id_).all():
			if np.sum(s==np.ones(size)*id_)==size:
				return id_

		#print('No player wins : draw')
		return 0

	def showBoard(self,nPlayers=2,listColors=['red','blue'],listMarkers=['X','o']):
		board_img = np.ones((3,3,3))*255
		board_img = board_img.astype(np.uint8)

		plt.xlim(0, 3)
		plt.ylim(0, 3)
		plt.imshow(board_img)
		#plt.title('tic tac toe board')

		plt.xticks([])
		plt.yticks([])
		
		plt.axvline(0,0,1,color=(0,0,0),linewidth=3)
		plt.axvline(1,0,1,color=(0,0,0),linewidth=3)
		plt.axvline(2,0,2,color=(0,0,0),linewidth=3)
		plt.axvline(3,0,2,color=(0,0,0),linewidth=3)

		plt.axhline(0,0,3,color=(0,0,0),linewidth=3)
		plt.axhline(1,0,3,color=(0,0,0),linewidth=3)
		plt.axhline(2,0,3,color=(0,0,0),linewidth=3)
		plt.axhline(3,0,3,color=(0,0,0),linewidth=3)

		for id_ in self.playerIDList:
			pos_player = np.nonzero(self.board==id_)
			pos_player = list(zip(*pos_player))

			for pos in pos_player:
				plt.scatter(pos[1]+0.5,2-pos[0]+0.5,c=listColors[id_-1],marker=listMarkers[id_-1],s=2000)
		
		plt.show()