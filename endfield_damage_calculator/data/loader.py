#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一数据加载层

此模块提供角色和武器数据的统一加载接口，支持数据缓存机制，
避免重复读取文件。

主要功能：
1. 加载 JSON 数据文件
2. 提供角色和武器数据的获取接口（带缓存）
3. 支持检查并保存数据到 JSON 文件

数据文件路径：
- 角色数据：character_weapon_equipment/character_data/characters.json
- 武器数据：character_weapon_equipment/weapon_data/weapons.json
"""
import json
from typing import List, Dict, Any, Optional
from utils.path_utils import get_resource_path

# 缓存数据
_characters: Optional[List[Dict[str, Any]]] = None
_weapons: Optional[List[Dict[str, Any]]] = None

# 数据文件路径配置
CHARACTERS_JSON_PATH: str = "character_weapon_equipment/character_data/characters.json"
WEAPONS_JSON_PATH: str = "character_weapon_equipment/weapon_data/weapons.json"


def load_json_file(filepath: str) -> List[Dict[str, Any]]:
    """加载 JSON 文件并返回数据列表

    Args:
        filepath: 相对于项目根目录的路径

    Returns:
        JSON 数据列表，如果文件不存在或解析失败返回空列表
    """
    try:
        full_path = get_resource_path(filepath)
        if not full_path.exists():
            return []

        with open(full_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []


def get_characters() -> List[Dict[str, Any]]:
    """获取所有角色数据（带缓存）

    Returns:
        角色数据列表
    """
    global _characters
    if _characters is None:
        _characters = load_json_file(CHARACTERS_JSON_PATH)
    return _characters


def get_weapons() -> List[Dict[str, Any]]:
    """获取所有武器数据（带缓存）

    Returns:
        武器数据列表
    """
    global _weapons
    if _weapons is None:
        _weapons = load_json_file(WEAPONS_JSON_PATH)
    return _weapons


def reload_characters() -> None:
    """重新加载角色数据（清除缓存）"""
    global _characters
    _characters = None


def reload_weapons() -> None:
    """重新加载武器数据（清除缓存）"""
    global _weapons
    _weapons = None


def save_characters(data: List[Dict[str, Any]]) -> bool:
    """保存角色数据到 JSON 文件

    Args:
        data: 要保存的角色数据列表

    Returns:
        是否保存成功
    """
    try:
        full_path = get_resource_path(CHARACTERS_JSON_PATH)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        reload_characters()
        return True
    except Exception:
        return False


def save_weapons(data: List[Dict[str, Any]]) -> bool:
    """保存武器数据到 JSON 文件

    Args:
        data: 要保存的武器数据列表

    Returns:
        是否保存成功
    """
    try:
        full_path = get_resource_path(WEAPONS_JSON_PATH)
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        reload_weapons()
        return True
    except Exception:
        return False


def check_and_save_characters(characters: List[Dict[str, Any]]) -> None:
    """检查并保存角色数据（仅在数据有变化时保存）"""
    if not characters:
        return

    current_data = get_characters()
    if not current_data:
        save_characters(characters)
        return

    if characters != current_data:
        save_characters(characters)


def check_and_save_weapons(weapons: List[Dict[str, Any]]) -> None:
    """检查并保存武器数据（仅在数据有变化时保存）"""
    if not weapons:
        return

    current_data = get_weapons()
    if not current_data:
        save_weapons(weapons)
        return

    if weapons != current_data:
        save_weapons(weapons)