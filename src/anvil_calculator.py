from typing import Self, Tuple, List, Dict, Union
from dataclasses import dataclass
from settings import EnchantmentNamespaceId, ItemNamespace, ENCHANTMENTS, ITEM_DURABILITY_TABLE
from int_to_roman import int_to_roman


class CraftingException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


@dataclass
class Enchantments(dict):

    def __init__(self, enchantments: Union[Dict[EnchantmentNamespaceId, int], None] = None) -> None:
        if enchantments is None:
            super().__init__()
        else:
            super().__init__(enchantments)

    def __str__(self) -> str:
        return '\n'.join(f"{enchantment_id} {int_to_roman(enchantment_lvl)}" for enchantment_id, enchantment_lvl in self.items())
    
    def is_mutually_exclusive_with(self, enchantment: EnchantmentNamespaceId) -> bool:
        return any(enchantment in ENCHANTMENTS[enchantment_id].get("exclusive_set", []) for enchantment_id in self.keys())


@dataclass
class Item:
    def __init__(self, 
                 namespace: ItemNamespace, 
                 repair_cost: int = 0, 
                 durability: Union[int, None] = None, 
                 enchantments: Union[Enchantments, Dict[EnchantmentNamespaceId, int], None] = None) -> None:
        self._namespace: ItemNamespace = namespace

        self._repair_cost: int = repair_cost

        if self._namespace == ItemNamespace.ENCHANTED_BOOK:
            self._durability = None
        elif durability is None:
            self._durability = ITEM_DURABILITY_TABLE.get(self._namespace)
        else:
            self._durability = durability

        if enchantments is None:
            self._enchantments: Enchantments = Enchantments()
        else:
            self._enchantments: Enchantments = enchantments if isinstance(enchantments, Enchantments) else Enchantments(enchantments)

        self._the_highest_durability: Union[int, None] = ITEM_DURABILITY_TABLE[self._namespace] if self._durability is not None else None

    def __str__(self) -> str:
        return f"{self._namespace}\n{self._enchantments.__str__().replace('\n', '\n\t')}\nrepair_cost: {self._repair_cost}\ndurability: {self._durability}"


    @property
    def namespace(self):
        return self._namespace

    @property
    def repair_cost(self):
        return self._repair_cost

    @property
    def durability(self):
        return self._durability

    @property
    def enchantments(self):
        return self._enchantments

    @property
    def the_highest_durability(self):
        return self._the_highest_durability


    def does_enchantment_support(self, enchantment : EnchantmentNamespaceId) -> bool:
        return self.namespace == ItemNamespace.ENCHANTED_BOOK or self._namespace in ENCHANTMENTS[enchantment]["supported_items"]

    def craft_with(self, sacrificial_item: 'Item') -> Tuple[Self, Union[int, None]]:
        is_same_item = self._namespace == sacrificial_item._namespace
        is_enchanted_book = sacrificial_item.namespace == ItemNamespace.ENCHANTED_BOOK

        if not is_same_item and not is_enchanted_book:
            raise CraftingException(f"Can't craft with {sacrificial_item}")
        
        cost_lvl = 0

        cost_lvl += self._repair_cost + sacrificial_item._repair_cost
        repair_cost = (max(self._repair_cost, sacrificial_item._repair_cost) + 1) * 2 - 1

        durability = self._durability
        if is_same_item and self._durability is not None and sacrificial_item._durability is not None and self._the_highest_durability is not None:
            if self._durability < self._the_highest_durability:
                cost_lvl += 2
                durability = min(int(self._durability + sacrificial_item._durability + 0.12 * self._the_highest_durability), self._the_highest_durability)

        enchantments = self._enchantments.copy()
        for enchantment_id, enchantment_lvl in sacrificial_item._enchantments.items():
            if not self.does_enchantment_support(enchantment_id):
                continue
            if self._enchantments.is_mutually_exclusive_with(enchantment_id):
                cost_lvl += 1
                continue
            lvl = self._enchantments.get(enchantment_id, 0)
            if lvl == enchantment_lvl:
                enchantments[enchantment_id] = lvl + 1 if lvl < ENCHANTMENTS[enchantment_id]["max_level"] else lvl
            else:
                enchantments[enchantment_id] = max(lvl, enchantment_lvl)
                
            anvil_cost = ENCHANTMENTS[enchantment_id]["anvil_cost"]
            if is_enchanted_book:
                anvil_cost = anvil_cost // 2 or 1

            cost_lvl += anvil_cost * enchantments[enchantment_id]
        
        return self.__class__(self._namespace, repair_cost, durability, enchantments), cost_lvl if 0 < cost_lvl < 40 else None


