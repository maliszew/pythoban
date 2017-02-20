"""Movement System.
uses Position and Velocity components to move entities."""
import esper

from components import Position, Velocity


class MovementSystem(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        pass