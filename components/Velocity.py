"""Velocity component."""


class Velocity:
    """Keeps velocity of an entity.
    in this moment, all entities that can move have the same, but that may change in the future."""

    def __init__(self, velocity):
        self.velocity = velocity
