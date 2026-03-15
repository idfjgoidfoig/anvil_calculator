import json
from enum import StrEnum, auto


with open("settings.json", "r") as f:
    data = json.load(f)

class ItemNamespace(StrEnum):
    ENCHANTED_BOOK = auto()
    ...

for item in data["items"]:
    setattr(ItemNamespace, item.upper(), item)

ITEM_DURABILITY_TABLE = {item: item_data["durability"] for item, item_data in data["items"].items()}


class EnchantmentNamespaceId(StrEnum):
    ...

for enchantment in data["enchantments"]:
    name = enchantment["description"]["translate"]
    setattr(EnchantmentNamespaceId, name.upper(), name)

ENCHANTMENTS = {i["description"]["translate"]: i for i in data["enchantments"]}

