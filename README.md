# anvil_calculator

A small practice-oriented Python project for calculating optimal Minecraft anvil combination paths and XP level costs.

Core capabilities:

- Item and enchantment modeling (supports durability, cumulative prior-work penalty, and enchantment levels)
- Single-step anvil combination and cost calculation
- DFS-based search for the minimum total cost sequence that satisfies a target condition

## Project Structure

```text
anvil_calculator/
├─ src/
│  ├─ anvil_calculator.py
│  ├─ int_to_roman.py
│  └─ settings.py
├─ test/
│  ├─ test_anvil_calculator.py
│  └─ test_int_to_roman.py
└─ settings.json
```

## Requirements

- Python 3.11+ (recommended)

The project currently relies only on the Python standard library, so no third-party packages are required.

## Quick Start

Run from the project root:

```powershell
python -m unittest discover -s test -p "test_*.py"
```

## Usage Example

```python
from anvil_calculator import Item, Enchantments, ItemMatcher, EnchantmentsMatcher, AnvilCalculator
from settings import ItemNamespace, EnchantmentNamespaceId

items = [
    Item(ItemNamespace.ENCHANTED_BOOK, 1, None, {EnchantmentNamespaceId.EFFICIENCY: 3}),
    Item(ItemNamespace.ENCHANTED_BOOK, 1, None, {EnchantmentNamespaceId.MENDING: 1}),
    Item(ItemNamespace.NETHERITE_PICKAXE, 0, 2031, {}),
]

target = ItemMatcher(
    ItemNamespace.NETHERITE_PICKAXE,
    None,
    2031,
    EnchantmentsMatcher.create_by_enchantments(
        Enchantments({
            EnchantmentNamespaceId.EFFICIENCY: 3,
            EnchantmentNamespaceId.MENDING: 1,
        })
    )
)

calculator = AnvilCalculator(items, target)
result = calculator.calculate()

if result:
    steps, total_cost = result[0]
    print(f"Minimum total cost: {total_cost}")
```

## Notes

- Configuration comes from `settings.json`, with Java Edition rules used by default.
- `src/settings.py` reads this file at import time, so run scripts/tests from the project root to ensure `settings.json` can be found.
- Without changing the anvil combination mechanics, you can support some non-vanilla enchantments by editing `settings.json`.
- If a single combination cost is outside the valid range (`1~39`), `craft_with` returns `None` for that combination cost.

## Possible Extensions

- Add a CLI (input items and target enchantments through command-line arguments)
- Add a Web UI or desktop GUI
