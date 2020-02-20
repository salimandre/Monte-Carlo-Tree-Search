import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

from boardgame_toolbox import BoardGame, Tic_Tac_Toe_Board
from mcts_toolbox import Node, State, MonteCarloTreeSearch

if __name__ == '__main__':

	nGames=100
	thinkingTime = 1. #seconds
	rewardDesign_1={'win': 3, 'draw': 1}
	rewardDesign_2={'win': 3, 'draw': 1}
	rewardDesign = [None,rewardDesign_1,rewardDesign_2]
	allOutcomes=np.zeros(3)
	for i in tqdm(range(nGames)):
		newGame = Tic_Tac_Toe_Board()
		nextPlayerId = 1
		gameIsFinished = False
		MCTree = MonteCarloTreeSearch(newGame,nextPlayerId,rewardDesign[nextPlayerId]['win'],rewardDesign[nextPlayerId]['draw'])
		while not gameIsFinished:
			nextMove = MCTree.findNextMove(thinkingTime)
			#nextMove.showBoard()
			nextPlayerId = nextMove.nextPlayerID[nextPlayerId]
			gameIsFinished = nextMove.hasEnded() or nextMove.getWinner()!=0
			MCTree = MonteCarloTreeSearch(nextMove,nextPlayerId,rewardDesign[nextPlayerId]['win'],rewardDesign[nextPlayerId]['draw'])
		#nextMove.showBoard()
		finalOutcome = nextMove.getWinner()
		if finalOutcome==0:
			print("\nNo winner: draw!\n")
		else:
			print('\nPlayer {} won!\n'.format(finalOutcome))
		allOutcomes[finalOutcome]+=1
	plt.bar([0,1,2], allOutcomes,color=['gray', 'red', 'blue'])
	plt.xticks([0,1,2], ('draw', 'P1 won', 'P2 won'))
	#plt.title('outcomes for {} seconds of thinking over {} games'.format(thinkingTime,nGames))
	plt.show()
	# 2s = 1000 search
	# 1s = 500 search
	# 0.1s = 75 search
	# 0.05s = 35 search

