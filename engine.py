from typing import TYPE_CHECKING
from tcod.console import Console
from tcod.context import Context
from entity import Actor
from game_map import GameMap
from tcod.map import compute_fov
from input_handlers import MainGameEventHandler
if TYPE_CHECKING:
   from game_map import GameMap


class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler = MainGameEventHandler(self)
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
            if entity.ai:
                entity.ai.perform()


    def render(self, console: Console, context: Context) -> None:
        """渲染 实体"""
        self.game_map.render(console)

        console.print(
            x = 1,
            y = 47,
            string=f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}",
        )

        context.present(console)

        console.clear()