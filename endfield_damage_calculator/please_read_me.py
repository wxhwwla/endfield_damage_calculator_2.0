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

项目结构：
    ├── main.py                    # 项目入口，启动应用
    ├── pyproject.toml             # 打包配置文件
    ├── please_read_me.py          # 项目说明文档（本文件）
    ├── gui_design/                # GUI 界面模块
    │   ├── gui.py                 # 主应用类，管理窗口和布局
    │   ├── gui_tools.py           # GUI 工具组件导出层
    │   ├── gui_settings.py        # GUI 设置初始化
    │   ├── selection_panel.py     # 选择面板类
    │   └── property_display.py    # 属性展示函数
    ├── calculation/               # 计算逻辑模块
    │   ├── multiplicative_zone.py # 乘法区伤害计算
    │   └── multiplicative_zones/  # 乘区子模块
    │       ├── base_zone.py       # 乘区基类
    │       ├── attribute_zone.py  # 能力乘区
    │       ├── defense_zone.py    # 防御减伤区
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

使用方法：
    1. 运行方式：
        python main.py
        
    2. 打包方式：
        pip install setuptools wheel pyinstaller
        pyinstaller --onefile --windowed main.py
        
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

伤害计算公式：
    最终攻击力 = 中间攻击力 × (能力值加成 + 1)
    中间攻击力 = 攻击加成攻击力 + 附加攻击力+
    攻击加成攻击力 = 基础攻击力 × 攻击力+乘区
    能力值加成 = 主能力×0.005 + 副能力×0.002

版本信息：
    v1.3.0 - 当前版本
