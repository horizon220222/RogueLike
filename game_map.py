import numpy as np
from tcod.console import Console
import tile_types
from typing import Iterable, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entity import Entity


class GameMap:

    def __init__(self, width: int, height: int, entities: Iterable["Entity"] = ()):
        self.width = width
        self.height = height

        self.entities = set(entities)

        self.visible = np.full((width, height), fill_value=False, order="F")
        self.explored = np.full((width, height), fill_value=False, order="F")

        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")


    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional["Entity"]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def in_bounds(self, x:int,y:int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.rgb[0: self.width, 0: self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            # Only print entities that are in the FOV
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)
