"""Type definitions

Users can use the following type definitions for creating and checking
arguments:

- Move: define how many coins are to be removed and from what heap
- ErrorRate: define the required error for both parties (when the program is to
  calculate the moves for both of them)
- HeapCoinRange: define heap or coin count ranges for automatic heap setup
"""


import collections
from typing import Union, List, Tuple


# A move vector, i.e. what heap is to be reduced and by how many coins
Move = collections.namedtuple('Move', 'heapdesig removecount')

# The error rate percentages can be defined for parties separately
ErrorRate = collections.namedtuple('ErrorRate', 'Computer Player')
ErrorRate_T = Union[int, ErrorRate]
ErrorRateTypes = (
    int, 
    ErrorRate
)

# How the user can indicate its requirement of the starting party
MyTurn_T = Union[str, bool]

# The accepted range of heap and coin numbers
HeapCoinRange = collections.namedtuple('HeapCoinRange', 'min max')
HeapCoinRange_T = Union[
    List[int],
    Tuple[int, int],
    HeapCoinRange
]
HeapCoinRangeTypes = (
    list, 
    tuple, 
    HeapCoinRange
)
