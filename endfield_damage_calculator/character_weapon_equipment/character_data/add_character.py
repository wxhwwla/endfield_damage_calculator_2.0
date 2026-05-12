#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用角色添加脚本

使用方法：
    直接运行脚本，按照提示输入角色参数，或者在代码中配置参数。
"""
import json
import math
from pathlib import Path

def calculate_growth_curve(base, growth, divisor, offset, max_level=90):
    """计算属性成长曲线"""
    return [base + math.floor((growth * (lv - 1) + offset) / divisor) for lv in range(1, max_level + 1)]

def calculate_skill_curve(base, growth, divisor, offset, special_values, max_level=12):
    """计算技能倍率曲线，支持10-12级的特殊值"""
    curve = [base + math.floor((growth * (lv - 1) + offset) / divisor) for lv in range(1, 10)]
    if special_values and len(special_values) >= 3:
        curve.extend(special_values[:3])
    else:
        curve.extend([base + math.floor((growth * (lv - 1) + offset) / divisor) for lv in range(10, 13)])
    return curve

def add_character(
    name: str,
    char_type: str,
    star: int,
    primary: str,
    secondary: str,
    weapon: str,  # 可用武器（如"单手剑", "双手剑", "施术单元", "长柄武器"等）
    strength: dict,  # {"base": int, "growth": int, "divisor": int, "offset": int}
    agility: dict,
    intellect: dict,
    will: dict,
    base_atk: dict,
    sk1: list,  # list of dicts (战技倍率参数，支持多段伤害)
    sk2: list,  # list of dicts (连携技倍率参数，最多 2 个技能)
    sk3: list,  # list of dicts (终结技倍率参数，最多 2 个技能)
):
    """
    添加新角色到 characters.json

    参数：
        name: 角色名称
        char_type: 角色类型（如"近卫"）
        star: 星级（3-6）
        primary: 主能力（"力量"/"敏捷"/"智识"/"意志"）
        secondary: 副能力
        weapon: 可用武器（如"单手剑", "双手剑", "施术单元", "长柄武器"）
        strength: 力量成长参数
        agility: 敏捷成长参数
        intellect: 智识成长参数
        will: 意志成长参数
        base_atk: 基础攻击力成长参数
        sk1: 战技倍率参数（列表，支持多段伤害）
        sk2: 连携技倍率参数（列表，最多 2 个技能）
        sk3: 终结技倍率参数（列表，最多 2 个技能）
    """
    # 辅助函数：提取参数并计算曲线
    def calc_skill(params):
        if params.get("divisor", 1) == 0:
            return []
        special = params.pop("special", None)
        return calculate_skill_curve(**params, special_values=special)
    
    # 构建角色数据
    character = {
        "名称": name,
        "类型": char_type,
        "星级": star,
        "武器": weapon,
        "等级": list(range(1, 91)),
        "潜能": list(range(0, 6)),
        "信赖": list(range(0, 5)),
        "信赖加成": [0, 10, 15, 15, 20],
        "主能力": primary,
        "副能力": secondary,
        "力量": calculate_growth_curve(**strength),
        "敏捷": calculate_growth_curve(**agility),
        "智识": calculate_growth_curve(**intellect),
        "意志": calculate_growth_curve(**will),
        "基础攻击力": calculate_growth_curve(**base_atk),
        "战技倍率": [calc_skill(s.copy()) for s in sk1],
        "战技倍率1": calc_skill(sk1[0].copy()) if len(sk1) > 0 else [],
        "战技倍率2": calc_skill(sk1[1].copy()) if len(sk1) > 1 else [],
        "连携技倍率": [calc_skill(s.copy()) for s in sk2],
        "连携技倍率1": calc_skill(sk2[0].copy()) if len(sk2) > 0 else [],
        "连携技倍率2": calc_skill(sk2[1].copy()) if len(sk2) > 1 else [],
        "终结技倍率": [calc_skill(s.copy()) for s in sk3],
        "终结技倍率1": calc_skill(sk3[0].copy()) if len(sk3) > 0 else [],
        "终结技倍率2": calc_skill(sk3[1].copy()) if len(sk3) > 1 else [],
    }

    # 读取现有数据
    json_path = Path(__file__).parent / "characters.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        characters = json.load(f)

    # 检查是否已存在
    existing = [c for c in characters if c["名称"] == name]
    if existing:
        print(f"⚠️  角色「{name}」已存在，覆盖数据。")
        characters = [c for c in characters if c["名称"] != name]

    # 添加新角色
    characters.append(character)

    # 保存
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(characters, f, ensure_ascii=False, indent=2)

    print(f"✅ 角色「{name}」已添加！")
    print(f"   武器: {weapon}")
    print(f"   类型: {char_type}  星级: {star}星")
    print(f"   主能力: {primary}  副能力: {secondary}")
    print(f"   当前角色总数: {len(characters)}")


if __name__ == "__main__":
    print("="*60)
    print("通用角色添加工具")
    print("="*60)

    # =============== 在这里配置你的新角色参数 ===============
    # 示例：陈千语
    add_character(
        name="萤石",
        char_type="术师",
        star=4,
        primary="敏捷",
        secondary="智识",
        weapon="手铳",

        strength={"base": 14, "growth": 47, "divisor": 55, "offset": 7},
        agility={"base": 14, "growth": 119, "divisor": 69, "offset": 47},
        intellect={"base": 12, "growth": 70, "divisor": 61, "offset": 28},
        will={"base": 10, "growth": 57, "divisor": 62, "offset": 6},
        
        base_atk={"base": 30, "growth": 187, "divisor": 61, "offset": 32},

        sk1=[
            {"base": 187, "growth": 56, "divisor": 3, "offset": 1, "special": [360, 388, 420]},
        ],
        sk2=[
            {"base": 169, "growth": 101, "divisor": 6, "offset": 5, "special": [325, 351, 380]},
        ],
        sk3=[
            {"base": 111, "growth": 56, "divisor": 5, "offset": 1, "special": [214, 231, 250]},
        ],
    )
    # ======================================================