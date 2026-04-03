# anvil_calculator

一个用于计算 Minecraft 铁砧合成最优路径与经验等级消耗的练手 Python 小项目。

项目核心能力：

- 物品与附魔建模（支持耐久、累计惩罚、附魔等级）
- 单步铁砧合成与费用计算
- 通过 DFS 搜索满足目标条件的最小总消耗合成步骤

## 项目结构

```text
anvil_calculator/
├─ src/
│  ├─ anvil_calculator.py
│  ├─ int_to_roman.py
│  └─ settings.py
├─ test/
│  ├─ test_anvil_calculator.py
│  └─ test_int_to_roman.py
│  ├─ test_matcher.py
└─ settings.json
```

## 环境要求

- Python 3.11+（推荐）

本项目目前只依赖 Python 标准库，无需额外安装第三方包。

## 快速开始

在项目根目录执行：

```powershell
python -m unittest discover -s test -p "test_*.py"
```

## 使用示例

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
    print(f"最小总消耗: {total_cost}")
```

## 说明

- 配置来源于 `settings.json`， 默认为Java版规则。
- `src/settings.py` 会在导入时读取该文件，因此请从项目根目录运行脚本/测试，确保可以找到 `settings.json`。
- 在不对铁砧合成机制进行改变的前提下，通过修改配置 `settings.json`支持部分非原版附魔。
- 当单次合成代价不在有效范围（`1~39`）时，`craft_with` 会返回 `None` 作为本次合成代价。

## 后续可扩展方向

- 增加 CLI（命令行参数输入物品和目标附魔）
- 增加 Web UI 或桌面 GUI