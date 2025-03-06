# Custom hook for the struct module
from PyInstaller.utils.hooks import collect_submodules

# Collect all submodules of struct
hiddenimports = collect_submodules('struct')

# Explicitly add _struct
hiddenimports.append('_struct')
