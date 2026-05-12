#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
路径工具模块

提供统一的路径处理功能，支持两种运行模式：
1. 开发模式：从源码运行（获取项目根目录）
2. 打包模式：从 PyInstaller 打包的 EXE 运行（获取 EXE 所在目录）

主要功能：
1. 获取应用程序根目录
2. 获取资源文件的完整路径
3. 支持开发和打包两种环境

依赖模块：
- sys: 系统相关操作
- pathlib: 路径对象处理
- os: 操作系统接口
"""

import sys
from pathlib import Path
import os


def _find_project_root() -> Path:
    """
    查找项目根目录（开发模式下使用）
    
    查找逻辑：
    1. 获取当前文件（path_utils.py）的绝对路径
    2. 逐级向上查找，直到找到包含特定标识文件的目录
    
    返回：
        项目根目录路径对象
    """
    # 获取当前文件的绝对路径
    current_file = Path(__file__).resolve()
    
    # 获取当前文件所在目录（utils 目录）
    current_dir = current_file.parent
    
    # 返回项目根目录（utils 的父目录）
    return current_dir.parent


def get_app_dir() -> Path:
    """
    获取应用程序根目录
    
    支持两种运行模式：
    1. 打包模式：通过 sys.frozen 判断，返回 EXE 所在目录
    2. 开发模式：返回项目源码根目录
    
    返回：
        应用程序根目录路径对象
    """
    # 判断是否为打包后的 EXE 运行
    if getattr(sys, 'frozen', False):
        # 打包模式：返回 EXE 所在目录
        return Path(sys.executable).parent
    else:
        # 开发模式：返回项目根目录
        return _find_project_root()


def get_resource_path(relative_path: str) -> Path:
    """
    获取资源文件的完整路径
    
    参数：
        relative_path: 资源文件相对于项目根目录的路径
        
    返回：
        资源文件的完整路径对象
    
    示例：
        get_resource_path("data/config.json")
        -> Path("C:/project/data/config.json")
    """
    # 获取应用根目录
    app_dir = get_app_dir()
    
    # 拼接完整路径
    return app_dir / relative_path


def ensure_dir_exists(file_path: Path) -> None:
    """
    确保文件所在目录存在（如果不存在则创建）
    
    参数：
        file_path: 文件路径对象
    
    功能：
        创建文件的父目录（如果不存在），用于确保写入文件时目录存在
    """
    # 获取文件所在目录
    parent_dir = file_path.parent
    
    # 如果目录不存在，创建它
    if not parent_dir.exists():
        parent_dir.mkdir(parents=True, exist_ok=True)


def is_file_exists(file_path: str) -> bool:
    """
    检查文件是否存在
    
    参数：
        file_path: 文件相对路径
        
    返回：
        文件存在返回 True，否则返回 False
    """
    # 获取完整路径
    full_path = get_resource_path(file_path)
    
    # 返回文件是否存在
    return full_path.exists() and full_path.is_file()


def list_directory(relative_path: str = "") -> list:
    """
    列出指定目录下的文件和子目录
    
    参数：
        relative_path: 相对于项目根目录的路径，默认为空（项目根目录）
        
    返回：
        目录内容列表（包含文件名和目录名）
    """
    # 获取目录完整路径
    dir_path = get_app_dir() / relative_path
    
    # 检查目录是否存在
    if not dir_path.exists() or not dir_path.is_dir():
        return []
    
    # 返回目录内容列表
    return [item.name for item in dir_path.iterdir()]
