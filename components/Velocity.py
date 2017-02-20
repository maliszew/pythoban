"""Velocity component."""


class Velocity:
    """Keeps velocity of an entity.
    in this moment, all entities that can move have the same, but that may change in the future."""

    def __init__(self, velocity_x, velocity_y):
        self.x = velocity_x
        self.y = velocity_y
