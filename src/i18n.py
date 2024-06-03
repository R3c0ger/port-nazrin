#!usr/bin/env python3
# -*- coding: utf-8 -*-
# Path: src/i18n.py

# 警告与错误信息的前缀
WARN = f"[Warning] "
ERROR = f"[Error] "


MSG = {
    # main.py
    'usage': "usage: PortNazrin [-h] [-i IP [IP ...]] [-p PORT [PORT ...]] [-I IMPORT_IP] [-P IMPORT_PORT] [--all] [-w [1-1000]] [-v]",
    'wait_input': "等待用户输入参数：",
    # 帮助内容
    'description': " - 简单的端口扫描器",
    'ip_help': "目标主机的IP地址。\n如“192.168.1.1”、“10.1.1.2,10.1.1.3“或“10.1.2.1-254”",
    'port_help': "待扫描的端口。\n如“80”、“135,445”或“1-65535”",
    'all_help': "扫描所有端口",
    'workers_help': "并发扫描的最大工作线程数",
    'output_help': "输出到文件",
    'version_help': "显示版本信息",
    'import-ip_help': "导入IP地址列表文件",
    'import-port_help': "导入端口列表文件",
    # main
    'error_ip': f"{ERROR}请指定目标主机的IP地址，或导入IP地址列表文件",
    'error_port': f"{ERROR}请指定待扫描的端口，或导入端口列表文件",
    # utils
    'error_ip_format': f"{ERROR}错误的IP地址：",
    'error_ip_exist': f"{ERROR}存在错误的IP地址或列表文件地址，请检查输入参数。是否继续使用其他正确的IP地址？[Y/n]: ",
    'error_iplist_nofound': f"{ERROR}未找到导入的IP地址列表文件：",
    'error_no_ip': f"{ERROR}未找到IP地址，请检查输入的IP地址与导入的文件。程序即将退出...",
    'error_port_format': f"{ERROR}错误的端口：",
    'error_port_exist': f"{ERROR}存在错误的端口或列表文件地址，请检查输入参数。是否继续使用其他正确的端口？[Y/n]: ",
    'error_portlist_nofound': f"{ERROR}未找到导入的端口列表文件：",
    'error_no_port': f"{ERROR}未找到端口，请检查输入的端口与导入的文件。程序即将退出...",
    # scanner
    'finish': f"扫描完成。",
}
