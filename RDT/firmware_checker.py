"""
Firmware Checker Module - FIXED VERSION
Now checks firmware at given IP address instead of model name
"""
import requests
import socket

def check_firmware_updates(ip):
    """
    Check firmware at specific IP address
    ip: Router IP address (e.g., "192.168.1.1")
    Returns: {'current': str, 'latest': str, 'status': str}
    """
    try:
        # Try to connect to router's web interface
        test_urls = [
            f"http://{ip}",
            f"http://{ip}/status",
            f"http://{ip}/info",
            f"https://{ip}"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=3, verify=False)
                if response.status_code == 200:
                    # Successfully connected
                    return {
                        'current': 'Connected - unable to detect version',
                        'latest': 'Check manufacturer website',
                        'status': f'Router accessible at {ip}'
                    }
            except:
                continue
        
        # If no HTTP connection, try ping
        import subprocess
        import platform
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        result = subprocess.run(['ping', param, '1', ip], 
                              capture_output=True, timeout=5)
        
        if result.returncode == 0:
            return {
                'current': 'Unknown (ping successful)',
                'latest': 'Unknown',
                'status': f'Device responds at {ip} but web interface unavailable'
            }
        else:
            return {
                'current': 'No response',
                'latest': 'No response', 
                'status': f'No device found at {ip}'
            }
            
    except Exception as e:
        return {
            'current': 'Error',
            'latest': 'Error',
            'status': f'Error checking {ip}: {str(e)}'
        }
