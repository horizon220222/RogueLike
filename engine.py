from typing import TYPE_CHECKING
from tcod.console import Console

import exceptions
from entity import Actor
from game_map import GameMap
from tcod.map import compute_fov
from input_handlers import MainGameEventHandler
from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

if TYPE_CHECKING:
   from game_map import GameMap


class Engine:
    game_map: GameMap

    def __init__(self, player: Actor):
        self.event_handler = MainGameEventHandler(self)
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
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
            if hasattr(entity, "ai") and entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass


    def render(self, console: Console) -> None:
        """渲染 实体"""
        self.game_map.render(console)

        self.message_log.render(console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location( console=console, x=21, y=44, engine=self)
