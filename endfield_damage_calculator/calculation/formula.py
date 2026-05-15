#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一公式模块

整合角色和武器的属性成长计算工具，支持通过配置参数生成成长曲线。

设计理念：
    通过配置驱动的方式，将成长参数存储在 JSON 中，
    添加新角色或武器时只需修改配置文件，无需修改代码。

属性成长公式说明：
    基础公式（1-90级）：base + floor((growth * (lv - 1) + offset) / divisor)
    特殊公式（10-12级）：可配置固定值或继续使用基础公式

数据范围：
    - levels: 等级 1-90
    - talent: 潜能/精炼等级 0-5
    - trust: 信赖等级 0-4
"""

import math
from typing import List, Dict, Any, Union


# ==================== 通用常量 ====================

# 等级列表（1-90级）
levels = list(range(1, 91))

# 潜能/精炼等级列表（0-5级）
talent = list(range(0, 6))

# 信赖等级列表（0-4级）
trust = list(range(0, 5))

# 信赖加成列表（0-4级）
trust_add = [0, 10, 15, 15, 20]


# ==================== 通用成长曲线计算器 ====================

def calculate_growth_curve(
    base: float | int,
    growth: float | int,
    divisor: float | int,
    offset: float | int = 0,
    max_level: int = 90
) -> List[float]:
    """
    计算属性成长曲线（通用公式）

    参数：
        base: 1级时的基础值（支持整数和小数）
        growth: 成长系数（支持整数和小数）
        divisor: 除数（用于控制成长速度，支持整数和小数）
        offset: 偏移量（微调成长曲线，支持整数和小数）
        max_level: 最大等级（默认90）

    公式：round(base + math.floor((growth * (lv - 1) + offset) / divisor), 1)

    返回：
        各等级属性值列表（索引0对应等级1，保留一位小数）

    异常：
        ValueError: 当divisor <= 0 或 max_level < 1时抛出
    """
    if divisor <= 0:
        raise ValueError("除数必须大于0")
    if max_level < 1:
        raise ValueError("最大等级必须大于等于1")

    return [
        round(base + math.floor((growth * (lv - 1) + offset) / divisor), 1)
        for lv in range(1, max_level + 1)
    ]


def calculate_skill_curve(
    base: float | int,
    growth: float | int,
    divisor: float | int,
    offset: float | int = 0,
    special_values: List[float | int] | None = None
) -> List[float]:
    """
    计算技能倍率成长曲线（支持10-12级特殊值）

    参数：
        base: 1级时的基础值（支持整数和小数）
        growth: 成长系数（支持整数和小数）
        divisor: 除数（支持整数和小数）
        offset: 偏移量（支持整数和小数）
        special_values: 10-12级的特殊值列表（长度为3，支持整数和小数）

    返回：
        各等级技能倍率列表（共12个值，索引0对应等级1，保留一位小数）

    异常：
        ValueError: 当divisor <= 0时抛出
    """
    if divisor <= 0:
        raise ValueError("除数必须大于0")

    # 1-9级使用公式计算
    curve = [
        round(base + math.floor((growth * (lv - 1) + offset) / divisor), 1)
        for lv in range(1, 10)
    ]

    # 10-12级使用特殊值或继续计算
    if special_values and len(special_values) >= 3:
        curve.extend([round(v, 1) for v in special_values[:3]])
    else:
        # 如果没有特殊值，继续使用公式计算
        curve.extend([
            round(base + math.floor((growth * (lv - 1) + offset) / divisor), 1)
            for lv in range(10, 13)
        ])

    return curve


def calculate_bonus_attribute(
    base: float | int,
    growth: float | int,
    divisor: float | int,
    offset: float | int = 0,
    special: List[float | int] | None = None,
    max_level: int = 9
) -> List[float]:
    """
    计算附加属性成长曲线（潜能1-9级）

    参数：
        base: 潜能1级时的基础值（支持整数和小数）
        growth: 成长系数（支持整数和小数）
        divisor: 除数（支持整数和小数）
        offset: 偏移量（支持整数和小数）
        special: 特殊值列表（第9级及以后的特殊值），如 [79] 表示第9级使用79（支持整数和小数）
        max_level: 最大等级，默认9

    返回：
        各潜能等级属性值列表（索引0对应潜能1，保留一位小数）
    """
    if divisor <= 0:
        raise ValueError("除数必须大于0")
    if max_level < 1:
        raise ValueError("最大等级必须大于等于1")

    # 前8级用公式计算
    curve = [
        round(base + math.floor((growth * (lv - 1) + offset) / divisor), 1)
        for lv in range(1, min(9, max_level + 1))
    ]

    # 如果有特殊值，第9级使用特殊值
    if max_level >= 9:
        if special and len(special) > 0:
            curve.append(round(special[0], 1))
        else:
            curve.append(round(base + math.floor((growth * 8 + offset) / divisor), 1))

    return curve


# ==================== 角色属性生成器 ====================

def generate_character_attributes(
    growth_params: Dict[str, Any]
) -> Dict[str, Union[List[float], List[List[float]]]]:
    """
    根据成长参数配置生成角色所有属性

    参数：
        growth_params: 成长参数配置字典，格式如下：
        {
            "力量": {"base": int, "growth": int, "divisor": int, "offset": int},
            "敏捷": {"base": int, "growth": int, "divisor": int, "offset": int},
            "智识": {"base": int, "growth": int, "divisor": int, "offset": int},
            "意志": {"base": int, "growth": int, "divisor": int, "offset": int},
            "基础攻击力": {"base": int, "growth": int, "divisor": int, "offset": int},
            "战技倍率": [
                {"base": int, "growth": int, "divisor": int, "offset": int, "special": [int, int, int]}
            ],
            "连携技倍率": [
                {"base": int, "growth": int, "divisor": int, "offset": int, "special": [int, int, int]},
                {"base": int, "growth": int, "divisor": int, "offset": int, "special": [int, int, int]}  # 第二段（可选）
            ],
            "终结技倍率": [
                {"base": int, "growth": int, "divisor": int, "offset": int, "special": [int, int, int]},
                {"base": int, "growth": int, "divisor": int, "offset": int, "special": [int, int, int]}  # 第二段（可选）
            ]
        }

    返回：
        包含所有属性成长曲线的字典
        - 普通属性返回 List[float]（90个值）
        - 技能倍率返回 List[List[float]]（每段12个值）
    """
    attributes: Dict[str, Union[List[float], List[List[float]]]] = {}

    # 属性类型分类
    normal_attrs = ["力量", "敏捷", "智识", "意志", "基础攻击力"]
    skill_attrs = ["战技倍率", "连携技倍率", "终结技倍率"]

    for attr_name in normal_attrs:
        if attr_name in growth_params:
            params = growth_params[attr_name]
            attributes[attr_name] = calculate_growth_curve(
                base=params.get("base", 0),
                growth=params.get("growth", 0),
                divisor=params.get("divisor", 1),
                offset=params.get("offset", 0)
            )

    for attr_name in skill_attrs:
        if attr_name in growth_params:
            segments = growth_params[attr_name]
            if isinstance(segments, list):
                # 支持多段技能
                curves: List[List[float]] = []
                for seg_params in segments:
                    special: List[float] | None = seg_params.get("special")
                    curves.append(calculate_skill_curve(
                        base=seg_params.get("base", 0),
                        growth=seg_params.get("growth", 0),
                        divisor=seg_params.get("divisor", 1),
                        offset=seg_params.get("offset", 0),
                        special_values=special
                    ))
                attributes[attr_name] = curves
            elif isinstance(segments, dict):
                # 兼容单段字典格式
                special: List[float] | None = segments.get("special")
                attributes[attr_name] = [calculate_skill_curve(
                    base=segments.get("base", 0),
                    growth=segments.get("growth", 0),
                    divisor=segments.get("divisor", 1),
                    offset=segments.get("offset", 0),
                    special_values=special
                )]

    return attributes


# ==================== 武器属性生成器 ====================

def generate_weapon_attributes(
    growth_params: Dict[str, Any]
) -> Dict[str, List[float]]:
    """
    根据成长参数配置生成武器所有属性

    参数：
        growth_params: 成长参数配置字典，格式如下：
        {
            "基础攻击力": {"base": float | int, "growth": float | int, "divisor": float | int, "offset": float | int},
            "敏捷+": {"base": float | int, "growth": float | int, "divisor": float | int, "offset": float | int, "special": list},
            "攻击力+": {"base": float | int, "growth": float | int, "divisor": float | int, "offset": float | int, "special": list},
            ...
        }

    返回：
        包含所有属性成长曲线的字典
    """
    attributes: Dict[str, List[float]] = {}

    for attr_name, params in growth_params.items():
        if attr_name == "基础攻击力":
            # 基础攻击力使用90级成长曲线
            attributes[attr_name] = calculate_growth_curve(
                base=params.get("base", 0),
                growth=params.get("growth", 0),
                divisor=params.get("divisor", 1),
                offset=params.get("offset", 0)
            )
        elif attr_name.endswith('+'):
            # 附加属性使用9级成长曲线（潜能）
            special: List[float | int] | None = params.get("special")
            attributes[attr_name] = calculate_bonus_attribute(
                base=params.get("base", 0),
                growth=params.get("growth", 0),
                divisor=params.get("divisor", 1),
                offset=params.get("offset", 0),
                special=special
            )

    return attributes


# ==================== 默认成长参数（原管理员数据）====================
# 这些参数可以迁移到 JSON 配置文件中
DEFAULT_GROWTH_PARAMS = {
    "力量": {"base": 14, "growth": 11, "divisor": 9, "offset": 8},
    "敏捷": {"base": 14, "growth": 17, "divisor": 12, "offset": 5},
    "智识": {"base": 9, "growth": 47, "divisor": 48, "offset": 38},
    "意志": {"base": 10, "growth": 13, "divisor": 12, "offset": 9},
    "基础攻击力": {"base": 30, "growth": 52, "divisor": 16, "offset": 5},
    "战技倍率": [{"base": 156, "growth": 78, "divisor": 5, "offset": 0, "special": [300, 323, 350]}],
    "连携技倍率": [
        {"base": 45, "growth": 22, "divisor": 5, "offset": 1, "special": [86, 93, 100]},
        {"base": 178, "growth": 71, "divisor": 4, "offset": 1, "special": [342, 369, 400]}
    ],
    "终结技倍率": [
        {"base": 356, "growth": 71, "divisor": 2, "offset": 0, "special": [684, 738, 800]},
        {"base": 267, "growth": 80, "divisor": 3, "offset": 1, "special": [514, 554, 600]}
    ]
}