from cx_Freeze import setup, Executable

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [Executable("ui\mine1.py", base=base)]
additional_mods = ['numpy.core._methods', 'numpy.lib.format','pyqtgraph.debug','pyqtgraph.ThreadsafeTimer']

packages = ["idna"]
options = {
    'build_exe': {

        'packages':packages,
        'includes': additional_mods
    },

}

setup(
    name = "AppVpn",
    options = options,
    version = "0.1",
    description = 'VPN Management App',
    executables = executables
)