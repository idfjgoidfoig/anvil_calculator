import os
import sys
import unittest

# make src importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from anvil_calculator import Item, Enchantments, CraftingException, ItemMatcher, EnchantmentsMatcher, AnvilCalculator
from settings import ItemNamespace, EnchantmentNamespaceId, ITEM_DURABILITY_TABLE


class TestItemInitialization(unittest.TestCase):
    def test_enchanted_book_has_no_durability(self):
        book = Item(ItemNamespace.ENCHANTED_BOOK)
        self.assertIsNone(book.durability)

    def test_other_item_has_correct_durability(self):
        item = Item(ItemNamespace.LEATHER_HELMET)
        expected = ITEM_DURABILITY_TABLE.get(ItemNamespace.LEATHER_HELMET)
        self.assertEqual(item.durability, expected)


class TestEnchantmentsStr(unittest.TestCase):
    def test_str_contains_enum_and_roman(self):
        ench = Enchantments({EnchantmentNamespaceId.SHARPNESS: 3})
        s = str(ench)
        # expect the enum name and roman numeral for 3
        self.assertIn('sharpness', s)
        self.assertIn('III', s)


class TestItemStr(unittest.TestCase):
    def test_str_contains_namespace_and_enchantments(self):
        item = Item(ItemNamespace.IRON_SWORD, repair_cost=5, enchantments={EnchantmentNamespaceId.SHARPNESS: 2})
        s = str(item)
        self.assertIn('iron_sword', s)
        self.assertIn('sharpness', s)
        self.assertIn('II', s)
        self.assertIn('repair_cost: 5', s)


class TestItemCrafting(unittest.TestCase):
    def test_crafting_same_item(self):
        item1 = Item(ItemNamespace.IRON_SWORD, repair_cost=1)
        item2 = Item(ItemNamespace.IRON_SWORD, repair_cost=3, enchantments={EnchantmentNamespaceId.SHARPNESS: 2})
        result, cost = item1.craft_with(item2)
        self.assertEqual((result, cost), (Item(ItemNamespace.IRON_SWORD, repair_cost=7, enchantments={EnchantmentNamespaceId.SHARPNESS: 2}), 6))

    def test_crafting_with_enchanted_book(self):
        sword = Item(ItemNamespace.IRON_SWORD, repair_cost=1)
        book = Item(ItemNamespace.ENCHANTED_BOOK, repair_cost=7, enchantments={EnchantmentNamespaceId.SHARPNESS: 1})
        result, cost = sword.craft_with(book)
        self.assertEqual((result, cost), (Item(ItemNamespace.IRON_SWORD, repair_cost=15, enchantments={EnchantmentNamespaceId.SHARPNESS: 1}), 9))

    def test_crafting_different_items_fails(self):
            sword = Item(ItemNamespace.IRON_SWORD)
            helmet = Item(ItemNamespace.IRON_HELMET)
            with self.assertRaises(CraftingException):
                sword.craft_with(helmet)

    def test_too_expensive(self):
        item1 = Item(ItemNamespace.IRON_SWORD, repair_cost=31)
        item2 = Item(ItemNamespace.IRON_SWORD, repair_cost=31)
        _, cost = item1.craft_with(item2)
        self.assertIsNone(cost)
        
        
class TestAnvilCalculator(unittest.TestCase):
    def test_calculator(self):
        items = [
            Item(ItemNamespace.ENCHANTED_BOOK, 1, None, {EnchantmentNamespaceId.EFFICIENCY: 3}),
            Item(ItemNamespace.ENCHANTED_BOOK, 1, None, {EnchantmentNamespaceId.MENDING: 1}),
            Item(ItemNamespace.ENCHANTED_BOOK, 0, None, {EnchantmentNamespaceId.EFFICIENCY: 3}),
            Item(ItemNamespace.ENCHANTED_BOOK, 0, None, {EnchantmentNamespaceId.UNBREAKING: 3, EnchantmentNamespaceId.FORTUNE: 2}),
            Item(ItemNamespace.NETHERITE_PICKAXE, 0, 2031, {})
        ]

        except_item = ItemMatcher(ItemNamespace.NETHERITE_PICKAXE, None, 2031, EnchantmentsMatcher.create_by_enchantments(
            Enchantments({
                EnchantmentNamespaceId.UNBREAKING: 3,
                EnchantmentNamespaceId.FORTUNE: 2,
                EnchantmentNamespaceId.EFFICIENCY: 4,
                EnchantmentNamespaceId.MENDING: 1
            })
        ))
        

        calculator = AnvilCalculator(items, except_item)
        result = calculator.calculate()

        self.assertIsNotNone(result)
        if result is not None:
            _, cost_lvl = result[0]
            self.assertEqual(cost_lvl, 26)


if __name__ == '__main__':
    unittest.main()
