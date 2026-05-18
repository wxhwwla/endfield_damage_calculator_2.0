#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式计算引擎

提供通用的成长曲线计算工具函数。

属性成长公式说明：
    基础公式（1-90级）：base + floor((growth * (lv - 1) + offset) / divisor)
    特殊公式（10-12级）：可配置固定值或继续使用基础公式

数据范围：
    - levels: 等级 1-90
    - talent: 潜能/精炼等级 0-5
    - trust: 信赖等级 0-4
"""

import math
from typing import List


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
