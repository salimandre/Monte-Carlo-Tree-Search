# Monte Carlo Tree Search

We implemented a Monte Carlo Tree Search (MCTS) from scratch and we successfully applied it to Tic-Tac-Toe game. 

We performed tests using different allocated time to build MCTS (thinking time). We also could test several symmetrical and asymmetrical reward designs.

Summary of steps of MCTS model:

* At each turn do:
  * during a time T, repeat the following steps:
    * create a Tree (root) where each node is associated to a state of game
    * select a leaf by UCB exploration
    * create a child node from this leaf
    * evaluate new state by roll out simulations
    * backpropagate from leaf to the root by updating visit count and reward at each node of the path

In our MCTS we used the following features:
* we used the following UCB for trees (UCT) formula with c = 1.4 :
<p align="center"> 
<img src="img/ucb.png" width="25%">
</p>

* roll out simulations we performed by using random uniform policy

# Results

Here is a demo with 2 players using MCTS playing against each other. Allocated thinking time is 0.1s. Reward designs are symmetrical with reward(win)=3 and reward(draw)=1.

<p align="center"> 
<img src="img/demo_0-1s-3-1.gif" width="25%">
</p>

Here is a demo with 2 players using MCTS playing against each other. Allocated thinking time is 0.3s. Reward designs are symmetrical with reward(win)=3 and reward(draw)=1.

<p align="center"> 
<img src="img/demo_0-3s-3-1.gif" width="25%">
</p>

In the next figure we show the distribution of outcomes after we performed 100 games where we vary the allocated thinking time from 0.01s to 0.2s. Reward designs are symmetrical with reward(win)=3 and reward(draw)=1. Player 1 is the player to play first while player 2 is the player to play second.

<p align="center"> 
<img src="img/img_baseline.png" width="60%">
</p>

In the next figure we show the distribution of outcomes after we performed 100 games where we vary the allocated thinking time from 0.01s to 0.2s. Reward designs are asymmetrical with reward(win)=3 and reward(draw)=1 for player 1 (player to play first) and reward(win)=1 and reward(draw)=1 for player 2 (player to play second).

<p align="center"> 
<img src="img/img_asym.png" width="60%">
</p>

In the next figure we show the distribution of outcomes after we performed 100 games where we vary the allocated thinking time from 0.01s to 0.2s. Reward designs are *symmetrical* with reward(win)=1 and reward(draw)=0. Player 1 is the player to play first while player 2 is the player to play second.

<p align="center"> 
<img src="img/img_no_draw_.png" width="60%">
</p>


In the next figure we show the distribution of outcomes after we performed 100 games where we vary the allocated thinking time from 0.01s to 0.2s. Reward designs are asymmetrical with reward(win)=1 and reward(draw)=0 for player 1 (player to play first) and reward(win)=1 and reward(draw)=0 for player 2 (player to play second).

<p align="center"> 
<img src="img/img_asym_att_def.png" width="60%">
</p>

# Conclusion

From the previous plots we can make two observations: 
- First, the reward design reward(win)=3 and reward(1)=1 is to be the best reward of the three for the second player. Basically it says that in order to defend better you need also to attack and look for victory.

- Second, the best reward strategy for the first player is to focus on victory. If thinking time is low < 0.1s then the best reward design is reward(win)=1 and reward(draw)=0 meaning that aggressive but risky strategies are effective while little time to think. This is in fact what we observ in speed chess. Also we actually could observ that with reward design focusing on victory only MCTS converge faster towards picking the center first. When thinking time is higher > 0.1s then  
