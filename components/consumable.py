from typing import Optional

import actions
import color
from components.base_component import BaseComponent
from components.inventor import Inventory
from entity import Actor, Item
from exceptions import Impossible


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[actions.Action]:
        return actions.ItemAction(consumer, self.parent)

    def activate(self, action: actions.ItemAction) -> None:
        raise NotImplementedError()

    def consume(self) -> None:
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):

    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: actions.ItemAction) -> None:
        consumer = action.entity
        amount_recovered = consumer.fighter.heal(self.amount)
        if amount_recovered > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recovered} HP!",
                color.health_recovered
            )
            self.consume()
        else:
            raise Impossible(f"Your health is already full.")
