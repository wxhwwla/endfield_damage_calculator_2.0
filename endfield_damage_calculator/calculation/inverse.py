#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反向计算公式参数模块

用于通过给定的等级数据，反向推导出属性成长公式和技能倍率公式的参数。

公式：base + floor((growth * (lv - 1) + offset) / divisor)

输入支持：
- 属性数据：90或94个数据（等级1-90）
- 技能倍率：9或12个数据（等级1-9或1-12）
- 支持整数和小数百分比格式
"""

import math
from typing import List, Tuple, Sequence


# ==================== 属性成长反向计算 ====================

def remove_duplicates(data: Sequence[int | float]) -> List[int | float]:
    """
    移除重复数据（第20,40,60,80级重复）
    重复位置：索引19-20, 40-41, 61-62, 82-83
    移除重复中后面的那个：索引20, 41, 62, 83
    """
    if len(data) != 94:
        raise ValueError(f"输入数据长度应为94，实际为{len(data)}")

    duplicate_indices = [20, 41, 62, 83]
    return [data[i] for i in range(94) if i not in duplicate_indices]


def fit_attribute_formula(data: Sequence[int | float]) -> Tuple[int | float, int, int, int]:
    """
    拟合属性成长公式参数：base + floor((growth * (lv - 1) + offset) / divisor)
    """
    if len(data) != 90:
        raise ValueError(f"数据长度应为90，实际为{len(data)}")

    base = data[0]
    print(f"\n数据长度: 90")
    print(f"base = {base}")

    diffs = [data[i] - data[i-1] for i in range(1, 90)]
    print(f"差分: 平均={sum(diffs)/len(diffs):.3f}, 最大={max(diffs)}, 最小={min(diffs)}")

    best_params = None
    best_error = float('inf')

    for divisor in range(1, 201):
        for growth in range(1, 301):
            offset_lower = -10**18
            offset_upper = 10**18

            valid = True
            for lv in range(1, 91):
                target = data[lv-1] - base
                lower = target * divisor - growth * (lv - 1)
                upper = (target + 1) * divisor - growth * (lv - 1)
                offset_lower = max(offset_lower, lower)
                offset_upper = min(offset_upper, upper)
                if offset_lower >= offset_upper:
                    valid = False
                    break

            if valid and offset_lower < offset_upper:
                for offset in range(int(offset_lower), min(int(offset_upper) + 1, int(offset_lower) + 200)):
                    error = 0
                    for lv in range(1, 91):
                        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
                        if calculated != data[lv-1]:
                            error += abs(calculated - data[lv-1])

                    if error == 0:
                        print(f"\n[OK] 找到完全匹配的参数!")
                        return (base, growth, divisor, offset)
                    elif error < best_error:
                        best_error = error
                        best_params = (base, growth, divisor, offset)

    if best_params is None:
        print("\n未找到精确匹配，使用最小二乘法...")
        for divisor in range(1, 201):
            for growth in range(1, 301):
                total_offset = sum((data[lv-1] - base) * divisor - growth * (lv - 1) for lv in range(1, 91))
                offset = round(total_offset / 90)
                error = sum(abs(base + math.floor((growth * (lv - 1) + offset) / divisor) - data[lv-1]) for lv in range(1, 91))
                if error < best_error:
                    best_error = error
                    best_params = (base, growth, divisor, offset)

    assert best_params is not None, "无法找到合适的公式参数"
    return best_params


def validate_attribute_formula(base: int | float, growth: int, divisor: int, offset: int, data: Sequence[int | float]) -> bool:
    """验证属性成长公式"""
    for lv in range(1, 91):
        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
        if calculated != data[lv-1]:
            return False
    return True


# ==================== 技能倍率反向计算 ====================

def fit_skill_formula(data: Sequence[int | float]) -> Tuple[int | float, int, int, int, List[int | float]]:
    """
    拟合技能倍率公式参数：base + floor((growth * (lv - 1) + offset) / divisor)

    特殊值（10-12级）直接从输入数据获取
    """
    if len(data) != 12:
        raise ValueError(f"技能倍率数据长度应为12，实际为{len(data)}")

    special_values = list(data[9:12])
    base_data = data[:9]

    base = base_data[0]
    print(f"\nbase = {base}")

    diffs = [base_data[i] - base_data[i-1] for i in range(1, 9)]
    if diffs:
        print(f"差分(1-9级): 平均={sum(diffs)/len(diffs):.3f}, 最大={max(diffs)}, 最小={min(diffs)}")
    print(f"特殊值(10-12级): {special_values}")

    best_params = None
    best_error = float('inf')

    # 扩大搜索范围
    for divisor in range(1, 501):
        for growth in range(1, 601):
            offset_lower = -10**18
            offset_upper = 10**18

            valid = True
            for lv in range(1, 10):
                target = base_data[lv-1] - base
                lower = target * divisor - growth * (lv - 1)
                upper = (target + 1) * divisor - growth * (lv - 1)
                offset_lower = max(offset_lower, lower)
                offset_upper = min(offset_upper, upper)
                if offset_lower >= offset_upper:
                    valid = False
                    break

            if valid and offset_lower < offset_upper:
                for offset in range(int(offset_lower), min(int(offset_upper) + 1, int(offset_lower) + 500)):
                    error = 0
                    for lv in range(1, 10):
                        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
                        if calculated != base_data[lv-1]:
                            error += abs(calculated - base_data[lv-1])

                    if error == 0:
                        print(f"\n[OK] 找到完全匹配的参数!")
                        return (base, growth, divisor, offset, special_values)
                    elif error < best_error:
                        best_error = error
                        best_params = (base, growth, divisor, offset, special_values)

    if best_params is None:
        print("\n未找到精确匹配，使用最小二乘法...")
        for divisor in range(1, 501):
            for growth in range(1, 601):
                total_offset = sum((base_data[lv-1] - base) * divisor - growth * (lv - 1) for lv in range(1, 10))
                offset = round(total_offset / 9)
                error = sum(abs(base + math.floor((growth * (lv - 1) + offset) / divisor) - base_data[lv-1]) for lv in range(1, 10))
                if error < best_error:
                    best_error = error
                    best_params = (base, growth, divisor, offset, special_values)

    assert best_params is not None, "无法找到合适的公式参数"
    return best_params


def fit_skill_formula_no_special(data: Sequence[int | float]) -> Tuple[int | float, int, int, int, List[int | float]]:
    """
    拟合技能倍率公式参数（9个元素版本）：base + floor((growth * (lv - 1) + offset) / divisor)

    前8个数据用公式拟合（1-8级），第9个作为特殊值（9级）
    """
    if len(data) != 9:
        raise ValueError(f"技能倍率数据长度应为9，实际为{len(data)}")

    special_values = [data[8]]  # 第9个作为特殊值
    base_data = data[:8]  # 前8个用公式拟合

    base = base_data[0]
    print(f"\nbase = {base}")

    diffs = [base_data[i] - base_data[i-1] for i in range(1, 8)]
    if diffs:
        print(f"差分(1-8级): 平均={sum(diffs)/len(diffs):.3f}, 最大={max(diffs)}, 最小={min(diffs)}")
    print(f"特殊值(9级): {special_values}")

    best_params = None
    best_error = float('inf')

    # 扩大搜索范围
    for divisor in range(1, 501):
        for growth in range(1, 601):
            offset_lower = -10**18
            offset_upper = 10**18

            valid = True
            for lv in range(1, 9):  # 仅拟合1-8级
                target = base_data[lv-1] - base
                lower = target * divisor - growth * (lv - 1)
                upper = (target + 1) * divisor - growth * (lv - 1)
                offset_lower = max(offset_lower, lower)
                offset_upper = min(offset_upper, upper)
                if offset_lower >= offset_upper:
                    valid = False
                    break

            if valid and offset_lower < offset_upper:
                for offset in range(int(offset_lower), min(int(offset_upper) + 1, int(offset_lower) + 500)):
                    error = 0
                    for lv in range(1, 9):  # 仅验证1-8级
                        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
                        if calculated != base_data[lv-1]:
                            error += abs(calculated - base_data[lv-1])

                    if error == 0:
                        print(f"\n[OK] 找到完全匹配的参数!")
                        return (base, growth, divisor, offset, special_values)
                    elif error < best_error:
                        best_error = error
                        best_params = (base, growth, divisor, offset, special_values)

    if best_params is None:
        print("\n未找到精确匹配，使用最小二乘法...")
        for divisor in range(1, 501):
            for growth in range(1, 601):
                total_offset = sum((base_data[lv-1] - base) * divisor - growth * (lv - 1) for lv in range(1, 9))
                offset = round(total_offset / 8)
                error = sum(abs(base + math.floor((growth * (lv - 1) + offset) / divisor) - base_data[lv-1]) for lv in range(1, 9))
                if error < best_error:
                    best_error = error
                    best_params = (base, growth, divisor, offset, special_values)

    assert best_params is not None, "无法找到合适的公式参数"
    return best_params


def validate_skill_formula(base: int | float, growth: int, divisor: int, offset: int, special_values: List[int | float], data: Sequence[int | float]) -> bool:
    """验证技能倍率公式（含特殊值）"""
    for lv in range(1, 10):
        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
        if calculated != data[lv-1]:
            return False
    for i in range(10, 13):
        if data[i-1] != special_values[i-10]:
            return False
    return True


def validate_skill_formula_no_special(base: int | float, growth: int, divisor: int, offset: int, special_values: List[int | float], data: Sequence[int | float]) -> bool:
    """验证技能倍率公式（9个元素版本）"""
    # 验证1-8级
    for lv in range(1, 9):
        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
        if calculated != data[lv-1]:
            return False
    # 验证9级特殊值
    if data[8] != special_values[0]:
        return False
    return True


# ==================== 快捷接口 ====================

def fit_formula(data: Sequence[int | float]) -> Tuple[int | float, int, int, int, List[int | float] | None]:
    """
    统一拟合接口，自动检测数据类型
    
    返回：(base, growth, divisor, offset, special_values)
    """
    if len(data) == 90:
        base, growth, divisor, offset = fit_attribute_formula(data)
        return (base, growth, divisor, offset, None)
    elif len(data) == 12:
        return fit_skill_formula(data)
    elif len(data) == 9:
        return fit_skill_formula_no_special(data)
    else:
        raise ValueError(f"不支持的数据长度: {len(data)}")


def validate_formula(base: int | float, growth: int, divisor: int, offset: int, data: Sequence[int | float], special_values: List[int | float] | None = None) -> bool:
    """
    统一验证接口，自动检测数据类型
    """
    if len(data) == 90:
        return validate_attribute_formula(base, growth, divisor, offset, data)
    elif len(data) == 12:
        return validate_skill_formula(base, growth, divisor, offset, special_values or [], data)
    elif len(data) == 9:
        return validate_skill_formula_no_special(base, growth, divisor, offset, special_values or [], data)
    else:
        raise ValueError(f"不支持的数据长度: {len(data)}")