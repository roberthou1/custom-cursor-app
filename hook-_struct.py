# Custom hook for the _struct module
from PyInstaller.utils.hooks import collect_dynamic_libs

# This will collect all dynamic libraries related to _struct
datas = []
binaries = collect_dynamic_libs('_struct')

# Add the specific _struct module path
struct_path = "/opt/homebrew/Cellar/python@3.13/3.13.2/Frameworks/Python.framework/Versions/3.13/lib/python3.13/lib-dynload/_struct.cpython-313-darwin.so"
binaries.append((struct_path, '.'))
