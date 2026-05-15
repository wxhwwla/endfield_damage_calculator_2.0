#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
计算模块包

整合所有计算相关功能，提供统一的导入接口。

包含：
- 正向计算公式（角色/武器属性成长）
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
    generate_character_attributes,
    generate_weapon_attributes,
    DEFAULT_GROWTH_PARAMS,
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
    parse_percent,
    parse_input,
)

# 伤害乘区计算
# 合并来自 multiplicative_zone 和 multiplicative_zones 的导入
from calculation.multiplicative_zone import (
    initialize_data,
    calculate_damage,
    calculate_defense_reduction,
    calculate_resistance_reduction,
)
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
    "DEFAULT_GROWTH_PARAMS",
    # 正向计算
    "calculate_growth_curve",
    "calculate_skill_curve",
    "calculate_bonus_attribute",
    "generate_character_attributes",
    "generate_weapon_attributes",
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
    "parse_percent",
    "parse_input",
    # 伤害计算
    "initialize_data",
    "calculate_damage",
    "calculate_defense_reduction",
    "calculate_resistance_reduction",
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