About
=====

This package implements the game called Nim. The game can be played
interactively in the CLI or in a web browser. You can install this package and
play the game. Easy::

> pip install nimgame
> nimgame

You can also try the game before installing the package, see the "TryIt" link
on the left (when it will work :-))

Those, who are more of the developer types, can use the API, after installing
the package. The game can then be embedded in other applications and played
from any other kind of a GUI.

For mathematicians/statisticians, it can also be used for creating statistics
by running multiple games. If you know `combinatorial game theory`_ terms like
`sequential game`_, `perfect information`_, `impartial game`_,
`Sprague–Grundy theorem`_ and such, this API can be useful for you.


Game Rules
===========

For the general description of the Nim and similar games, see the
`Wikipedia page`_.

This game is played by 2 palyers (the computer can be a player).
There are coins arranged in heaps. Some descriptions call the grouped objects
stones, shells, matches, and the grouping may also be called piles.
There may be any number of heaps and any number of coins in a heap.

Players take turns. In each turn, a player takes coins from a heap (only 1
heap). It must be at least 1 coin. There is no upper limit (but the heap size).

There are 2 types of the game:

- the "normal" game is where the player, who takes the last coin, wins
- the "misère_" game is where the player, who has to take the last coin, loses


Usage
======

After instantiating the Nim class, you need to get the heaps set up. The
starting heaps then can be analysed and the starting player set. If it is the
Computer, it automatically does the 1\ :sup:`st` move. Then the Player is to do
the next move, then the Computer moves, and so on. When no more coins left, the
game ends.

.. code:: python

    import nimgame
    nim = nimgame.Nim(error_rate=10)  # Make the Computer do 10% errors
    nim.setup_heaps()  # Create heaps randomly
    nim.set_start(myturn=True)  # Indicate that the Player wants to start
    nim.do_move(nim.Move('b', 4))  # From heap 'B', remove 4 coins
    ...
    if nim.game_end():
        exit(0)


.. _Wikipedia page: https://en.wikipedia.org/wiki/Nim
.. _misère: https://en.wikipedia.org/wiki/Mis%C3%A8re#Mis%C3%A8re_game
.. _combinatorial game theory: https://en.wikipedia.org/wiki/Combinatorial_game_theory
.. _sequential game: https://en.wikipedia.org/wiki/Sequential_game
.. _perfect information: https://en.wikipedia.org/wiki/Perfect_information
.. _impartial game: https://en.wikipedia.org/wiki/Impartial_game
.. _Sprague–Grundy theorem: https://en.wikipedia.org/wiki/Sprague%E2%80%93Grundy_theorem
