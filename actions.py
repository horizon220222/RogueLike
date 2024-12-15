from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    """动作"""

    def perform(self, engine: "Engine", entity: "Entity") -> None:
        """
        执行此操作需要使用确定其范围的对象。

        engine 是执行此操作的范围。
        entity 是执行操作的对象。

        此方法必须由Action子类重写。
        """
        raise NotImplementedError()



class EscapeAction(Action):
    """动作 退出"""

    def perform(self, engine: "Engine", entity: "Entity") -> None:
        raise SystemExit()


class ActionWithDirection(Action):
    """方向"""

    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, engine: "Engine", entity: "Entity") -> None:
        pass


class MeleeAction(ActionWithDirection):

    def perform(self, engine: "Engine", entity: "Entity") -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        target = engine.game_map.get_blocking_entity_at_location(dest_x, dest_y)
        if not target:
            return

        print(f"You kick the {target.name}, much to its annoyance!")


class MovementAction(ActionWithDirection):
    """动作 移动"""

    def perform(self, engine: "Engine", entity: "Entity") -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return
        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return

        entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """碰撞"""

    def perform(self, engine: "Engine", entity: "Entity") -> None:
        dest_x = entity.x + self.dx
        dest_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return MeleeAction(self.dx, self.dy).perform(engine, entity)
        else:
            return MovementAction(self.dx, self.dy).perform(engine, entity)
