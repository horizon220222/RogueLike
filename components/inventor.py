from typing import List

from components.base_component import BaseComponent
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from entity import Actor, Item


class Inventory(BaseComponent):
    parent: "Actor"

    def __init__(self, capacity: int):
        self.capacity = capacity # 最大物品数
        self.items: List[Item] = []

    def drop(self, item: "Item") -> None:
        self.items.remove(item)

        item.place(self.parent.x, self.parent.y, self.gamemap)
        self.engine.message_log.add_message(f"You dropped the {item.name}.")