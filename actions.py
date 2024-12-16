from typing import TYPE_CHECKING, Tuple, Optional

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor


class Action:
    """动作"""

    def __init__(self, entity: "Actor") -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> "Engine":
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """
        执行此操作需要使用确定其范围的对象。

        self.engine 是执行此操作的范围。
        self.entity 是执行操作的对象。

        此方法必须由Action子类重写。
        """
        raise NotImplementedError()


class EscapeAction(Action):
    """动作 退出"""

    def perform(self) -> None:
        raise SystemExit()


class WaitAction(Action):
    """动作 等待"""

    def perform(self) -> None:
        pass


class ActionWithDirection(Action):
    """方向"""

    def __init__(self, entity: "Actor", dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) ->Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional["Entity"]:
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional["Actor"]:
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        pass


class MeleeAction(ActionWithDirection):

    def perform(self) -> None:
        target = self.target_actor
        if not target:
            return

        damage = self.entity.fighter.powser - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if damage > 0:
            print(f"{attack_desc} for {damage} hit points.")
            target.fighter.hp -= damage
        else:
            print(f"{attack_desc} but does no damage.")



class MovementAction(ActionWithDirection):
    """动作 移动"""

    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            return

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    """碰撞"""

    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
