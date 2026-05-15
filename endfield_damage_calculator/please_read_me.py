#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终末地伤害计算小工具 - 项目说明文档

项目简介：
    本工具是一个基于 CustomTkinter 开发的伤害计算辅助工具，用于游戏《明日方舟：终末地》。
    玩家可以通过选择角色和武器，查看属性面板和乘区数据，帮助优化配装和战斗策略。

功能特性：
    1. 角色选择：支持按类型、星级筛选角色
    2. 武器选择：支持按类型、星级筛选武器，包含特殊能力等级选择
    3. 属性展示：显示角色和武器的详细属性
    4. 乘区计算：实时计算能力乘区、能力值加成、攻击力等数据
"""

# ==================== 版本信息（只在此处修改） ====================
# 项目版本号（用于文档、内部标识）
_VERSION = "1.6.2"

# EXE 版本号（用于打包发布）
_EXE_VERSION = "0.1.0-beta"
# ==============================================================

# ==================== 项目结构文档（自动生成） ====================
PROJECT_STRUCTURE = f"""
项目结构：
    ├── main.py                    # 项目入口，启动应用
    ├── pyproject.toml             # 打包配置文件
    ├── please_read_me.py          # 项目说明文档
    ├── build.py                   # 打包脚本
    ├── gui_design/                # GUI 界面模块
    │   ├── gui.py                 # 主应用类，管理窗口和布局
    │   ├── gui_tools.py           # GUI 工具组件导出层
    │   ├── gui_settings.py        # GUI 设置初始化
    │   ├── selection_panel.py     # 选择面板类
    │   ├── selection_components.py # 选择面板组件
    │   └── property_display.py    # 属性展示函数
    ├── calculation/               # 计算逻辑模块
    │   ├── multiplicative_zone.py # 乘法区伤害计算
    │   └── multiplicative_zones/  # 乘区子模块
    │       ├── base_zone.py       # 乘区基类
    │       ├── attribute_zone.py  # 能力乘区
    │       ├── defense_zone.py     # 防御减伤区
    │       ├── ability_bonus_zone.py # 能力值加成区
    │       ├── final_attack_zone.py  # 最终攻击力区
    │       └── zone_manager.py    # 乘区管理器
    ├── data/                      # 统一数据加载层
    │   └── loader.py              # 角色和武器数据的统一加载与缓存
    ├── utils/                     # 工具函数模块
    │   └── path_utils.py          # 路径处理工具
    └── character_weapon_equipment/# 数据文件目录
        ├── character_data/        # 角色数据（JSON格式）
        └── weapon_data/           # 武器数据（JSON格式）
"""

USAGE_INFO = f"""
使用方法：
    1. 运行方式：
        python main.py

    2. 打包方式：
        pip install setuptools wheel pyinstaller
        python build.py

    3. 操作流程：
        - 在左侧选择角色类型和星级
        - 在左侧选择武器类型和星级
        - 调整等级和信赖等级（角色）
        - 调整特殊能力等级（武器）
        - 点击"确认选择"按钮查看属性和乘区数据

技术栈：
    - Python 3.10+
    - CustomTkinter 5.2.2+（GUI框架）
    - JSON（数据存储）
    - PyInstaller（打包工具）
"""

FORMULA_INFO = f"""
伤害计算公式：
    最终攻击力 = 中间攻击力 × (能力值加成 + 1)
    中间攻击力 = 攻击加成攻击力 + 附加攻击力+
    攻击加成攻击力 = 基础攻击力 × 攻击力+乘区
    能力值加成 = 主能力×0.005 + 副能力×0.002
"""

VERSION_INFO = f"""
版本信息：
    项目版本: v{_VERSION}
    EXE版本:  v{_EXE_VERSION}
"""


def get_version() -> str:
    """
    获取项目版本号

    返回：
        版本号字符串（如 "1.5.3"）
    """
    return _VERSION


def get_exe_version() -> str:
    """
    获取 EXE 版本号（用于打包发布）

    返回：
        EXE 版本号字符串（如 "1.0.0"）
    """
    return _EXE_VERSION


def get_full_intro() -> str:
    """获取完整的项目介绍文档"""
    return f"""
终末地伤害计算小工具 v{_VERSION}
{'=' * 50}
{PROJECT_STRUCTURE}
{USAGE_INFO}
{FORMULA_INFO}
{VERSION_INFO}
    """


def show_help() -> None:
    """
    显示项目帮助信息
    """
    print(f"""
