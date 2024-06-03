#!usr/bin/env python3
# -*- coding: utf-8 -*-
# Path: src/scanner.py

import socket
import threading
from queue import Queue

from config import LOGGER
from i18n import MSG


class PortScanner:
    def __init__(self, ip_list, port_list, workers):
        self.ip_list = ip_list
        self.port_list = port_list
        self.workers = workers
        self.queue = Queue()
        self.lock = threading.Lock()

    def scan(self, ip, port):
        """
        扫描指定IP和端口
        :param ip: 目标IP地址
        :param port: 目标端口
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, int(port)))
            with self.lock:
                if result == 0:
                    LOGGER.info(f"IP：{ip}，端口：{port} 开放")
                else:
                    LOGGER.info(f"IP：{ip}，端口：{port} 关闭")
            sock.close()
        except Exception as e:
            LOGGER.error(f"扫描IP：{ip}、端口：{port} 时出错：\n{e}")

    def worker(self):
        """扫描工作线程，从队列中获取IP和端口并扫描"""
        while not self.queue.empty():
            ip, port = self.queue.get()
            self.scan(ip, port)
            self.queue.task_done()

    def run(self):
        """运行端口扫描"""
        # 将所有IP和端口组合添加到队列中
        for ip in self.ip_list:
            for port in self.port_list:
                self.queue.put((ip, port))

        # 开启工作线程
        threads = []
        for _ in range(self.workers):
            thread = threading.Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        self.queue.join()
        for thread in threads:
            thread.join()

        LOGGER.info(MSG['finish'])
