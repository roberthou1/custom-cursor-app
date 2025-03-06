
import os
import sys
import importlib.util

# Add the application directory to sys.path
if getattr(sys, 'frozen', False):
    # We are running in a bundle
    bundle_dir = os.path.dirname(sys.executable)
    # Add bundle directory to path
    if bundle_dir not in sys.path:
        sys.path.insert(0, bundle_dir)
    # Add Resources directory to path (for macOS)
    resources_dir = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
    if os.path.exists(resources_dir) and resources_dir not in sys.path:
        sys.path.insert(0, resources_dir)
