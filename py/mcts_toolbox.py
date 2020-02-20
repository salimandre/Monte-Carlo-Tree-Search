"""
Monte Carlo Tree Search project
* Node class
* State class
* MonteCarloTreeSearch class
"""

import numpy as np
from time import time
from random import shuffle

from boardgame_toolbox import BoardGame, Tic_Tac_Toe_Board

CONST_UCB = 1.4

class Node:
	def __init__(self,state,parent_node=None,childs_list=[]):
		self.state = state
		self.parent = parent_node
		self.childs_list = childs_list;

	def addChild(self,childNode):
		self.childs_list = self.childs_list + [childNode]
		childNode.parent = self

	def isFullyExpanded(self):
		return len(self.childs_list)==len(self.state.boardGame.getAllPossibleStates(self.state.playerId))

	def optimistic_selection(self):

		if self.isFullyExpanded() and not self.state.boardGame.hasEnded() and self.state.boardGame.getWinner()==0:
			best_UCB = -1e6
			#print('\nlooking for best child USB...')
			for i, child in enumerate(self.childs_list):
				child_UCB = child.state.reward/child.state.visitCount + CONST_UCB * np.sqrt(np.log(self.state.visitCount)/child.state.visitCount)
				#print('child_UCB: ', child_UCB)
				if child_UCB > best_UCB:
					best_UCB_child_i = i
					best_UCB = child_UCB
			return self.childs_list[best_UCB_child_i].optimistic_selection()

		else:
			return self

	def expand(self):
		allPossibleStates = self.state.boardGame.getAllPossibleStates(self.state.playerId)
		shuffle(allPossibleStates)
		existingStates = [child.state.boardGame.board for child in self.childs_list]

		i = 0
		while np.any([np.all(allPossibleStates[i]==s) for s in existingStates]):
			i+=1

		newState = State(Tic_Tac_Toe_Board(allPossibleStates[i]), self.state.boardGame.nextPlayerID[self.state.playerId])
		newNode = Node(newState)
		self.addChild(newNode)
		return newNode

	# function for backpropagation 
	def backpropagate(self, winnerId,winReward,drawReward):
		tempNode = self
		while tempNode!=None:
			tempNode.update_stats(winnerId,winReward,drawReward)
			tempNode = tempNode.parent

	def update_stats(self, winnerId,winReward,drawReward):
		self.state.visitCount = self.state.visitCount + 1
		if  self.parent==None or self.parent.state.playerId==winnerId:
			self.state.reward = self.state.reward + winReward
		elif winnerId==0:
			self.state.reward = self.state.reward + drawReward

class State:
	def __init__(self,boardGame,playerId,visitCount=0,reward=0):
		self.boardGame=boardGame
		self.playerId=playerId
		self.visitCount=visitCount
		self.reward=reward

class MonteCarloTreeSearch:
	def __init__(self, boardGame,playerId,winReward=3,drawReward=1):
		self.root = Node(State(boardGame,playerId));
		self.nNodes=0
		self.winReward=winReward
		self.drawReward=drawReward
	#def __init__(self, root_node):
	#	self.root = root_node;

	def getBestRootChild(self): 
		best_reward=-1e6
		for i, child in enumerate(self.root.childs_list):
			if child.state.reward > best_reward:
				best_child_i = i
				best_reward = child.state.reward
		return self.root.childs_list[best_child_i]

	def findNextMove(self, Thinkingtime):
	#define an end time which will act as a terminating condition
		startClock = time()
		endClock = time()
		#for iter in tqdm(range(nIter)):
		i = 0
		while endClock - startClock < Thinkingtime:
			#print('endClock - startClock: ', endClock-startClock)
			selectedNode = self.root.optimistic_selection()
			if not selectedNode.state.boardGame.hasEnded() and selectedNode.state.boardGame.getWinner()==0:

				newLeaf = selectedNode.expand()
				self.nNodes+=1
				outcome = newLeaf.state.boardGame.simulateRandomPlay(newLeaf.state.playerId)
				newLeaf.backpropagate(outcome,self.winReward,self.drawReward)
			else:
				outcome = selectedNode.state.boardGame.getWinner()
				selectedNode.backpropagate(outcome,self.winReward,self.drawReward)
			endClock = time()
			i+=1
			#print('i = ', i)

		return self.getBestRootChild().state.boardGame #.showBoard()