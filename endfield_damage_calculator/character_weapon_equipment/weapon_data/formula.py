#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
武器属性计算公式模块

提供通用的武器属性成长计算工具，支持通过配置参数生成武器属性成长曲线。

设计理念：
    通过配置驱动的方式，将武器属性成长参数存储在 JSON 中，
    添加新武器时只需修改配置文件，无需修改代码。

属性成长公式说明：
    基础公式（1-90级）：base + floor((growth * (lv - 1) + offset) / divisor)

数据范围：
    - levels: 武器等级 1-90
    - talent: 精炼等级 0-5
"""

import math
from typing import List, Dict, Any


# ==================== 通用常量 ====================

# 武器等级列表（1-90级）
levels = list(range(1, 91))

# 精炼等级列表（0-5级）
talent = list(range(0, 6))


# ==================== 通用成长曲线计算器 ====================

def calculate_weapon_attack(
    base: int,
    growth: int,
    divisor: int,
    offset: int = 0,
    max_level: int = 90
) -> List[int]:
    """
    计算武器基础攻击力成长曲线（通用公式）

    参数：
        base: 1级时的基础攻击力
        growth: 成长系数
        divisor: 除数（用于控制成长速度）
        offset: 偏移量（微调成长曲线）
        max_level: 最大等级（默认90）

    公式：base + floor((growth * (lv - 1) + offset) / divisor)

    返回：
        各等级攻击力列表（索引0对应等级1）

    异常：
        ValueError: 当divisor <= 0 或 max_level < 1时抛出
    """
    if divisor <= 0:
        raise ValueError("除数必须大于0")
    if max_level < 1:
        raise ValueError("最大等级必须大于等于1")

    return [
        base + math.floor((growth * (lv - 1) + offset) / divisor)
        for lv in range(1, max_level + 1)
    ]


def calculate_bonus_attribute(
    base: int,
    growth: int,
    divisor: int,
    offset: int = 0,
    special: List[int] | None = None,
    max_level: int = 9
) -> List[int]:
    """
    计算武器附加属性成长曲线（潜能1-9级）

    参数：
        base: 潜能1级时的基础值
        growth: 成长系数
        divisor: 除数
        offset: 偏移量
        special: 特殊值列表（第9级及以后的特殊值），如 [79] 表示第9级使用79
        max_level: 最大等级，默认9

    返回：
        各潜能等级属性值列表（索引0对应潜能1）
    """
    if divisor <= 0:
        raise ValueError("除数必须大于0")
    if max_level < 1:
        raise ValueError("最大等级必须大于等于1")

    # 前8级用公式计算
    curve = [
        base + math.floor((growth * (lv - 1) + offset) / divisor)
        for lv in range(1, min(9, max_level + 1))
    ]

    # 如果有特殊值，第9级使用特殊值
    if max_level >= 9:
        if special and len(special) > 0:
            curve.append(special[0])
        else:
            curve.append(base + math.floor((growth * 8 + offset) / divisor))

    return curve


def generate_weapon_attributes(
    growth_params: Dict[str, Any]
) -> Dict[str, List[int]]:
    """
    根据成长参数配置生成武器所有属性

    参数：
        growth_params: 成长参数配置字典，格式如下：
        {
            "基础攻击力": {"base": int, "growth": int, "divisor": int, "offset": int},
            "敏捷+": {"base": int, "growth": int, "divisor": int, "offset": int, "special": list},
            "攻击力+": {"base": int, "growth": int, "divisor": int, "offset": int, "special": list},
            ...
        }

    返回：
        包含所有属性成长曲线的字典
    """
    attributes: Dict[str, List[int]] = {}

    for attr_name, params in growth_params.items():
        if attr_name == "基础攻击力":
            # 基础攻击力使用90级成长曲线
            attributes[attr_name] = calculate_weapon_attack(
                base=params.get("base", 0),
                growth=params.get("growth", 0),
                divisor=params.get("divisor", 1),
                offset=params.get("offset", 0)
            )
        elif attr_name.endswith('+'):
            # 附加属性使用9级成长曲线（潜能）
            special: List[int] | None = params.get("special")
            attributes[attr_name] = calculate_bonus_attribute(
                base=params.get("base", 0),
                growth=params.get("growth", 0),
                divisor=params.get("divisor", 1),
                offset=params.get("offset", 0),
                special=special
            )

    return attributes
