#!usr/bin/env python3
# -*- coding: utf-8 -*-
# Path: src/main.py

import argparse
import os
import signal
import sys

from config import VERSION, TITLE, LOGGER
from i18n import MSG
from scanner import PortScanner
from utils import ascii_banner, extract_ip, extract_port


def argparser():
    """
    命令行参数解析
    :return: 命令行参数
    """
    parser = argparse.ArgumentParser(description=f"{TITLE}" + MSG['description'], prog=f"{TITLE}")
    parser.add_argument("-i", "--ip", help=MSG['ip_help'], action="extend", nargs="+", type=str)
    parser.add_argument("-p", "--port", help=MSG['port_help'], action="extend", nargs="+", type=str)
    # 导入ip地址列表文件、导入端口列表文件
    parser.add_argument("-I", "--import-ip", help=MSG['import-ip_help'])
    parser.add_argument("-P", "--import-port", help=MSG['import-port_help'])
    parser.add_argument("--all", help=MSG['all_help'], action="store_true")
    parser.add_argument(
        "-w", "--workers", help=MSG['workers_help'],
        type=int, default=1, choices=range(1, 1001), metavar="[1-1000]"
    )
    # TODO: 支持协议
    # parser.add_argument("-t", "--tcp", help="TCP协议", action="store_true")
    # parser.add_argument("-u", "--udp", help="UDP协议", action="store_true")
    # TODO: 扫描速度控制
    # parser.add_argument("-s", "--speed", help="扫描速度", type=int, default=1, choices=range(1, 6))
    parser.add_argument("-v", "--version", help=MSG['version_help'], action="store_true")
    args = parser.parse_args()
    # 春之岸边播放器正在播放曲目：
    LOGGER.debug(f"\n{args}\n")
    return args


def main():
    args = argparser()

    # 版本信息
    if args.version:
        print(f"{TITLE} - {VERSION}")
        sys.exit(0)

    # 检查IP地址的参数值是否为空
    if not args.ip and not args.import_ip:
        LOGGER.error(MSG['error_ip'])
        sys.exit(1)
    # 提取IP地址
    ip_list = extract_ip(args.ip, args.import_ip)
    # 去重，排序
    ip_list = list(set(ip_list))

    if not args.all:
        # 检查端口的参数值是否为空
        if not args.port and not args.import_port:
            LOGGER.error(MSG['error_port'])
            sys.exit(1)
        port_list = extract_port(args.port, args.import_port)
        port_list = list(set(port_list))
        port_list = sorted(port_list, key=lambda x: int(x))
    else:
        port_list = [str(i) for i in range(1, 65536)]

    LOGGER.debug(f"\nip_list: {ip_list}\nport_list: {port_list}")

    # 创建端口扫描器并运行
    scanner = PortScanner(ip_list, port_list, args.workers)
    scanner.run()


if __name__ == "__main__":
    ascii_banner()
    if len(sys.argv) == 1:
        print(f"{TITLE} - {VERSION}")
        print(MSG['usage'])
        # 等待用户输入参数
        print(MSG['wait_input'])
        args = input()
        sys.argv.extend(args.split())
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os.kill(os.getpid(), signal.SIGTERM)
