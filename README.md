
# Parallel Implementation of Connect Four Minimax Algorithm

## Technical Approach
The goal of this project is to parallelize a Minimax artificial intelligence agent to play the game of Connect Four. Connect Four is a two-player game which consists of a vertical board of six rows by seven columns. Each player has twenty-one pieces of the same color and they take turns to drop a piece in one of the seven columns. The piece will drop down to the lowest unoccupied row. A player wins when they manage to get four consecutive pieces of the same color either horizontal, vertical or diagonally.  Although the game is deterministic, it would require four terabytes of memory to keep all possible legal board combinations. 
In order to build an artificial intelligence agent that can play against a human player, an algorithm called Minimax can be used. The basic function of the algorithm is to look ahead and choose the move that leads it to the best possible outcome. The Minimax algorithm will look ahead and choose the best move it can play. The more moves that it can look ahead, the better it will be at winning. However, this also increases the running time of the algorithm. 

 ![picture](img/figure1.png)

Figure 1. Beginning of search tree at depth of two

Since the time complexity of the search algorithm for the tree is exponential, for every additional move it explores it takes seven times longer. It is possible to parallelize the search algorithm in order to minimize its running time. Figure 1 shows the exponential behavior of the Minimax search algorithm.
The Minimax part of the name means that this is a backtracking algorithm that is used the find the best possible move. In this implementation the best possible move that can be found is limited by the certain depth of a tree data structure through which the algorithm will traverse through. The best move can either be the move that maximizes the computer’s score or the move that most affects (minimizes) the opponent’s score. The way the program gives a value to a certain move is by an evaluation function which depends on the probability of that move leading to a win. 

## Performance Metrics and Experimental Settings
Resources from Texas Advanced Computing Center (TACC) were used on the Chameleon cluster. The instance used had 2 CPUs, 48 threads, 128 GiB of RAM and of node type gpu_k80. A CentOS application was run on the resource.
To achieve parallelization of the code, the numba library available for Python was used.  More specifically we used “prange” instead of “range” in the loops that were parallelized. Numba implements the ability to run loops in parallel, like OpenMP parallel for-loops and Cython’s prange. The loops body is scheduled in separate threads, and they execute in a nopython numba context. 
To test the algorithm, the depth of the search tree was varied from 3 to 6. Since the time complexity is O(7depth), we should have a diverse range of problem sizes to measure performance of our algorithms.

## Infrastructure and Programming Models Used 
The library that was used to parallelize the code is numba with a focus on prange which automatically takes care of data privatization and reductions. This library will use as many CPUs as detected by the multiprocessing module and the option for scheduling and setting the amount of threads to be used has not yet been implemented. Even though this is the case, one can set the number of cores within the CentOS kernel which enabled the program to run properly.

## Experimental Results 
Performance results are summarized in Table 1. 

| Depth | Serial Time (s)| Parallel Time (s) | Speedup |
|---|---|---|---|
|3 | 0.407 | 0.271 | 1.499 |
|4 | 2.920 | 1.627 | 1.795 |
|5 | 19.180 | 9.799 | 1.957 |
|6 | 135.691 | 50.829 | 2.670 |

Table 1: Running times for serial and parallel Minimax algorithms at various depth levels.

We can see how the parallel running times are faster than the serial algorithm. The speedup also increased with bigger problem size. Figure 2 illustrates the performance of the algorithm.

 ![picture](img/figure2.png)
 
Figure 2: Parallel vs serial performance

The parallel version of this algorithm is faster compared to the original serial version. Not only is it faster in most cases, the parallel version is also very consistent since most of the turns the algorithm took using the parallelized code, take about the same amount of time depending on the depth it is searching through. This is great, but the results that were obtained may show an underlying issue with the algorithm. The times that calculated show that at a depth larger than 4, a significant increase of total time to complete a game is observed.

## Conclusions and Future Work
The Minimax algorithm for the game Connect Four works incredibly well serialized, but parallelization opens the door to further improvements. The parallel version was incredibly consistent and with further improvements such as adding Alpha-Beta pruning could take the turn times even further down which could enable the code to run even deeper for a better success rate. This is because if the algorithm can search at a higher depth in the turn tree, the more moves it can analyze and in short, the algorithm can make better decisions. 

Demo video: https://www.youtube.com/watch?v=-eMDyHR9QJ8

