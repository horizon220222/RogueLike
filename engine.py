from typing import TYPE_CHECKING
from tcod.console import Console
from tcod.context import Context
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler
from tcod.map import compute_fov

if TYPE_CHECKING:
   from entity import Entity
   from game_map import GameMap

class Engine:
    game_map: GameMap

    def __init__(self, player: Entity):
        self.event_handler = EventHandler(self)
        self.player = player

    def __update_fov__(self) -> None:
        """更新视角"""

        # 实时
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        # 累加
        self.game_map.explored |= self.game_map.visible

    def __handle_enemy_turns__(self) -> None:
        """怪物回合"""

        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')


    def render(self, console: Console, context: Context) -> None:
        """渲染 实体"""
        self.game_map.render(console)

        context.present(console)

        console.clear()