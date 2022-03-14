# -*- coding: utf-8 -*-


def portScan(host):
    import nmap
    nm = nmap.PortScanner()
    nm.scan(host, ports=None, arguments="-sS -sV")
    print(nm.command_line())
    print(nm.scanninfo())


if __name__ =="__main__":
    portScan("192.168.105.1")