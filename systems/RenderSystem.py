"""Render System.
uses Render and Position components to display entities on the sreen."""
import esper

from components import Render, Position


class RenderSystem(esper.Processor):
    def __init__(self):
        super().__init__()

    def process(self):
        pass
