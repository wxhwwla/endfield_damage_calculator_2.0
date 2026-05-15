#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI 工具组件模块（导出层）

此模块作为统一导出接口，保持向后兼容性。
实际实现已迁移到以下子模块：
- gui_settings: GUI 全局设置
- selection_panel: 选择面板类
- property_display: 属性展示函数
"""

# 从子模块导入
from .gui_settings import gui_settings
from .selection_panel import ChooseTypesStarsNamesLevels
from .property_display import confirm_selection, LEVEL_ATTRIBUTES, _get_attribute_value

# 导出所有公共接口
__all__ = [
    'gui_settings',
    'ChooseTypesStarsNamesLevels',
    'confirm_selection',
    'LEVEL_ATTRIBUTES',
    '_get_attribute_value'
]
