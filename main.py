import traceback
import tcod
import setup_game
import color
import exceptions
import input_handlers


def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""

    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
    print("Game saved.")


def main():
    # 初始变量
    screen_width = 80
    screen_height = 50

    # 这个就是全局handler
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

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
        root_console = tcod.console.Console(screen_width, screen_height, order="F") # 固定
        try:
            while True:
                root_console.clear() # 固定
                handler.on_render(console=root_console)  # 用户渲染
                context.present(root_console) # 固定

                try:
                    for event in tcod.event.wait(): # 固定
                        context.convert_event(event) # 固定
                        # 这个就是更换handler
                        handler = handler.handle_events(event) # 用户输入
                except Exception:
                    traceback.print_exc()
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(traceback.format_exc(), color.error)
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:
            save_game(handler, "savegame.sav")
        except BaseException:
            save_game(handler, "savegame.sav")




if __name__ == '__main__':
    main()