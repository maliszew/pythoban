"""Sokoban map object."""
import numpy


class GameMap:

    def __init__(self, height, width, board):
        self.height = height
        self.width = width
        self.board = board
