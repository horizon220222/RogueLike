class Action:
    """动作"""

    pass


class EscapeAction(Action):
    """动作 退出"""

    pass


class MovementAction(Action):
    """动作 移动"""

    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy