import os
import sys
import unittest

# make src importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from anvil_calculator import Item, Enchantments, ItemMatcher, EnchantmentsMatcher, IntMatcher
from settings import ItemNamespace, EnchantmentNamespaceId


class TestItemMatcher(unittest.TestCase):
    def test_match_namespace(self):
        matcher = ItemMatcher(namespace=ItemNamespace.IRON_SWORD)
        item = Item(ItemNamespace.IRON_SWORD)
        self.assertTrue(matcher.match(item))

    def test_match_repair_cost(self):
        matcher = ItemMatcher(repair_cost=IntMatcher([1, 2, 3]))
        item = Item(ItemNamespace.IRON_SWORD, repair_cost=2)
        self.assertTrue(matcher.match(item))

    def test_match_durability(self):
        matcher = ItemMatcher(durability=IntMatcher([100, 200, 300]))
        item = Item(ItemNamespace.IRON_SWORD, durability=200)
        self.assertTrue(matcher.match(item))

    def test_match_enchantments(self):
        matcher = ItemMatcher(enchantments={EnchantmentNamespaceId.SHARPNESS: IntMatcher([1, 2])})
        item = Item(ItemNamespace.IRON_SWORD, enchantments={EnchantmentNamespaceId.SHARPNESS: 2})
        self.assertTrue(matcher.match(item))

    def test_match_all_conditions(self):
        matcher = ItemMatcher(
            namespace=ItemNamespace.IRON_SWORD,
            repair_cost=IntMatcher([1, 2, 3]),
            durability=IntMatcher([100, 200, 300]),
            enchantments={EnchantmentNamespaceId.SHARPNESS: IntMatcher([1, 2])}
        )
        item = Item(ItemNamespace.IRON_SWORD, repair_cost=2, durability=200, enchantments={EnchantmentNamespaceId.SHARPNESS: 2})
        self.assertTrue(matcher.match(item))

    def test_match_fail(self):
        matcher = ItemMatcher(namespace=ItemNamespace.IRON_SWORD)
        item = Item(ItemNamespace.IRON_HELMET)
        self.assertFalse(matcher.match(item))


class TestEnchantmentsMatcher(unittest.TestCase):
    def test_match_enchantments(self):
        matcher = EnchantmentsMatcher({EnchantmentNamespaceId.SHARPNESS: IntMatcher([1, 2])})
        enchantments = Enchantments({EnchantmentNamespaceId.SHARPNESS: 2})
        self.assertTrue(matcher.match(enchantments))

    def test_match_fail(self):
        matcher = EnchantmentsMatcher({EnchantmentNamespaceId.SHARPNESS: IntMatcher([1, 2])})
        enchantments = Enchantments({EnchantmentNamespaceId.SHARPNESS: 3})
        self.assertFalse(matcher.match(enchantments))


class TestIntMatcher(unittest.TestCase):
    def test_match_no_conditions(self):
        matcher = IntMatcher(None)
        self.assertTrue(matcher.match(1))
        self.assertTrue(matcher.match(100))

    def test_match_single_value(self):
        matcher = IntMatcher(5)
        self.assertTrue(matcher.match(5))
        self.assertFalse(matcher.match(4))

    def test_match_list(self):
        matcher = IntMatcher([1, 2, 3])
        self.assertTrue(matcher.match(2))
        self.assertFalse(matcher.match(4))

    def test_match_empty_list(self):
        matcher = IntMatcher([])
        self.assertFalse(matcher.match(1))

    def test_match_str(self):
        matcher = IntMatcher(">5 <10 !=7")
        self.assertTrue(matcher.match(6))
        self.assertFalse(matcher.match(4))
        self.assertFalse(matcher.match(10))


if __name__ == '__main__':
    unittest.main()