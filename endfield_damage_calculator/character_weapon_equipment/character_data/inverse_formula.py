#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
反向计算公式参数脚本

用于通过给定的等级数据，反向推导出属性成长公式的参数。

公式：base + floor((growth * (lv - 1) + offset) / divisor)

输入支持：
- 94个数据：对应等级1-90，其中第20,40,60,80级的数据重复，会自动去重
- 90个数据：认为是已经去重后的，直接处理
- 94或90的倍数：分成多组数据分别处理
"""

import math
import sys
from typing import List, Tuple


def remove_duplicates(data: List[int]) -> List[int]:
    """
    移除重复数据（第20,40,60,80级重复）
    重复位置：索引19-20, 40-41, 61-62, 82-83
    移除重复中后面的那个：索引20, 41, 62, 83
    """
    if len(data) != 94:
        raise ValueError(f"输入数据长度应为94，实际为{len(data)}")

    duplicate_indices = [20, 41, 62, 83]
    return [data[i] for i in range(94) if i not in duplicate_indices]


def fit_formula(data: List[int]) -> Tuple[int, int, int, int]:
    """
    拟合公式参数：base + floor((growth * (lv - 1) + offset) / divisor)
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
                        print(f"\n✅ 找到完全匹配的参数!")
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


def validate_formula(base: int, growth: int, divisor: int, offset: int, data: List[int]) -> bool:
    """验证公式"""
    for lv in range(1, 91):
        calculated = base + math.floor((growth * (lv - 1) + offset) / divisor)
        if calculated != data[lv-1]:
            return False
    return True


def parse_input(data_str: str) -> List[int]:
    """解析输入数据"""
    values = []
    for part in data_str.replace('\n', ' ').split():
        part = part.strip()
        if part:
            try:
                values.append(int(part))
            except ValueError:
                raise ValueError(f"无法解析 '{part}' 为整数")
    return values


def process_single_dataset(data: List[int], dataset_index: int = 1) -> None:
    """处理单个数据集"""
    print(f"\n{'='*60}")
    print(f"处理第 {dataset_index} 组数据")
    print(f"{'='*60}")
    
    data_length = len(data)
    
    if data_length == 94:
        print(f"输入数据: {len(data)} 个（原始格式，包含重复）")
        cleaned_data = remove_duplicates(data)
        print(f"去重后数据: {len(cleaned_data)} 个")
    elif data_length == 90:
        print(f"输入数据: {len(data)} 个（已去重格式）")
        cleaned_data = data.copy()
    else:
        print(f"错误: 单组数据长度应为90或94，实际为{data_length}")
        return

    base, growth, divisor, offset = fit_formula(cleaned_data)

    print("\n" + "="*50)
    print(f"第 {dataset_index} 组数据 - 公式参数计算结果")
    print("="*50)
    print(f'"base": {base}, "growth": {growth}, "divisor": {divisor}, "offset": {offset}')
    print("="*50)
    print(f"公式: value = {base} + floor(({growth} * (lv - 1) + {offset}) / {divisor})")
    print("="*50)

    if validate_formula(base, growth, divisor, offset, cleaned_data):
        print("✅ 验证通过：完全匹配")
    else:
        print("❌ 验证失败：存在误差")


def process_multiple_datasets(data: List[int]) -> None:
    """处理多组数据"""
    total_length = len(data)
    
    # 检测数据格式
    if total_length % 94 == 0:
        group_size = 94
        group_count = total_length // 94
        print(f"检测到 {group_count} 组原始数据（每组94个元素）")
    elif total_length % 90 == 0:
        group_size = 90
        group_count = total_length // 90
        print(f"检测到 {group_count} 组已去重数据（每组90个元素）")
    else:
        print(f"错误: 数据长度 {total_length} 不是90或94的倍数")
        return
    
    # 分割并处理每组数据
    for i in range(group_count):
        start_idx = i * group_size
        end_idx = start_idx + group_size
        group_data = data[start_idx:end_idx]
        process_single_dataset(group_data, i + 1)


def main():
    print("属性公式参数计算器")
    print("支持输入：90个元素（已去重）、94个元素（原始）、或它们的倍数（多组数据）")
    print("输入 'stop' 或 'quit' 退出程序")
    print("-" * 60)
    
    while True:
        print("\n请输入数据（用空格分隔），按回车结束：")
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
        if total_length == 90 or total_length == 94:
            process_single_dataset(data)
        elif total_length % 90 == 0 or total_length % 94 == 0:
            process_multiple_datasets(data)
        else:
            print(f"错误: 数据长度 {total_length} 不支持（应为90、94或它们的倍数）")


if __name__ == "__main__":
    main()