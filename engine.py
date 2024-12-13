from typing import Set, Iterator, Any

from tcod.console import Console
from tcod.context import Context

from actions import MovementAction, EscapeAction
from entity import Entity
from input_handlers import EventHandler


class Engine:

    def __init__(self, entities: Set[Entity], event_handler: EventHandler, player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.player = player

    def handle_events(self, events: Iterator[Any]):
        """事件处理"""


        for event in events:

            action = self.event_handler.dispatch(event)

            if action is None:
                continue

            if isinstance(action, MovementAction):
                self.player.move(action.dx, action.dy)

            elif isinstance(action, EscapeAction):
                raise SystemExit()

    def render(self, console: Console, context: Context) -> None:
        """渲染 实体"""
        console.clear()

        for entity in self.entities:
            console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
