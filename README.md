# PortNazrin

A simple port scanner using python for educational purposes.

## Installation

```bash
git clone
cd PortNazrin
pip install -r requirements.txt
pyinstaller -F src/main.py -n PortNazrin -p src/
```

## Environment

- Python 3.6+
- art~=6.2
- colorama~=0.4.6
- qlogging~=1.3.1
- pyinstaller~=6.7.0

## Usage

查看帮助：
```bash
PortNazrin -h
```

```bash
usage: PortNazrin [-h] [-i IP [IP ...]] [-p PORT [PORT ...]] [-I IMPORT_IP] [-P IMPORT_PORT] [--all] [-w [1-1000]] [-v]
optional arguments:
  -h, --help            show this help message and exit
  -i IP [IP ...], --ip IP [IP ...]
                        目标主机的IP地址。 如“192.168.1.1”、“10.1.1.2,10.1.1.3“或“10.1.2.1-254”
  -p PORT [PORT ...], --port PORT [PORT ...]
                        待扫描的端口。 如“80”、“135,445”或“1-65535”
  -I IMPORT_IP, --import-ip IMPORT_IP
                        导入IP地址列表文件
  -P IMPORT_PORT, --import-port IMPORT_PORT
                        导入端口列表文件
  --all                 扫描所有端口
  -w [1-1000], --workers [1-1000]
                        并发扫描的最大工作线程数
  -v, --version         显示版本信息
```