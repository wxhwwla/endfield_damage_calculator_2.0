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
import sys
import re
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

def parse_percent(value: str) -> Tuple[int, bool]:
    """解析百分比字符串（支持整数和小数）
    
    支持格式：
    - 整数百分比: "156%" -> 156
    - 整数: "156" -> 156
    - 小数百分比: "3.3%" -> 33 (乘10)
    - 小数: "3.3" -> 33 (乘10)
    
    返回值：(百分比值的整数, 是否为小数)
    """
    value = value.strip()
    is_decimal = False
    
    if value.endswith('%'):
        value = value[:-1]
    
    # 检查是否为小数
    if '.' in value:
        is_decimal = True
        # 将小数转换为整数（乘10）
        try:
            decimal_value = float(value)
            return int(decimal_value * 10), is_decimal
        except ValueError:
            raise ValueError(f"输入 '{value}' 不是有效的数字")
    else:
        # 整数输入
        if not value.isdigit():
            raise ValueError(f"输入 '{value}' 不是有效的整数")
        return int(value), is_decimal


def parse_input(data_str: str, data_type: str = "auto") -> Tuple[List[int], bool]:
    """解析输入数据
    
    参数：
        data_str: 输入数据字符串
        data_type: 数据类型，"auto"自动检测，"attribute"属性，"skill"技能
        
    返回值：(数据列表, 是否为小数)
    """
    values = []
    is_decimal = False
    raw_values = []  # 保存原始字符串值用于判断是否有小数
    
    for part in data_str.replace('\n', ' ').split():
        part = part.strip()
        if part:
            raw_values.append(part)
            try:
                val, dec = parse_percent(part)
                values.append(val)
                if dec:
                    is_decimal = True
            except ValueError:
                raise ValueError(f"无法解析 '{part}' 为数字")
    
    # 如果存在小数，所有整数百分比也需要乘10
    if is_decimal:
        for i, part in enumerate(raw_values):
            part = part.strip()
            if part.endswith('%'):
                part = part[:-1]
            # 如果是整数但没被乘10，现在乘10
            if '.' not in part and part.isdigit():
                values[i] = int(part) * 10
    
    return values, is_decimal


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


# ==================== 命令行工具 ====================

def parse_input_with_tags(data_str: str) -> Tuple[List[List[int | float]], List[str]]:
    """解析带标签的输入数据（如：力量...敏捷...智识...意志...攻击力...）"""
    # 定义标签（按优先级排序，避免短标签干扰）
    tags = ['力量', '敏捷', '智识', '意志', '攻击力']
    tag_pattern = '|'.join(tags)
    
    # 分割数据
    parts = re.split(f'({tag_pattern})', data_str)
    
    # 提取标签后的数据
    groups = []
    group_names = []
    
    # 如果开头就有数据（第一个标签前面的数据）
    if parts and parts[0].strip():
        # 提取开头数据（支持整数和小数）
        nums = [float(x) if '.' in x else int(x) for x in re.findall(r'\d+\.?\d*', parts[0])]
        if nums:
            groups.append(nums)
            group_names.append('第一组')
    
    # 提取标签后的数据
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            tag = parts[i]
            content = parts[i+1]
            nums = [float(x) if '.' in x else int(x) for x in re.findall(r'\d+\.?\d*', content)]
            if nums:
                groups.append(nums)
                group_names.append(tag)
    
    return groups, group_names


def main():
    print("公式参数计算器")
    print("支持输入：")
    print("  - 属性数据：90或94个元素（等级1-90）")
    print("  - 技能倍率：9或12个元素（等级1-9或1-12）")
    print("  - 也支持标签格式：敏捷...智识...意志...攻击力...")
    print("支持整数和小数百分比格式（如：156% 或 3.3%）")
    print("输入 'stop' 或 'quit' 退出程序")
    print("-" * 60)
    
    while True:
        print("\n请输入数据（用空格分隔），按回车结束：")
        data_str = input().strip()
        
        if data_str.lower() in ['stop', 'quit', 'exit']:
            print("退出程序...")
            break
            
        try:
            # 先尝试标签格式解析（属性数据）
            groups, group_names = parse_input_with_tags(data_str)
            if groups and all(len(g) in [90, 94] for g in groups):
                for name, group in zip(group_names, groups):
                    print(f"\n{'='*60}")
                    print(f"处理: {name}")
                    print(f"{'='*60}")
                    
                    if len(group) == 94:
                        print(f"输入数据: 94个（原始格式）")
                        cleaned_data = remove_duplicates(group)
                    else:
                        print(f"输入数据: 90个（已去重）")
                        cleaned_data = group
                    
                    base, growth, divisor, offset = fit_attribute_formula(cleaned_data)
                    
                    print(f'\n"base": {base}, "growth": {growth}, "divisor": {divisor}, "offset": {offset}')
                    print(f"公式: value = {base} + floor(({growth} * (lv - 1) + {offset}) / {divisor})")
                    
                    if validate_attribute_formula(base, growth, divisor, offset, cleaned_data):
                        print("[OK] 验证通过")
                    else:
                        print("[X] 验证失败")
                continue
        except Exception:
            pass
        
        # 尝试技能倍率解析
        try:
            data, is_decimal = parse_input(data_str)
        except ValueError as e:
            print(f"错误: {e}")
            continue
        
        total_length = len(data)
        
        if total_length == 0:
            print("错误: 输入数据为空")
            continue
            
        if total_length == 9 or total_length == 12:
            # 单组技能数据
            if total_length == 12:
                base, growth, divisor, offset, special = fit_skill_formula(data)
                if is_decimal:
                    print(f'\n"base": {base/10}, "growth": {growth/10}, "divisor": {divisor}, "offset": {offset/10}, "special": {[v/10 for v in special]}')
                else:
                    print(f'\n"base": {base}, "growth": {growth}, "divisor": {divisor}, "offset": {offset}, "special": {special}')
            else:
                base, growth, divisor, offset, special = fit_skill_formula_no_special(data)
                if is_decimal:
                    print(f'\n"base": {base/10}, "growth": {growth/10}, "divisor": {divisor}, "offset": {offset/10}, "special": {[v/10 for v in special]}')
                else:
                    print(f'\n"base": {base}, "growth": {growth}, "divisor": {divisor}, "offset": {offset}, "special": {special}')
        elif total_length % 9 == 0 or total_length % 12 == 0:
            # 多组技能数据
            group_size = 12 if total_length % 12 == 0 else 9
            for i in range(total_length // group_size):
                group_data = data[i*group_size:(i+1)*group_size]
                print(f"\n{'='*60}")
                print(f"处理第 {i+1} 组数据")
                print(f"{'='*60}")
                
                if group_size == 12:
                    base, growth, divisor, offset, special = fit_skill_formula(group_data)
                    if is_decimal:
                        print(f'\n"base": {base/10}, "growth": {growth/10}, "divisor": {divisor}, "offset": {offset/10}, "special": {[v/10 for v in special]}')
                    else:
                        print(f'\n"base": {base}, "growth": {growth}, "divisor": {divisor}, "offset": {offset}, "special": {special}')
                else:
                    base, growth, divisor, offset, special = fit_skill_formula_no_special(group_data)
                    if is_decimal:
                        print(f'\n"base": {base/10}, "growth": {growth/10}, "divisor": {divisor}, "offset": {offset/10}, "special": {[v/10 for v in special]}')
                    else:
                        print(f'\n"base": {base}, "growth": {growth}, "divisor": {divisor}, "offset": {offset}, "special": {special}')
        else:
            print(f"错误: 数据长度 {total_length} 不支持")


if __name__ == "__main__":
    main()