#!usr/bin/env python3
# -*- coding: utf-8 -*-
# Path: src/utils.py

import random
import re

from art import text2art
from colorama import Fore, init

from config import LOGGER
from i18n import MSG


def ascii_banner():
    """用于显示在程序运行开始的随机字符画"""
    init(autoreset=True)
    text = "PortNazrin"
    fonts = ["standard", "basic", "chunky", "cyberlarge",
             "doom", "epic", "isometric1", "isometric3",]
    font = random.choice(fonts)
    banner = text2art(text, font=font)
    print(Fore.CYAN + banner + Fore.RESET)


def read_file(file_path, msg):
    """
    读取文件内容
    :param file_path: 文件路径
    :param msg: 错误信息
    :return: 文件内容列表
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except FileNotFoundError:
        LOGGER.error(f"{msg}{file_path}")
        return []


def match_ip(ip_str):
    """
    匹配IP地址
    :param ip_str: IP地址字符串
    :return: 匹配结果
    """
    ip_pattern = re.compile(
        r'^(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'  # 第一段
        r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'  # 第二段
        r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.'  # 第三段
        r'(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$'  # 第四段
    )
    return ip_pattern.match(ip_str)


def extract_ip(arg_ip, arg_import_ip):
    """
    提取IP地址
    :param arg_ip: 命令行参数-i的IP地址
    :param arg_import_ip: 命令行参数中-I导入的IP列表文件地址
    :return: IP地址列表
    """
    exist_wrong_ip = False  # 使用一个flag来标志是否有错误的IP地址
    ip_list_init = []  # 参数输入和文件导入的IP地址列表，未经检查

    # 提取-i参数值中的IP地址，处理分隔符
    if arg_ip:
        for ip in arg_ip:
            ip_list_init.extend(re.split(r"[,，;；、]", ip))

    # 读取-I导入的IP地址列表文件
    if arg_import_ip:
        import_ip_list = read_file(arg_import_ip, MSG['error_iplist_nofound'])
        if not import_ip_list:
            exist_wrong_ip = True
        else:
            ip_list_init.extend(import_ip_list)
    LOGGER.debug(f"ip_list_init: {ip_list_init}")

    # 处理IP地址
    ip_list = []  # --ip 参数中的IP地址列表
    for ip_splited in ip_list_init:
        # 若不是范围就直接正则检查
        if "-" not in ip_splited:
            if match_ip(ip_splited):
                ip_list.append(ip_splited)
            else:
                LOGGER.error(f"{MSG['error_ip_format']}{ip_splited}")
                exist_wrong_ip = True
        # 处理IP地址范围
        else:
            ip_range = ip_splited.split("-")
            LOGGER.debug(f"ip_range: {ip_range}")
            # “-”左右只能有两个元素
            if len(ip_range) != 2:
                LOGGER.error(f"{MSG['error_ip_format']}{ip_splited}")
                exist_wrong_ip = True
                continue
            # 提取IP地址的前三段和第四段的范围
            ip_base_start, end_last_octet = ip_range
            base_ip = ".".join(ip_base_start.split(".")[:-1])
            start_last_octet = ip_base_start.split(".")[-1]
            # 正则检查
            if not match_ip(ip_base_start):
                LOGGER.error(f"{MSG['error_ip_format']}{ip_splited}")
                exist_wrong_ip = True
                continue
            # 尝试将第四段IP地址转换为整数
            try:
                start_last_octet = int(start_last_octet)
                end_last_octet = int(end_last_octet)
            except ValueError:
                LOGGER.error(f"{MSG['error_ip_format']}{ip_splited}")
                exist_wrong_ip = True
                continue
            # 若第四段IP地址不在0-255之间，则为错误的IP地址
            if not 0 <= start_last_octet <= 255 or not 0 <= end_last_octet <= 255:
                LOGGER.error(f"{MSG['error_ip_format']}{ip_splited}")
                exist_wrong_ip = True
                continue
            # 若第四段起始IP大于结束IP，则交换两者的值
            if start_last_octet > end_last_octet:
                start_last_octet, end_last_octet = end_last_octet, start_last_octet
            # 生成并添加IP地址列表
            for i in range(start_last_octet, end_last_octet + 1):
                ip_list.append(f"{base_ip}.{i}")

    LOGGER.debug(f"ip_list: {ip_list}")
    # 若没有正确的IP，则退出程序
    if not ip_list:
        LOGGER.error(MSG['error_no_ip'])
        exit(1)
    # 若有错误的IP地址，让用户选择是否使用已经检查为正确的IP地址
    if exist_wrong_ip:
        LOGGER.error(MSG['error_ip_exist'])
        choice = input()
        # 默认为继续
        if choice.lower() == "n":
            exit(1)
    return ip_list


def extract_port(arg_port, arg_import_port):
    """
    提取端口
    :param arg_port: 命令行参数-p的端口
    :param arg_import_port: 命令行参数中-P导入的端口列表文件地址
    :return: 端口列表
    """
    exist_wrong_port = False  # 使用一个flag来标志是否有错误的端口
    port_list_init = []  # 参数输入和文件导入的端口列表，未经检查

    # 提取-p参数值中的端口，处理分隔符
    if arg_port:
        for port in arg_port:
            port_list_init.extend(re.split(r"[,，;；、]", port))

    # 读取-P导入的端口列表文件
    if arg_import_port:
        import_port_list = read_file(arg_import_port, MSG['error_portlist_nofound'])
        if not import_port_list:
            exist_wrong_port = True
        else:
            port_list_init.extend(import_port_list)

    LOGGER.debug(f"port_list_init: {port_list_init}")

    # 处理端口
    port_list = []  # --port 参数中的端口列表
    for port_splited in port_list_init:
        # 若不是范围就直接正则检查
        if "-" not in port_splited:
            # 检查
            if port_splited.isdigit() and 0 < int(port_splited) <= 65535:
                port_list.append(port_splited)
            else:
                LOGGER.error(f"{MSG['error_port_format']}{port_splited}")
                exist_wrong_port = True
        # 处理端口范围
        else:
            port_range = port_splited.split("-")
            LOGGER.debug(f"port_range: {port_range}")
            # “-”左右只能有两个元素
            if len(port_range) != 2:
                LOGGER.error(f"{MSG['error_port_format']}{port_splited}")
                exist_wrong_port = True
                continue
            # 提取端口范围
            start_port, end_port = port_range
            # 正则检查
            if (not (start_port.isdigit() and 0 < int(start_port) <= 65535)
                    or not (end_port.isdigit() and 0 < int(end_port) <= 65535)):
                LOGGER.error(f"{MSG['error_port_format']}{port_splited}")
                exist_wrong_port = True
                continue
            # 若起始端口大于结束端口，则交换两者的值
            if start_port > end_port:
                start_port, end_port = end_port, start_port
            # 生成并添加端口列表
            for i in range(int(start_port), int(end_port) + 1):
                port_list.append(str(i))

    LOGGER.debug(f"port_list: {port_list}")
    # 若没有正确的端口，则退出程序
    if not port_list:
        LOGGER.error(MSG['error_no_port'])
        exit(1)
    # 若有错误的端口，让用户选择是否使用已经检查为正确的端口
    if exist_wrong_port:
        LOGGER.error(MSG['error_port_exist'])
        choice = input()
        # 默认为继续
        if choice.lower() == "n":
            exit(1)
    return port_list
