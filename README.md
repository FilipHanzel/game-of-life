# Game of Life in python with pygame

*Tested with python 3.8.5*

Implementation of *Game of Life* algorithm in pure python, Numpy and CuPy with visualization in pygame. CuPy implementation is similar to numpy with minor adjustments for pygame visualization.

### Time comparison
Time of map update can be roughly compared using src/compare.py script (sample output below for map size 5000x5000)
```
Runnig vanilla python implementation...
Init time: 0.17900[s] Total loop time: 109.09504[s], 5 iterations, 21.81901[s] per iteration

Runnig np python implementation...
Init time: 0.00000[s] Total loop time: 9.26000[s], 50 iterations, 0.18520[s] per iteration

Runnig cp python implementation...
Init time: 0.26600[s] Total loop time: 0.16700[s], 50 iterations, 0.00334[s] per iteration
```
This does not take into account drawing the map. With CuPy to draw the map, conversion from CuPy array to Numpy array is needed (copy from the GPU) and that is a major bottleneck.
