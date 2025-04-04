#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk  # 确保导入 tkinter
from tkinter import scrolledtext
import os
import subprocess
from pathlib import Path
import datetime

# --- 配置 ---
COMMAND_PHRASE = "在桌面新建文档"
DEFAULT_FILENAME_BASE = "新建文档"
DEFAULT_EXTENSION = ".txt"
# --- 在下面两行中选择一个作为 LOGO 文字，注释掉另一个 ---
LOGO_TEXT = "天算AI"
# LOGO_TEXT = "Natural Algorithm"
# --- 配置结束 ---

def get_desktop_path():
    """使用 xdg-user-dir 获取用户桌面路径，更可靠"""
    try:
        command = ["xdg-user-dir", "DESKTOP"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        desktop_path = result.stdout.strip()
        if desktop_path and os.path.isdir(desktop_path):
            return Path(desktop_path)
        else:
            # Fallback to common defaults if xdg-user-dir fails or returns invalid path
            fallback_path_zh = Path.home() / "桌面"
            fallback_path_en = Path.home() / "Desktop"
            if fallback_path_zh.is_dir():
                return fallback_path_zh
            elif fallback_path_en.is_dir():
                return fallback_path_en
            else:
                 print("错误：无法自动检测桌面路径。")
                 return None # Could not find Desktop
    except (FileNotFoundError, subprocess.CalledProcessError, Exception) as e:
        print(f"获取桌面路径时出错: {e}")
        # Fallback if xdg-user-dir is not found or errors out
        fallback_path_zh = Path.home() / "桌面"
        fallback_path_en = Path.home() / "Desktop"
        if fallback_path_zh.is_dir():
            return fallback_path_zh
        elif fallback_path_en.is_dir():
            return fallback_path_en
        else:
            print("错误：无法自动检测桌面路径。")
            return None # Could not find Desktop

def find_unique_filename(directory, base, ext):
    """查找一个不重复的文件名，例如 新建文档.txt, 新建文档 (1).txt"""
    counter = 0
    while True:
        if counter == 0:
            filename = f"{base}{ext}"
        else:
            filename = f"{base} ({counter}){ext}"

        filepath = directory / filename
        if not filepath.exists():
            return filepath
        counter += 1

def create_file_on_desktop():
    """在桌面上创建文件"""
    desktop = get_desktop_path()
    if not desktop or not desktop.is_dir():
        log_message("错误：无法找到桌面文件夹。")
        return

    try:
        target_filepath = find_unique_filename(desktop, DEFAULT_FILENAME_BASE, DEFAULT_EXTENSION)

        # 创建空文件
        target_filepath.touch()

        log_message(f"成功：已在桌面创建文件 '{target_filepath.name}'")

    except OSError as e:
        log_message(f"错误：创建文件时出错 - {e}")
    except Exception as e:
        log_message(f"未知错误：{e}")

def log_message(message):
    """在文本区域显示消息"""
    now = datetime.datetime.now().strftime("%H:%M:%S")
    output_area.configure(state='normal') # 允许编辑以插入文本
    output_area.insert(tk.END, f"[{now}] {message}\n")
    output_area.configure(state='disabled') # 禁止用户编辑
    output_area.see(tk.END) # 滚动到底部

def process_input(event=None): # event=None 允许按钮点击调用
    """处理输入框中的命令"""
    user_input = entry_input.get().strip()
    log_message(f"你输入了: {user_input}") # 显示用户输入

    if user_input == COMMAND_PHRASE:
        create_file_on_desktop()
    elif user_input: # 如果输入了但不是指定命令
        log_message("无法识别的命令。请输入 '在桌面新建文档'")
    else: # 如果没输入
         log_message("请输入命令。")

    entry_input.delete(0, tk.END) # 清空输入框

# --- GUI 设置 ---
root = tk.Tk()
root.title("桌面文件创建工具")
root.geometry("450x350") # 调整窗口高度以适应Logo

# --- 添加 Logo 标签 ---
try:
    # 尝试使用稍好或系统中可能存在的字体
    logo_font = ("Arial", 14, "bold")
    # 可以尝试其他字体，例如:
    # logo_font = ("WenQuanYi Micro Hei", 14, "bold")
    # logo_font = ("Noto Sans CJK SC", 14, "bold")
except tk.TclError:
    # 如果指定字体不存在，使用默认字体
    logo_font = ("TkDefaultFont", 14, "bold")

logo_label = tk.Label(root, text=LOGO_TEXT, font=logo_font)
# pady=(上边距, 下边距) 设置 Logo 上下的间距
logo_label.pack(pady=(10, 5))
# --- Logo 标签添加结束 ---


# 输出区域 (类似聊天记录)
output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=10)
# pady=(上边距, 下边距)，调整上边距为0，因为Logo已有下边距
output_area.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)

# 输入框框架
input_frame = tk.Frame(root)
input_frame.pack(pady=5, padx=10, fill=tk.X)

# 输入框
entry_input = tk.Entry(input_frame, width=40)
entry_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
entry_input.bind("<Return>", process_input) # 绑定回车键

# 执行按钮
button_execute = tk.Button(input_frame, text="执行", command=process_input)
button_execute.pack(side=tk.RIGHT)

# 初始提示
log_message("工具已启动。请输入 '在桌面新建文档' 并按回车或点击'执行'按钮。")

# 启动 GUI 主循环
root.mainloop()