"""


def get_version() -> str:
    """
    获取当前版本号
    
    返回：
        版本号字符串（如 "1.3.0"）
    """
    return "1.5.4"


def show_help() -> None:
    """
    显示项目帮助信息
    """
    print("=" * 60)
    print("终末地伤害计算小工具 v{}".format(get_version()))
    print("=" * 60)
    print("\n项目结构：")
    print("  main.py                 - 项目入口")
    print("  gui_design/             - GUI界面模块")
    print("  calculation/            - 计算逻辑模块")
    print("  data/                   - 数据加载层")
    print("  utils/                  - 工具函数")
    print("  character_weapon_equipment/ - 数据文件")
    print("\n使用方法：")
    print("  python main.py          - 启动应用")
    print("  python please_read_me.py - 显示此帮助")
    print("=" * 60)


if __name__ == "__main__":
    show_help()



# ## 1. 高层摘要（TL;DR）

# *   **影响范围：** 🟡 **中等** - 添加了 PyInstaller 打包功能，更新版本号，新增 IDE 配置文件
# *   **核心变更：**
#     *   ✨ 新增 `build.py` 打包脚本，支持一键生成 Windows 可执行文件
#     *   🔧 新增 PyInstaller 配置文件 `终末地伤害计算器.spec`
#     *   📦 版本号从 **1.5.2** 更新到 **1.5.3**
#     *   🛠️ 添加 PyCharm IDE 项目配置文件
#     *   🚫 新增 `.gitignore` 规则，排除敏感文件

# ---

# ## 2. 可视化概览（代码与逻辑映射）

# ```mermaid
# graph TD
#     subgraph "开发环境配置"
#         A[".idea 配置文件<br/>IDE 项目设置"]
#         B[".gitignore<br/>Git 忽略规则"]
#     end
    
#     subgraph "打包流程"
#         C["build.py<br/>打包脚本"]
#         D["终末地伤害计算器.spec<br/>PyInstaller 配置"]
#         E["main.py<br/>主程序入口"]
#     end
    
#     subgraph "打包输出"
#         F["dist/终末地伤害计算器.exe<br/>可执行文件"]
#         G["build/终末地伤害计算器/<br/>构建产物"]
#     end
    
#     subgraph "数据文件"
#         H["characters.json<br/>角色数据"]
#         I["weapons.json<br/>武器数据"]
#     end
    
#     A --> C
#     B --> C
#     C --> D
#     D --> E
#     E --> F
#     E --> G
#     H --> D
#     I --> D
    
#     style A fill:#f3e5f5,color:#7b1fa2
#     style C fill:#bbdefb,color:#0d47a1
#     style D fill:#fff3e0,color:#e65100
#     style F fill:#c8e6c9,color:#1a5e20
# ```

# ---

# ## 3. 详细变更分析

# ### 📦 组件一：打包工具与配置

# #### **文件：`build.py` - 打包脚本（新增）**

# **变更说明：**
# 新增自动化打包脚本，使用 PyInstaller 将 Python 程序打包为 Windows 可执行文件。

# **核心功能：**

# | 函数名 | 功能描述 |
# |--------|----------|
# | `check_pyinstaller()` | 检查 PyInstaller 是否已安装，未安装则自动安装 |
# | `build_exe()` | 执行打包流程，生成单文件可执行程序 |

# **打包参数配置：**

# | 参数 | 值 | 说明 |
# |------|-----|------|
# | 模式 | `--onefile` | 单文件模式，所有依赖打包到一个 exe |
# | 窗口模式 | `--windowed` | 无控制台窗口，GUI 应用 |
# | 程序名称 | `终末地伤害计算器` | 生成的 exe 文件名 |
# | 数据文件 | `characters.json`, `weapons.json` | 打包时包含的 JSON 配置文件 |
# | 清理选项 | `--clean` | 清理临时文件 |

# **代码逻辑：**
# ```python
# # 打包命令示例
# sys.executable, "-m", "PyInstaller",
# "--onefile",              # 单文件模式
# "--windowed",             # 无控制台窗口
# "--name=终末地伤害计算器",
# "--add-data", "characters.json;character_weapon_equipment/character_data/",
# "--add-data", "weapons.json;character_weapon_equipment/weapon_data/",
# "--clean",
# str(project_root / "main.py")
# ```

# ---

# #### **文件：`终末地伤害计算器.spec` - PyInstaller 配置（新增）**

# **变更说明：**
# PyInstaller 的配置文件，定义打包的详细参数。

# **配置详情：**

# | 配置项 | 值 | 说明 |
# |--------|-----|------|
# | 入口文件 | `main.py` | 程序主入口 |
# | 数据文件 | `characters.json`, `weapons.json` | 需要打包的配置文件 |
# | 输出名称 | `终末地伤害计算器` | 可执行文件名 |
# | 控制台模式 | `False` | 无控制台窗口 |
# | UPX 压缩 | `True` | 使用 UPX 压缩可执行文件 |

# ---

# ### 🔧 组件二：项目配置文件

# #### **文件：`.gitignore` - Git 忽略规则（新增）**

# **新增忽略项：**

# | 文件/目录 | 原因 |
# |-----------|------|
# | `github_upload_module.py` | GitHub 上传脚本（本地工具） |
# | `git_key.txt` | Git 密钥文件（敏感信息） |

# ---

# #### **文件：`.idea/*` - PyCharm IDE 配置（新增）**

# **新增文件列表：**

# | 文件 | 用途 |
# |------|------|
# | `.idea/.gitignore` | IDEA 项目忽略规则（忽略 `shelf/`, `workspace.xml`） |
# | `.idea/endfield_damage_calculator.iml` | Python 模块配置（Python 3.13） |
# | `.idea/inspectionProfiles/profiles_settings.xml` | 代码检查配置 |
# | `.idea/misc.xml` | 项目元数据和 Black 格式化配置 |
# | `.idea/modules.xml` | 模块管理配置 |
# | `.idea/vcs.xml` | Git 版本控制映射 |

# **Python 版本配置：**
# ```xml
# <component name="Black">
#   <option name="sdkName" value="Python 3.13" />
# </component>
# <component name="ProjectRootManager" version="2" 
#   project-jdk-name="Python 3.13 (endfield_damage_calculator)" 
#   project-jdk-type="Python SDK" />
# ```

# ---

# ### 📝 组件三：版本更新

# #### **文件：`please_read_me.py` - 项目说明**

# **变更说明：**
# - 版本号从 `1.5.2` 更新到 `1.5.3`
# - 删除了文件末尾的大量注释内容（之前的版本历史记录），保持文件简洁

# **版本变更：**
# ```python
# # 旧版本
# return "1.5.2"

# # 新版本
# return "1.5.3"
# ```

# ---

# ### 🏗️ 组件四：打包产物（自动生成）

# #### **文件：`build/终末地伤害计算器/*` - PyInstaller 构建产物**

# **新增文件说明：**

# | 文件 | 说明 |
# |------|------|
# | `Analysis-00.toc` | 分析结果，包含所有依赖的 Python 模块列表 |
# | `EXE-00.toc` | 可执行文件打包信息 |
# | `PKG-00.toc` | 打包配置信息 |
# | `PYZ-00.toc` | Python 模块压缩包信息 |
# | `warn-终末地伤害计算器.txt` | PyInstaller 警告信息（缺失模块列表） |
# | `xref-终末地伤害计算器.html` | 模块依赖关系交叉引用 HTML 报告 |

# **重要数据文件打包：**
# ```python
# # 打包时包含的配置文件
# ('character_weapon_equipment\\character_data\\characters.json', 'DATA')
# ('character_weapon_equipment\\weapon_data\\weapons.json', 'DATA')
# ```

# **警告信息说明：**
# `warn-终末地伤害计算器.txt` 中列出了 PyInstaller 无法找到的模块，这些大多是：
# - Unix/Linux 特有模块（如 `pwd`, `grp`, `fcntl`）
# - 可选依赖（如 `typing_extensions`, `psutil`）
# - 条件导入的模块

# 这些警告不影响 Windows 平台的正常运行。

# ---

# ## 4. 影响与风险评估

# ### ⚠️ 破坏性变更

# | 变更类型 | 影响范围 | 迁移建议 |
# |----------|----------|----------|
# | 版本号更新 | 依赖版本号的脚本或配置 | 更新版本号引用为 `1.5.3` |
# | 新增打包脚本 | 无 | 可选使用，不影响现有功能 |

# ### 🧪 测试建议

# | 测试场景 | 验证要点 |
# |----------|----------|
# | **打包流程** | 运行 `python build.py` 能否成功生成 exe 文件 |
# | **可执行文件运行** | 双击 `终末地伤害计算器.exe` 能否正常启动 |
# | **数据文件加载** | 打包后的 exe 能否正确读取 `characters.json` 和 `weapons.json` |
# | **GUI 功能** | 打包后的程序所有 GUI 功能是否正常 |
# | **无控制台窗口** | 运行 exe 时不应出现控制台窗口 |

# ### ✅ 改进亮点

# 1. **一键打包：** 新增 `build.py` 脚本，简化打包流程
# 2. **自动化依赖检查：** 自动检测并安装 PyInstaller
# 3. **单文件输出：** 使用 `--onefile` 模式，生成独立的 exe 文件
# 4. **数据文件打包：** 自动包含必要的 JSON 配置文件
# 5. **IDE 配置完善：** 添加 PyCharm 项目配置，方便团队协作
# 6. **版本管理：** 版本号更新，便于追踪发布版本

# ### 📌 使用说明

# **打包命令：**
# ```bash
# cd endfield_damage_calculator
# python build.py
# ```

# **打包后文件位置：**
# - 可执行文件：`endfield_damage_calculator/终末地伤害计算器.exe`
# - 构建产物：`endfield_damage_calculator/build/终末地伤害计算器/`

# **注意事项：**
# - 打包后的 exe 文件较大（约 50-100 MB），因为包含了 Python 解释器和所有依赖
# - 首次运行可能较慢，因为需要解压临时文件
# - 确保 `characters.json` 和 `weapons.json` 文件存在，否则打包会失败