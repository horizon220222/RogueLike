import tcod

from actions import MovementAction, EscapeAction
from engine import Engine
from entity import Entity
from game_map import GameMap
from input_handlers import EventHandler


def main():
    # 初始变量
    event_handler = EventHandler()

    screen_width = 80
    screen_height = 50
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 255, 255))
    npc = Entity(int(screen_width / 2 -5), int(screen_height / 2), "@", (255, 255, 0))
    entities = {npc, player}

    map_width = 80
    map_height = 45
    game_map = GameMap(map_width, map_height)

    # 初始engine
    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    # 绘制屏幕
    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )
    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Yet Another Roguelike Tutorial",
            vsync=True
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            engine.handle_events(tcod.event.wait())


if __name__ == '__main__':
    main()