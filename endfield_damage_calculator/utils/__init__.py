"""工具模块

提供通用的工具函数，支持应用程序路径处理、文件操作等功能。

导出的函数：
- get_app_dir: 获取应用程序根目录
- get_resource_path: 获取资源文件的完整路径
"""

from .path_utils import get_app_dir, get_resource_path

__all__ = ["get_app_dir", "get_resource_path"]
