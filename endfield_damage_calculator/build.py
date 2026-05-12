#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
终末地伤害计算器 - 打包脚本

使用PyInstaller将程序打包为Windows可执行文件
"""

import os
import sys
import subprocess
from pathlib import Path


def check_pyinstaller() -> bool:
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print(f"PyInstaller 已安装: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("PyInstaller 未安装，正在安装...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True


def build_exe():
    """使用PyInstaller构建可执行文件"""
    project_root = Path(__file__).parent
    
    # 定义PyInstaller参数
    args = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",              # 单文件模式
        "--windowed",             # 无控制台窗口
        "--name=终末地伤害计算器",
        "--add-data", f"{project_root / 'character_weapon_equipment' / 'character_data' / 'characters.json'};character_weapon_equipment/character_data/",
        "--add-data", f"{project_root / 'character_weapon_equipment' / 'weapon_data' / 'weapons.json'};character_weapon_equipment/weapon_data/",
        "--clean",                # 清理临时文件
        str(project_root / "main.py")
    ]
    
    print("=" * 60)
    print("开始打包...")
    print("=" * 60)
    
    # 执行打包命令
    try:
        subprocess.check_call(args, cwd=project_root)
        print("\n" + "=" * 60)
        print("打包完成！")
        print(f"可执行文件位置: {project_root / 'dist' / '终末地伤害计算器.exe'}")
        print("=" * 60)
        
        # 将可执行文件移动到根目录
        exe_source = project_root / "dist" / "终末地伤害计算器.exe"
        exe_target = project_root / "终末地伤害计算器.exe"
        
        if exe_source.exists():
            import shutil
            shutil.copy2(exe_source, exe_target)
            print(f"\n已将可执行文件复制到: {exe_target}")
            
    except subprocess.CalledProcessError as e:
        print(f"\n打包失败: {e}")
        sys.exit(1)


def main():
    print("终末地伤害计算器 - 打包工具")
    print("-" * 60)
    
    # 检查PyInstaller
    if not check_pyinstaller():
        sys.exit(1)
    
    # 执行打包
    build_exe()


if __name__ == "__main__":
    main()
