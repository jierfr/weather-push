#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git自动安装脚本
"""

import os
import subprocess
import sys
import urllib.request
import io

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def download_git():
    """下载Git安装程序"""
    git_url = "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/Git-2.45.0-64-bit.exe"
    download_path = os.path.expanduser("~/Downloads/Git-2.45.0-64-bit.exe")
    
    print(f"正在下载Git安装程序到：{download_path}")
    print("这可能需要几分钟，请耐心等待...")
    
    try:
        urllib.request.urlretrieve(git_url, download_path)
        print(f"✅ 下载完成：{download_path}")
        return download_path
    except Exception as e:
        print(f"❌ 下载失败：{str(e)}")
        print("\n请手动下载：")
        print("1. 访问：https://git-scm.com/download/win")
        print("2. 点击下载链接")
        print("3. 运行下载的安装程序")
        return None

def install_git(installer_path):
    """静默安装Git"""
    if not installer_path or not os.path.exists(installer_path):
        print("❌ 安装程序不存在")
        return False
    
    print("\n正在安装Git...")
    print("安装过程中会弹出窗口，请允许运行")
    
    try:
        # 静默安装参数
        cmd = [
            installer_path,
            "/VERYSILENT",
            "/NORESTART",
            "/NOCANCEL",
            "/SP-",
            "/CLOSEAPPLICATIONS",
            "/RESTARTAPPLICATIONS"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Git安装完成")
            print("\n请重新打开PowerShell窗口，然后运行：")
            print("git --version")
            return True
        else:
            print(f"❌ 安装失败：{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 安装异常：{str(e)}")
        return False

def main():
    print("=" * 50)
    print("Git自动安装工具")
    print("=" * 50)
    
    # 下载Git
    installer_path = download_git()
    
    if installer_path:
        # 安装Git
        install_git(installer_path)
    
    print("\n安装完成！")

if __name__ == "__main__":
    main()
