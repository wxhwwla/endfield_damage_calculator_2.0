#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反向计算技能倍率公式参数脚本

用于通过给定的等级数据，反向推导出技能倍率成长公式的参数。

公式：base + floor((growth * (lv - 1) + offset) / divisor)

输入支持：
- 12个数据：对应等级1-12，其中10-12级为特殊值
- 9个数据：对应等级1-9，无特殊值
- 12或9的倍数：分成多组数据分别处理
"""

import math
import sys
from typing import List, Tuple


def parse_percent(value: str) -> int:
    """解析百分比字符串，返回整数"""
    value = value.strip()
    if value.endswith('%'):
        value = value[:-1]
    return int(value)


def parse_input(data_str: str) -> List[int]:
    """解析输入数据"""
    values = []
    for part in data_str.replace('\n', ' ').split():
        part = part.strip()
        if part:
            try:
                values.append(parse_percent(part))
            except ValueError:
                raise ValueError(f"无法解析 '{part}' 为整数")
    return values


def fit_skill_formula(data: List[int]) -> Tuple[int, int, int, int, List[int]]:
    """
    拟合技能倍率公式参数：base + floor((growth * (lv - 1) + offset) / divisor)

    特殊值（10-12级）直接从输入数据获取
    """
    if len(data) != 12:
        raise ValueError(f"技能倍率数据长度应为12，实际为{len(data)}")

    special_values = data[9:12]
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
                        print(f"\n✅ 找到完全匹配的参数!")
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


def fit_skill_formula_no_special(data: List[int]) -> Tuple[int, int, int, int, List[int]]:
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
                        print(f"\n✅ 找到完全匹配的参数!")
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


def validate_skill_formula(base: int, growth: int, divisor: int, offset: int, special_values: List[int], data: List[int]) -> bool:
    """验证公式（含特殊值）"""
    for lv in range(1, 10):
        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
        if calculated != data[lv-1]:
            return False
    for i in range(10, 13):
        if data[i-1] != special_values[i-10]:
            return False
    return True


def validate_skill_formula_no_special(base: int, growth: int, divisor: int, offset: int, special_values: List[int], data: List[int]) -> bool:
    """验证公式（9个元素版本）"""
    # 验证1-8级
    for lv in range(1, 9):
        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
        if calculated != data[lv-1]:
            return False
    # 验证9级特殊值
    if data[8] != special_values[0]:
        return False
    return True


def process_single_dataset(data: List[int], dataset_index: int = 1) -> None:
    """处理单个数据集"""
    print(f"\n{'='*60}")
    print(f"处理第 {dataset_index} 组数据")
    print(f"{'='*60}")
    
    data_length = len(data)
    
    if data_length == 12:
        print(f"输入数据: {len(data)} 个（含特殊值10-12级）")
        base, growth, divisor, offset, special_values = fit_skill_formula(data)
        
        print("\n" + "="*50)
        print(f"第 {dataset_index} 组数据 - 公式参数计算结果")
        print("="*50)
        print(f'"base": {base}, "growth": {growth}, "divisor": {divisor}, "offset": {offset}, "special": {special_values}')
        print("="*50)
        print(f"公式: value = {base} + floor(({growth} * (lv - 1) + {offset}) / {divisor})")
        print(f"特殊值(10-12级): {special_values}")
        print("="*50)

        if validate_skill_formula(base, growth, divisor, offset, special_values, data):
            print("✅ 验证通过：完全匹配")
        else:
            print("❌ 验证失败：存在误差")
            print("\n手动验证1-9级:")
            for lv in range(1, 10):
                calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
                expected = data[lv-1]
                status = "✅" if calculated == expected else "❌"
                print(f"  等级{lv}: 计算={calculated}, 期望={expected} {status}")
    elif data_length == 9:
        print(f"输入数据: {len(data)} 个（1-8级公式拟合，9级特殊值）")
        base, growth, divisor, offset, special_values = fit_skill_formula_no_special(data)
        
        print("\n" + "="*50)
        print(f"第 {dataset_index} 组数据 - 公式参数计算结果")
        print("="*50)
        print(f'"base": {base}, "growth": {growth}, "divisor": {divisor}, "offset": {offset}, "special": {special_values}')
        print("="*50)
        print(f"公式: value = {base} + floor(({growth} * (lv - 1) + {offset}) / {divisor})")
        print(f"特殊值(9级): {special_values}")
        print("="*50)

        if validate_skill_formula_no_special(base, growth, divisor, offset, special_values, data):
            print("✅ 验证通过：完全匹配")
        else:
            print("❌ 验证失败：存在误差")
            print("\n手动验证1-8级:")
            for lv in range(1, 9):
                calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
                expected = data[lv-1]
                status = "✅" if calculated == expected else "❌"
                print(f"  等级{lv}: 计算={calculated}, 期望={expected} {status}")
    else:
        print(f"错误: 单组数据长度应为9或12，实际为{data_length}")


def process_multiple_datasets(data: List[int]) -> None:
    """处理多组数据"""
    total_length = len(data)
    
    # 检测数据格式
    if total_length % 12 == 0:
        group_size = 12
        group_count = total_length // 12
        print(f"检测到 {group_count} 组数据（每组12个元素，含特殊值）")
    elif total_length % 9 == 0:
        group_size = 9
        group_count = total_length // 9
        print(f"检测到 {group_count} 组数据（每组9个元素，9级特殊值）")
    else:
        print(f"错误: 数据长度 {total_length} 不是9或12的倍数")
        return
    
    # 分割并处理每组数据
    for i in range(group_count):
        start_idx = i * group_size
        end_idx = start_idx + group_size
        group_data = data[start_idx:end_idx]
        process_single_dataset(group_data, i + 1)


def main():
    print("技能倍率公式参数计算器")
    print("支持输入：9个元素（仅1-9级）、12个元素（含10-12级特殊值）、或它们的倍数（多组数据）")
    print("输入 'stop' 或 'quit' 退出程序")
    print("-" * 60)
    
    while True:
        print("\n请输入数据（用空格分隔），按回车结束：")
        print("示例：169% 186% 203% 219% 236% 253% 270% 287% 304% 325% 350% 380%")
        data_str = input().strip()
        
        if data_str.lower() in ['stop', 'quit', 'exit']:
            print("退出程序...")
            break
            
        try:
            data = parse_input(data_str)
        except ValueError as e:
            print(f"错误: {e}")
            continue

        total_length = len(data)
        
        if total_length == 0:
            print("错误: 输入数据为空")
            continue
            
        # 判断是单组还是多组数据
        if total_length == 9 or total_length == 12:
            process_single_dataset(data)
        elif total_length % 9 == 0 or total_length % 12 == 0:
            process_multiple_datasets(data)
        else:
            print(f"错误: 数据长度 {total_length} 不支持（应为9、12或它们的倍数）")


if __name__ == "__main__":
    main()