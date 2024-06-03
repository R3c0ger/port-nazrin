import argparse
import socket
import sys
import threading
import csv
import concurrent
from concurrent.futures import ThreadPoolExecutor


def scanport(host, port, results, lock):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(8)
            result = sock.connect_ex((host, port))
            if result == 0:
                with lock:
                    results[port] = {"status": "OPEN"}
    except socket.error as e:
        with lock:
            results[port] = {"status": f"错误: {str(e)}"}


def showreport(results):
    print("\n扫描报告:")
    if not results.items():
        print("无开放端口")
        return
    for port, status in sorted(results.items()):
        print(f"端口 {port}: {status['status']}")


def writecsv(results, filepath="scan_results.csv"):
    if not results.items():
        print("无开放端口")
        return
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['port', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for port, status in sorted(results.items()):
            writer.writerow({'port': port, 'status': status['status']})
    print(f"\n扫描结果已经存到 {filepath}")


def scanall(host, max_workers=800):
    results = {}
    lock = threading.Lock()

    def worker(port):
        print(f"扫描 {port}...")
        scanport(host, port, results, lock)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker, port) for port in range(1, 65536)}
        for future in concurrent.futures.as_completed(futures):
            pass

    return results


def scanports(host, ports, max_workers=100):
    results = {}
    lock = threading.Lock()

    def worker(port):
        print(f"扫描 {port}...")
        scanport(host, port, results, lock)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, port) for port in ports]
        for future in concurrent.futures.as_completed(futures):
            pass

    return results


def main():
    parser = argparse.ArgumentParser(description="简单的端口扫描器")
    parser.add_argument("host", help="需要扫描的ip")
    parser.add_argument("--all", action="store_true", help="扫描从1-65535的所有端口")
    parser.add_argument("-p", "--port", metavar="PORT", nargs="+", type=int, help="指定待扫描的端口号")
    parser.add_argument("--report", choices=["text", "csv"], help="指定扫描报告的格式：直接打印或保存为csv文件")
    args = parser.parse_args()

    host = args.host
    if args.all:
        print(f"扫描 {host}上所有端口...")
        results = scanall(host)
    elif args.port:
        print(f"扫描 {host}上的指定端口...")
        results = scanports(host, args.port)
    else:
        parser.print_help()
        sys.exit(1)

    # 根据用户选择输出报告
    if args.report == "text" or not args.report:
        showreport(results)
    elif args.report == "csv":
        writecsv(results)
    if args.report:
        print("报告已经生成")


if __name__ == "__main__":
    main()