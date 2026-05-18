#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式参数计算器 CLI

此脚本提供交互式的公式参数计算界面。

功能：
- 通过输入属性数据反推属性成长公式参数
- 通过输入技能倍率数据反推技能公式参数
- 支持带标签的批量数据输入

用法：
    python scripts/inverse_cli.py
"""
import re
import sys
from pathlib import Path
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent / "endfield_damage_calculator"))

from calculation.inverse import (
    remove_duplicates,
    fit_attribute_formula,
    fit_skill_formula,
    fit_skill_formula_no_special,
    validate_attribute_formula,
)


def parse_percent(value: str) -> Tuple[int, bool]:
    """解析百分比字符串（支持整数和小数）"""
    value = value.strip()
    is_decimal = False
    
    if value.endswith('%'):
        value = value[:-1]
    
    if '.' in value:
        is_decimal = True
        try:
            decimal_value = float(value)
            return int(decimal_value * 10), is_decimal
        except ValueError:
            raise ValueError(f"输入 '{value}' 不是有效的数字")
    else:
        if not value.isdigit():
            raise ValueError(f"输入 '{value}' 不是有效的整数")
        return int(value), is_decimal


def parse_input(data_str: str, data_type: str = "auto") -> Tuple[List[int], bool]:
    """解析输入数据"""
    values = []
    is_decimal = False
    raw_values = []
    
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
    
    if is_decimal:
        for i, part in enumerate(raw_values):
            part = part.strip()
            if part.endswith('%'):
                part = part[:-1]
            if '.' not in part and part.isdigit():
                values[i] = int(part) * 10
    
    return values, is_decimal


def parse_input_with_tags(data_str: str) -> Tuple[List[List[int | float]], List[str]]:
    """解析带标签的输入数据"""
    tags = ['力量', '敏捷', '智识', '意志', '攻击力']
    tag_pattern = '|'.join(tags)

    parts = re.split(f'({tag_pattern})', data_str)

    groups = []
    group_names = []

    if parts and parts[0].strip():
        nums = [float(x) if '.' in x else int(x) for x in re.findall(r'\d+\.?\d*', parts[0])]
        if nums:
            groups.append(nums)
            group_names.append('第一组')

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
