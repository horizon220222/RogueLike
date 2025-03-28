import lzma
import pickle
from typing import TYPE_CHECKING
from tcod.console import Console
import exceptions
import render_functions
from game_map import GameMap, GameWorld
from tcod.map import compute_fov
from message_log import MessageLog
from entity import Actor

if TYPE_CHECKING:
   from game_map import GameMap



class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
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

        # 渲染实体和方块
        self.game_map.render(console)

        # 渲染日志
        self.message_log.render(console, x=21, y=45, width=40, height=5)

        # 渲染血条
        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        # 渲染
        render_functions.render_dungeon_level(console=console, dungeon_level=self.game_world.current_floor, location=(0, 47))


        # 渲染鼠标
        render_functions.render_names_at_mouse_location( console=console, x=21, y=44, engine=self)





    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""

        # 压缩和序列化对象
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
