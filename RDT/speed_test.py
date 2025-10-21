# speed_test.py
"""
Speed Test Module
Runs an internet speed test using the speedtest-cli API
"""
import speedtest

def run_speed_test():
    """
    Returns dict with 'download' and 'upload' speeds in Mbps
    """
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # to Mbps
        upload = st.upload() / 1_000_000
        return {'download': round(download, 2), 'upload': round(upload, 2)}
    except Exception:
        return {'download': 0.0, 'upload': 0.0}
