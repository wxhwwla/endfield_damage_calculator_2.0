#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 功能：从远程 Git 仓库拉取代码并强制覆盖本地（强制推送的反向操作）
# 运行位置：文件夹内（脚本与密钥同目录）

import os
import sys
import subprocess
from datetime import datetime

# ===== 配置区 =====
REMOTE_REPO = "https://github.com/wxhwwla/endfield_damage_calculator_2.0.git"
KEY_FILE = "git_key.txt"
# 从环境变量获取用户名，默认为空（使用 token 认证时可省略用户名）
GIT_USERNAME = os.environ.get("GIT_USERNAME", "wxhwwla")
# =================

def _decode_output(output) -> str:
    """统一解码输出，确保返回字符串"""
    if output is None:
        return ""
    if isinstance(output, str):
        return output
    if isinstance(output, bytes):
        return output.decode('utf-8', errors='replace')
    if isinstance(output, memoryview):
        return bytes(output).decode('utf-8', errors='replace')
    return str(output)

from typing import Any, Tuple

def run_git(args, check=True, capture_output=False) -> Tuple[Any, str, str]:
    """执行 Git 命令"""
    try:
        if capture_output:
            proc = subprocess.run(
                ["git"] + args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8',
                errors='replace',
                check=check
            )
            stdout = _decode_output(proc.stdout)
            stderr = _decode_output(proc.stderr)
            return (proc.returncode, stdout, stderr)
        else:
            proc = subprocess.run(["git"] + args, check=check)
            return (proc.returncode, "", "")
    except subprocess.CalledProcessError as e:
        print(f"[错误] Git 命令执行失败: {' '.join(args)}")
        print(f"[错误] 返回码: {e.returncode}")
        if capture_output:
            print(f"[错误] 输出: {e.output}")
        raise
    except FileNotFoundError:
        print("[错误] 未找到 git 命令，请确保 Git 已安装并添加到 PATH")
        sys.exit(1)

def setup_git_repo():
    """设置 Git 仓库"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 检查密钥文件
    if not os.path.isfile(KEY_FILE):
        print(f"[错误] 密钥文件 '{KEY_FILE}' 不存在，请创建并写入 GitHub Token")
        sys.exit(1)
    
    with open(KEY_FILE, 'r') as f:
        TOKEN = f.read().strip()
    
    # 构建认证 URL
    if not REMOTE_REPO.startswith("https://"):
        print("[错误] 只支持 https 协议的仓库地址")
        sys.exit(1)
    REPO_PATH = REMOTE_REPO[8:]
    AUTH_URL = f"https://{GIT_USERNAME}:{TOKEN}@{REPO_PATH}"
    
    # 初始化仓库（如果不存在）
    if not os.path.isdir(".git"):
        print("[信息] 初始化 Git 仓库")
        run_git(["init"])
        run_git(["config", "user.name", "wxhwwla"])
        run_git(["config", "user.email", "wxhwwla@users.noreply.github.com"])
    
    # 确保当前分支是 main
    _, current_branch, _ = run_git(["branch", "--show-current"], capture_output=True)
    current_branch = current_branch.strip()
    if current_branch != "main":
        print(f"[信息] 当前分支是 '{current_branch}'，切换到 main")
        returncode, _, _ = run_git(["checkout", "main"], check=False, capture_output=True)
        if returncode != 0:
            print("[信息] main 分支不存在，创建新分支")
            run_git(["checkout", "-b", "main"])
    
    # 设置远程地址
    _, stdout, _ = run_git(["remote", "-v"], capture_output=True)
    if "origin" not in stdout:
        print("[信息] 添加远程仓库 origin")
        run_git(["remote", "add", "origin", AUTH_URL])
    else:
        # 更新远程地址
        run_git(["remote", "set-url", "origin", AUTH_URL])
    
    return AUTH_URL

def force_pull():
    """强制拉取远程代码并覆盖本地所有更改"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("[信息] 开始强制拉取远程代码...")
    
    # 设置 Git 不进行交互式操作
    run_git(["config", "--local", "core.askpass", "false"], check=False, capture_output=True)
    
    # 检查工作区是否有未提交的更改
    returncode, stdout, _ = run_git(["status", "--porcelain"], check=False, capture_output=True)
    has_local_changes = bool(stdout.strip())
    
    if has_local_changes:
        print("[警告] 检测到本地有未提交的更改")
        print("[信息] 将强制覆盖所有本地更改，包括未提交的内容")
        
        # 强制重置索引和工作区（丢弃所有本地更改）
        print("[信息] 重置索引和工作区...")
        returncode, stdout, stderr = run_git(["reset", "--hard", "-q", "HEAD"], check=False, capture_output=True)
        if returncode != 0:
            print(f"[警告] 重置失败: {stderr.strip()}")
            print("[信息] 尝试跳过重置直接拉取...")
    
    # 清理未跟踪的文件和目录（使用 -q 避免交互式提示）
    print("[信息] 清理未跟踪的文件...")
    returncode, stdout, stderr = run_git(["clean", "-fdq"], check=False, capture_output=True)
    if returncode != 0:
        print(f"[警告] 清理失败: {stderr.strip()}")
    
    # 强制拉取远程代码，覆盖本地
    print("[信息] 强制拉取远程 main 分支...")
    try:
        run_git(["pull", "--force", "--rebase=false", "origin", "main"])
        print("[成功] 强制拉取完成！")
        return True
    except subprocess.CalledProcessError as e:
        print("[错误] 强制拉取失败")
        print("[提示] 可能的原因:")
        print("  1. 远程仓库不存在或无权限访问")
        print("  2. 权限不足，请检查 Token 是否正确")
        print("  3. 网络问题")
        print("  4. 某些文件正在被其他程序使用（如 IDE），请关闭后重试")
        return False

def main():
    print("="*60)
    print("GitHub 强制拉取脚本")
    print("="*60)
    
    try:
        # 设置仓库
        setup_git_repo()
        
        # 强制拉取
        if not force_pull():
            return
        
        print("="*60)
        print("[完成] 已成功从远程仓库拉取并覆盖本地代码！")
        print("[警告] 所有本地未提交的更改已被丢弃")
        print("="*60)
        
    except Exception as e:
        print(f"\n[错误] 操作失败: {e}")
        print("[提示] 请检查错误信息并手动解决问题")
        sys.exit(1)

if __name__ == "__main__":
    main()
