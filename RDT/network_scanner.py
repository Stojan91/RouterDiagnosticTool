# network_scanner.py
"""
Network Scanner Module
Scans local LAN for active devices using ARP ping sweep.
"""
import subprocess
import platform
import re
from concurrent.futures import ThreadPoolExecutor
import socket

def ping(ip):
    param = '-n' if platform.system().lower()=='windows' else '-c'
    command = ['ping', param, '1', '-w', '1000', ip]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL)
        return result.returncode==0
    except:
        return False

def get_mac(ip):
    try:
        pid = subprocess.Popen(['arp', '-n', ip], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        data = pid.communicate()[0].decode()
        m = re.search(r'([0-9a-fA-F]{2}(?:[:-][0-9a-fA-F]{2}){5})', data)
        return m.group(1) if m else ''
    except:
        return ''

def scan_network():
    """
    Returns list of devices on local subnet. Each: {ip, mac, hostname, manufacturer}
    """
    # Detect local IP and subnet
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    parts = local_ip.split('.')
    base = '.'.join(parts[0:3])
    ips = [f"{base}.{i}" for i in range(1,255)]
    devices = []
    
    def check(ip):
        if ping(ip):
            mac = get_mac(ip)
            try:
                hn = socket.gethostbyaddr(ip)[0]
            except:
                hn = ''
            manufacturer = mac.split(':')[0] if mac else ''
            devices.append({'ip': ip, 'mac': mac, 'hostname': hn, 'manufacturer': manufacturer})
    
    with ThreadPoolExecutor(max_workers=100) as exe:
        exe.map(check, ips)
    
    return devices
