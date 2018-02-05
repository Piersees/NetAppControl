from cx_Freeze import setup, Executable

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [Executable("mine1.py", base=base)]
additional_mods = ['numpy.core._methods', 'numpy.lib.format','pyqtgraph.debug','pyqtgraph.ThreadsafeTimer','win32pipe', 'win32file', 'win32con','speedtest','requests',
                   "nmap","scapy","scapy.all"]
#include_file = ["Network/inject.py","Network/SpeedTestFunctions.py","Network/External_IP.py","Network/ping.py","Network/NetworkScan.py",
#                "Network/Wifi_stat.py","Network/Wireshark.py","Network/openvpn.py","Network/Stats.py","Network/BandWidth.py",
#                "Network/Interfaces.py"]
include_file = ["Network/","ui/","data/","images/"]
packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
        'includes': additional_mods,
        'include_files': include_file
    },

}

setup(
    name = "AppVpn",
    options = options,
    version = "0.1",
    description = 'VPN Management App',
    executables = executables
)