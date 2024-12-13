from typing import Set, Iterator, Any

from tcod.console import Console
from tcod.context import Context
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


class Engine:

    def __init__(self, entities: Set[Entity], event_handler: EventHandler,  game_map: GameMap, player: Entity):
        self.event_handler = event_handler

        self.game_map = game_map

        self.entities = entities
        self.player = player

    def handle_events(self, events: Iterator[Any]):
        """事件处理"""

        for event in events:
            action = self.event_handler.dispatch(event)
            if action is None:
                continue
            action.perform(self, self.player)

    def render(self, console: Console, context: Context) -> None:
        """渲染 实体"""
        self.game_map.render(console)

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)

        console.clear()