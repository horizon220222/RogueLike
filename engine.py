from typing import Set, Iterator, Any

from tcod.console import Console
from tcod.context import Context
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler
from tcod.map import compute_fov


class Engine:

    def __init__(self, event_handler: EventHandler,  game_map: GameMap, player: Entity):
        self.event_handler = event_handler

        self.game_map = game_map
        self.player = player

        self.__update_fov__()

    def __update_fov__(self) -> None:
        # 实时
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8
        )
        # 累加
        self.game_map.explored |= self.game_map.visible

    def __handle_enemy_turns__(self) -> None:
        for entity in self.game_map.entities - {self.player}:
            print(f'The {entity.name} wonders when it will get to take a real turn.')


    def handle_events(self, events: Iterator[Any]):
        """事件处理"""

        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue
            action.perform(self, self.player)
            self.__handle_enemy_turns__()
            self.__update_fov__()

    def render(self, console: Console, context: Context) -> None:
        """渲染 实体"""
        self.game_map.render(console)

        context.present(console)

        console.clear()