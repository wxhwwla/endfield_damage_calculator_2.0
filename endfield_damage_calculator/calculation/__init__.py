#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算模块包

整合所有计算相关功能，提供统一的导入接口。

包含：
- 正向计算公式（通用成长曲线计算）
- 反向推导公式（通过数据反推公式参数）
- 伤害乘区计算（乘法区伤害计算）
"""

# 正向计算公式
from calculation.formula import (
    levels,
    talent,
    trust,
    trust_add,
    calculate_growth_curve,
    calculate_skill_curve,
    calculate_bonus_attribute,
)

# 反向推导公式
from calculation.inverse import (
    remove_duplicates,
    fit_attribute_formula,
    fit_skill_formula,
    fit_skill_formula_no_special,
    fit_formula,
    validate_attribute_formula,
    validate_skill_formula,
    validate_skill_formula_no_special,
    validate_formula,
)

# 伤害乘区计算
from calculation.multiplicative_zones import (
    ZoneManager,
    BaseZone,
    DefenseReductionZone,
    AttributeMultiplierZone,
    AttributeZoneManager,
    calculate_attribute_zones,
    calculate_attribute_zones_with_details,
    AbilityBonusZone,
    calculate_ability_bonus,
    calculate_ability_bonus_with_details,
    FinalAttackZone,
    calculate_final_attack,
    calculate_final_attack_with_details,
)

__all__ = [
    # 常量
    "levels",
    "talent",
    "trust",
    "trust_add",
    # 正向计算
    "calculate_growth_curve",
    "calculate_skill_curve",
    "calculate_bonus_attribute",
    # 反向推导
    "remove_duplicates",
    "fit_attribute_formula",
    "fit_skill_formula",
    "fit_skill_formula_no_special",
    "fit_formula",
    "validate_attribute_formula",
    "validate_skill_formula",
    "validate_skill_formula_no_special",
    "validate_formula",
    # 乘区类
    "ZoneManager",
    "BaseZone",
    "DefenseReductionZone",
    "AttributeMultiplierZone",
    "AttributeZoneManager",
    "calculate_attribute_zones",
    "calculate_attribute_zones_with_details",
    "AbilityBonusZone",
    "calculate_ability_bonus",
    "calculate_ability_bonus_with_details",
    "FinalAttackZone",
    "calculate_final_attack",
    "calculate_final_attack_with_details",
]
