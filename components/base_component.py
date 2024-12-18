from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from engine import Engine
    from game_map import GameMap
    from entity import Entity

class BaseComponent:
    parent: "Entity"

    @property
    def gamemap(self) -> "GameMap":
        return self.parent.gamemap

    @property
    def engine(self) -> "Engine":
        return self.gamemap.engine