class EnchantmentsMatcher(dict):
    def __init__(self, enchantments: Union[Dict[EnchantmentNamespaceId, List[int]], Enchantments]) -> None:
        super().__init__(enchantments)

    def match(self, enchantments: Enchantments) -> bool:
        if not self:
            return True
        def gen():
            for enchantment_id, enchantment_lvls in self.items():
                if enchantment_id not in enchantments.keys() or enchantments[enchantment_id] not in enchantment_lvls:
                    yield False
        return all(gen())
    
    @classmethod
    def create_by_enchantments(cls, enchantments: Enchantments) -> Self:
        return cls({enchantment_id: [enchantment_lvl] for enchantment_id, enchantment_lvl in enchantments.items()})


class ItemMatcher:
    def __init__(self, 
                 namespace: Union[ItemNamespace, None] = None,
                 repair_cost: Union[List[int], int, None] = None,
                 durability: Union[List[int], int, None] = None,
                 enchantments: Union[EnchantmentsMatcher, Dict[EnchantmentNamespaceId, List[int]], Enchantments, None] = None) -> None:
        if namespace is None:
            self._namespace = None
        elif isinstance(namespace, str):
            self._namespace = [namespace]

        if repair_cost is None:
            self._repair_cost = None
        elif isinstance(repair_cost, int):
            self._repair_cost = [repair_cost]
        elif isinstance(repair_cost, list):
            self._repair_cost = repair_cost

        if durability is None:
            self._durability = None
        elif isinstance(durability, int):
            self._durability = [durability]
        elif isinstance(durability, list):
            self._durability = durability

        if enchantments is None:
            self._enchantments = None
        elif isinstance(enchantments, dict) or isinstance(enchantments, Enchantments):
            self._enchantments = EnchantmentsMatcher(enchantments)
        elif isinstance(enchantments, EnchantmentsMatcher):
            self._enchantments = enchantments
    
    
    def match(self, item: Item) -> bool:
        if self._namespace is not None and item.namespace not in self._namespace:
            return False
        if self._repair_cost is not None and item.repair_cost not in self._repair_cost:
            return False
        if self._durability is not None and item.durability not in self._durability:
            return False
        if self._enchantments is not None and not self._enchantments.match(item.enchantments):
            return False
        return True
    

    @classmethod
    def create_by_item(cls, item: Item) -> Self:
        enchantments = EnchantmentsMatcher(item.enchantments)
        return cls(item.namespace, item.repair_cost, item.durability, enchantments)
            

@dataclass
class Step:
    def __init__(self, main_item: Item, sacrificial_item: Item, cost_lvl: int) -> None:
        self.main_item = main_item
        self.sacrificial_item = sacrificial_item
        self.cost_lvl = cost_lvl


class AnvilCalculator:
    def __init__(self, items: List[Item], excepted_item: ItemMatcher) -> None:
        self.items = items
        self.excepted_item = excepted_item
        self.__result = None

    def __dfs_find_steps(self, items: Union[List[Item], None] = None, steps: List[Step] = None, cost_lvl: int = 0) -> None:
        if items is None:
            items = self.items
        if steps is None:
            steps = []

        if any(self.excepted_item.match(item) for item in items):
            self.__result.append((steps, cost_lvl))
            return
        elif len(items) <= 1:
            return
        
        for main_item in items:
            for sacrificial_item in items:
                if main_item is sacrificial_item:
                    continue
                try:
                    item, lvl = main_item.craft_with(sacrificial_item)
                    if lvl is not None:
                        new_items = [item] + [i for i in items if i is not main_item and i is not sacrificial_item]
                        new_steps = steps + [Step(main_item, sacrificial_item, lvl)]
                        self.__dfs_find_steps(new_items, new_steps, cost_lvl + lvl)
                except CraftingException:
                    continue

    def calculate(self) -> Union[List[Tuple[List[Step], int]], None]:
        self.__result: List[tuple[List[Step], int]] = []
        self.__dfs_find_steps()
        if not self.__result:
            return None
        else:
            min_cost_lvl = min(cost_lvl for _, cost_lvl in self.__result)
            self.__result = [(steps, cost_lvl) for steps, cost_lvl in self.__result if cost_lvl == min_cost_lvl]
            return self.__result

