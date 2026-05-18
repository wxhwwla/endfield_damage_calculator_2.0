#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
武器属性生成器

此模块负责根据成长参数配置生成武器的所有属性数据。
"""
from typing import Dict, List, Any
from calculation.formula import calculate_growth_curve, calculate_bonus_attribute


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
            attributes[attr_name] = calculate_growth_curve(
                base=params.get("base", 0),
                growth=params.get("growth", 0),
                divisor=params.get("divisor", 1),
                offset=params.get("offset", 0)
            )
        elif attr_name.endswith('+'):
            special: List[float | int] | None = params.get("special")
            attributes[attr_name] = calculate_bonus_attribute(
                base=params.get("base", 0),
                growth=params.get("growth", 0),
                divisor=params.get("divisor", 1),
                offset=params.get("offset", 0),
                special=special
            )

    return attributes
