#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
乘法区伤害计算模块

此模块负责计算游戏中的乘法区伤害。

伤害计算公式（终末地游戏机制）：
总伤害 = 基础攻击力 × 攻击倍率 × 伤害加成 × 防御减伤 × 抗性减伤

乘法区包含：
1. 攻击倍率：角色技能倍率、武器技能倍率
2. 伤害加成：各类伤害加成效果
3. 防御减伤：基于敌方防御力的减伤系数
4. 抗性减伤：基于敌方元素抗性的减伤系数

当前状态：开发中
"""


def initialize_data() -> bool:
    """
    初始化数据（延迟加载）

    功能：
    1. 预加载武器数据
    2. 预加载角色数据
    3. 将数据缓存在内存中，提高后续访问速度

    返回值：
        bool: 数据是否加载成功（武器和角色数据都非空）

    调用时机：
    - 应用启动时调用一次即可
    - 在第一次计算伤害前调用

    设计说明：
    使用延迟导入避免潜在的循环依赖问题
    """
    try:
        # 延迟导入（避免循环依赖）
        from data.loader import get_weapons, get_characters

        # 加载武器数据（会自动缓存）
        weapons = get_weapons()

        # 加载角色数据（会自动缓存）
        characters = get_characters()

        # 返回数据是否加载成功
        return bool(weapons) and bool(characters)
    except Exception:
        return False


def gjl() -> None:
    """
    攻击倍率计算函数（待实现）

    功能（规划）：
        1. 根据角色等级和技能等级计算基础倍率
        2. 结合武器倍率加成（如武器技能倍率）
        3. 计算最终攻击倍率

    返回值（规划）：
        float: 攻击倍率数值（如 1.5 表示 150%）

    当前状态：待实现，占位函数

    计算逻辑（规划）：
        最终攻击倍率 = 角色技能倍率 × 武器技能倍率 × 其他倍率加成
    """
    pass


def calculate_damage(
    base_attack: float,
    skill_multiplier: float,
    damage_bonus: float = 1.0,
    defense_reduction: float = 1.0,
    resistance_reduction: float = 1.0
) -> float:
    """
    计算最终伤害（完整公式）

    参数：
        base_attack: 基础攻击力（角色基础攻击 + 武器攻击）
        skill_multiplier: 技能倍率（如 1.5 表示 150%）
        damage_bonus: 伤害加成系数（默认为 1.0，即无加成）
        defense_reduction: 防御减伤系数（默认为 1.0）
        resistance_reduction: 抗性减伤系数（默认为 1.0）

    返回：
        最终伤害值（float）

    计算公式：
        最终伤害 = 基础攻击力 × 技能倍率 × 伤害加成 × 防御减伤 × 抗性减伤

    示例：
        calculate_damage(1000, 1.5, 1.2, 0.8, 0.9)
        = 1000 × 1.5 × 1.2 × 0.8 × 0.9
        = 1296
    """
    # 计算最终伤害
    final_damage = (
        base_attack *
        skill_multiplier *
        damage_bonus *
        defense_reduction *
        resistance_reduction
    )

    return final_damage


def calculate_defense_reduction(
    attacker_level: int,
    defender_defense: int,
    defense_ignore: float = 0.0,
    defense_penetration: float = 0.0
) -> float:
    """
    计算防御减伤系数

    参数：
        attacker_level: 攻击者等级
        defender_defense: 防御者防御力
        defense_ignore: 防御忽略百分比（0.0-1.0，默认为 0）
        defense_penetration: 防御穿透值（默认为 0）

    返回：
        防御减伤系数（0-1之间的浮点数）

    计算公式（游戏机制）：
        减伤系数 = 攻击者等级 / (攻击者等级 + 防御者剩余防御)
        剩余防御 = 防御者防御力 × (1 - 防御忽略) - 防御穿透

    注意：剩余防御最小为 0
    """
    # 计算剩余防御
    remaining_defense = defender_defense * (1 - defense_ignore) - defense_penetration

    # 确保剩余防御不为负数
    remaining_defense = max(0, remaining_defense)

    # 计算减伤系数
    reduction = attacker_level / (attacker_level + remaining_defense)

    return reduction


def calculate_resistance_reduction(
    resistance: float,
    resistance_penetration: float = 0.0,
    resistance_ignore: float = 0.0
) -> float:
    """
    计算抗性减伤系数

    参数：
        resistance: 元素抗性值（通常为 0-1，即 0%-100%）
        resistance_penetration: 抗性穿透值（默认为 0）
        resistance_ignore: 抗性忽略百分比（0.0-1.0，默认为 0）

    返回：
        抗性减伤系数（0-1之间的浮点数）

    计算公式：
        剩余抗性 = max(0, (抗性 - 抗性穿透) × (1 - 抗性忽略))
        减伤系数 = 1 - 剩余抗性

    注意：抗性减伤系数最小为 0.1（即至少造成 10% 伤害）
    """
    # 计算剩余抗性
    remaining_resistance = max(0, (resistance - resistance_penetration) * (1 - resistance_ignore))

    # 计算减伤系数（最小保留 10% 伤害）
    reduction = max(0.1, 1 - remaining_resistance)

    return reduction