============================================================
终末地伤害计算小工具 v{_VERSION}
============================================================
{PROJECT_STRUCTURE}
{USAGE_INFO}
{FORMULA_INFO}
{VERSION_INFO}
    """)

if __name__ == "__main__":
    show_help()


# ## 1. 高层摘要 (TL;DR)

# **影响范围：** 🟡 **中等** - 涉及核心计算公式改进、角色数据结构扩展和项目文档体系建立

# **关键变更：**
# - ✨ **公式计算精度提升**：属性成长曲线计算统一返回浮点数，并保留一位小数
# - 📊 **角色数据结构扩展**：为所有角色新增战技/连携技/终结技倍率的独立字段（倍率1/倍率2）
# - 🛡️ **空值处理优化**：修复技能倍率字段在空列表时返回 `[]` 的bug，改为返回 `None`
# - 📝 **项目文档体系建立**：新增 Agent 配置、领域文档、Issue 追踪和分类标签文档

# ---

# ## 2. 可视化概览 (代码与逻辑映射)

# ```mermaid
# graph TD
#     subgraph "formula.py - 公式计算层"
#         A1["calculate_growth_curve()"]
#         A2["calculate_skill_curve()"]
#         A1 --> A3["返回: List[float>"]
#         A2 --> A4["返回: List[float>"]
#         A3 --> A5["公式: round(base + floor(...), 1)"]
#     end
    
#     subgraph "character_data.py - 数据处理层"
#         B1["process_character_data()"]
#         B1 --> B2["战技倍率1"]
#         B1 --> B3["连携技倍率1/2"]
#         B1 --> B4["终结技倍率1/2"]
#         B2 --> B5["空值返回 None"]
#         B3 --> B5
#         B4 --> B5
#     end
    
#     subgraph "characters.json - 数据存储层"
#         C1["角色数据对象"]
#         C1 --> C2["新增字段: 战技倍率1"]
#         C1 --> C3["新增字段: 连携技倍率1/2"]
#         C1 --> C4["新增字段: 终结技倍率1/2"]
#     end
    
#     subgraph "add_character.py - 数据生成层"
#         D1["sys.path.insert()"]
#         D1 --> D2["添加项目根目录到搜索路径"]
#         D2 --> D3["导入 formula 模块"]
#     end
    
#     A5 -.-> B1
#     B1 -.-> C1
#     D3 -.-> A1
    
#     style A1 fill:#bbdefb,color:#0d47a1
#     style A2 fill:#bbdefb,color:#0d47a1
#     style B1 fill:#c8e6c9,color:#1a5e20
#     style C1 fill:#fff3e0,color:#e65100
#     style D1 fill:#f3e5f5,color:#7b1fa2
# ```

# ---

# ## 3. 详细变更分析

# ### 📐 3.1 公式计算模块 (`formula.py`)

# **变更内容：**
# - **返回类型统一化**：`calculate_growth_curve` 和 `calculate_skill_curve` 的返回类型从 `List[int | float]` 改为 `List[float]`
# - **精度控制优化**：公式从 `base + floor(...)` 改为 `round(base + math.floor(...), 1)`，确保所有属性值保留一位小数

# **代码对比：**

# | 项目 | 旧值 | 新值 |
# |------|------|------|
# | 返回类型 | `List[int \| float]` | `List[float]` |
# | 公式 | `base + floor((growth * (lv - 1) + offset) / divisor)` | `round(base + math.floor((growth * (lv - 1) + offset) / divisor), 1)` |

# **影响分析：**
# - 提升了计算精度的一致性
# - 简化了类型系统，避免混合类型带来的复杂性

# ---

# ### 🛡️ 3.2 角色数据处理 (`character_data.py`)

# **变更内容：**
# 修复了向后兼容性字段在空列表时的返回值问题。原代码在列表为空时返回 `[]`，现改为返回 `None`。

# **代码变更：**

# ```python
# # 旧代码
# processed["战技倍率1"] = processed["战技倍率"][0]
# processed["连携技倍率1"] = processed["连携技倍率"][0] if len(processed["连携技倍率"]) > 0 else []
# processed["连携技倍率2"] = processed["连携技倍率"][1] if len(processed["连携技倍率"]) > 1 else []
# processed["终结技倍率1"] = processed["终结技倍率"][0] if len(processed["终结技倍率"]) > 0 else []
# processed["终结技倍率2"] = processed["终结技倍率"][1] if len(processed["终结技倍率"]) > 1 else []

# # 新代码
# processed["战技倍率1"] = processed["战技倍率"][0] if len(processed["战技倍率"]) > 0 else None
# processed["连携技倍率1"] = processed["连携技倍率"][0] if len(processed["连携技倍率"]) > 0 else None
# processed["连携技倍率2"] = processed["连携技倍率"][1] if len(processed["连携技倍率"]) > 1 else None
# processed["终结技倍率1"] = processed["终结技倍率"][0] if len(processed["终结技倍率"]) > 0 else None
# processed["终结技倍率2"] = processed["终结技倍率"][1] if len(processed["终结技倍率"]) > 1 else None
# ```

# **影响分析：**
# - 修复了潜在的逻辑错误：空列表 `[]` 会被误判为有效数据
# - 统一了空值表示方式，使用 `None` 更符合 Python 惯例

# ---

# ### 📊 3.3 角色数据扩展 (`characters.json`)

# **变更内容：**
# 为多个角色新增了技能倍率的独立字段，包括：

# | 新增字段 | 说明 |
# |----------|------|
# | `战技倍率1` | 战技第一段倍率（12个等级） |
# | `连携技倍率1` | 连携技第一段倍率（12个等级） |
# | `连携技倍率2` | 连携技第二段倍率（12个等级，部分角色为 `null`） |
# | `终结技倍率1` | 终结技第一段倍率（12个等级） |
# | `终结技倍率2` | 终结技第二段倍率（12个等级，部分角色为 `null`） |

# **受影响角色示例：**

# | 角色名称 | 新增字段数量 | 特殊说明 |
# |----------|--------------|----------|
# | 安洁莉娅 | 5个字段 | 完整倍率数据 |
# | 珂洛蒂亚 | 5个字段 | 连携技倍率2为 `null` |
# | 珂洛蒂亚 | 5个字段 | 连携技倍率1/2为 `null` |
# | 珂洛蒂亚 | 5个字段 | 连携技倍率1/2为 `null` |
# | ... | ... | 共约15+角色 |

# **数据结构示例：**

# ```json
# {
#   "战技倍率1": [156, 171, 187, 202, 218, 234, 249, 265, 280, 300, 323, 350],
#   "连携技倍率1": [45, 49, 54, 58, 62, 67, 71, 76, 80, 86, 93, 100],
#   "连携技倍率2": [178, 196, 213, 231, 249, 267, 284, 302, 320, 342, 369, 400],
#   "终结技倍率1": [356, 391, 427, 462, 498, 533, 569, 604, 640, 684, 738, 800],
#   "终结技倍率2": [267, 294, 320, 347, 374, 400, 427, 454, 480, 514, 554, 600]
# }
# ```

# ---

# ### 🔧 3.4 角色添加脚本 (`add_character.py`)

# **变更内容：**
# - 添加了 `sys` 模块导入
# - 添加了项目根目录到模块搜索路径，确保可以正确导入 `calculation.formula` 模块

# **代码变更：**

# ```python
# import sys
# from pathlib import Path

# # 添加项目根目录到模块搜索路径
# sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# from calculation.formula import (
#     calculate_growth_curve,
#     calculate_skill_curve,
#     ...
# )
# ```

# **影响分析：**
# - 修复了模块导入路径问题，确保脚本可以独立运行

# ---

# ### 📝 3.5 项目文档体系 (新增文件)

# #### 3.5.1 `AGENTS.md` - Agent 配置总览
# - 定义了 Issue 追踪方式
# - 指定了分类标签文档位置
# - 配置了领域文档路径

# #### 3.5.2 `docs/agents/domain.md` - 领域文档规范
# - 规定了代码探索前应阅读的文档（`CONTEXT.md`、`docs/adr/`）
# - 定义了单上下文和多上下文仓库的文件结构
# - 要求使用术语表中的词汇
# - 规定了 ADR 冲突的处理方式

# #### 3.5.3 `docs/agents/issue-tracker.md` - Issue 追踪器配置
# - 指定使用 GitHub Issues 作为问题追踪系统
# - 定义了 `gh` CLI 的使用规范
# - 规定了创建、读取、列表、评论、标签、关闭等操作

# #### 3.5.4 `docs/agents/triage-labels.md` - 分类标签映射

# | Agent 标签 | 实际标签 | 含义 |
# |------------|----------|------|
# | `needs-triage` | `needs-triage` | 需要维护者评估 |
# | `needs-info` | `needs-info` | 等待报告者提供更多信息 |
# | `ready-for-agent` | `ready-for-agent` | 完全规范，AFK agent 可处理 |
# | `ready-for-human` | `ready-for-human` | 需要人工实现 |
# | `wontfix` | `wontfix` | 不会处理 |

# ---

# ## 4. 影响与风险评估

# ### ⚠️ 4.1 破坏性变更

# | 变更项 | 破坏性级别 | 说明 |
# |--------|------------|------|
# | `formula.py` 返回类型 | 🟡 中等 | 从 `List[int \| float]` 改为 `List[float>`，可能影响依赖整数返回值的代码 |
# | `character_data.py` 空值处理 | 🟢 低 | 从 `[]` 改为 `None`，更符合语义，但需检查是否有代码依赖空列表判断 |
# | `characters.json` 数据结构 | 🟢 低 | 新增字段，不影响现有字段读取 |

# ### 🧪 4.2 测试建议

# **公式计算测试：**
# - 验证 `calculate_growth_curve` 在不同参数下返回值均为浮点数
# - 验证返回值保留一位小数
# - 测试边界情况（`max_level=1`、`divisor=0` 等）

# **数据处理测试：**
# - 测试空列表场景下返回 `None` 而非 `[]`
# - 验证新增字段正确生成
# - 测试部分角色字段为 `null` 的情况

# **兼容性测试：**
# - 检查是否有代码依赖 `List[int | float]` 类型
# - 检查是否有代码使用 `if multiplier == []` 判断空值

# **文档验证：**
# - 确认 `gh` CLI 命令在项目环境中可用
# - 验证文档路径正确性

# ---

# ## 5. 总结

# 本次变更主要围绕三个核心目标：

# 1. **精度提升**：统一公式计算的返回类型和精度控制
# 2. **数据扩展**：为角色技能系统添加更细粒度的倍率数据
# 3. **规范化**：建立项目文档体系，明确开发协作流程

# 这些变更提升了代码的可维护性和数据的一致性，同时为后续的功能扩展奠定了基础。建议重点关注公式计算返回类型变更可能带来的兼容性问题。