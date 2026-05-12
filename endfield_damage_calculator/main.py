#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终末地伤害计算小工具 - 项目入口文件

项目结构说明：
├── main.py                    # 项目入口，启动应用
├── pyproject.toml             # 打包配置文件
├── gui_design/                # GUI 界面模块
│   ├── gui.py                 # 主应用类，管理窗口和布局
│   ├── gui_tools.py           # GUI 工具组件导出层
│   ├── gui_settings.py        # GUI 设置初始化
│   ├── selection_panel.py     # 选择面板类
│   └── property_display.py    # 属性展示函数
├── calculation/               # 计算逻辑模块
│   └── multiplicative_zone.py # 乘法区伤害计算
├── data/                      # 统一数据加载层
│   └── loader.py              # 角色和武器数据的统一加载与缓存
├── utils/                     # 工具函数模块
│   └── path_utils.py          # 路径处理工具（支持打包后运行）
└── character_weapon_equipment/# 数据文件目录
    ├── character_data/        # 角色数据（JSON格式）
    └── weapon_data/           # 武器数据（JSON格式）

功能说明：
1. 提供角色和武器选择界面
2. 显示选中角色/武器的属性
3. 预留伤害计算区域（开发中）

使用方式：
    python main.py
"""

def main() -> None:
    """
    应用主入口函数

    功能：
    1. 延迟导入 GUI 模块（加快启动速度）
    2. 创建应用实例
    3. 启动主事件循环
    """
    import character_weapon_equipment.weapon_data.weapon_data as _weapon_data_module
    import character_weapon_equipment.character_data.character_data as _character_data_module

    from gui_design.gui import DamageCalculatorApp
    
    # 创建应用实例
    app = DamageCalculatorApp()
    
    # 启动主事件循环，显示窗口
    app.run()


# 程序入口判断
if __name__ == "__main__":
    # 调用主函数启动应用
    main()

