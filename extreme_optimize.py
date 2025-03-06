#!/usr/bin/env python3
"""
Extreme Size Optimization Script for Custom Cursor App
This script builds the app with the most aggressive size optimizations possible.
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path
import platform

def create_minimal_venv():
    """Create a minimal virtual environment with only required packages"""
    print("Creating minimal virtual environment...")
    
    # Remove existing venv if it exists
    venv_path = Path("minimal_venv")
    if venv_path.exists():
        shutil.rmtree(venv_path)
    
    # Create new venv
    subprocess.run([sys.executable, "-m", "venv", "minimal_venv"], check=True)
    
    # Determine pip path
    if platform.system() == "Windows":
        pip_path = "minimal_venv\\Scripts\\pip"
    else:
        pip_path = "minimal_venv/bin/pip"
    
    # Upgrade pip
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    
    # Install only the absolutely required packages
    required_packages = ["PyQt6==6.5.0", "pillow==9.5.0", "pyinstaller==6.12.0"]
    
    # Add platform-specific packages
    if platform.system() == "Windows":
        required_packages.append("pywin32==306")
    elif platform.system() == "Darwin":
        required_packages.append("pyobjc-framework-Cocoa==9.0")
    
    # Install packages
    subprocess.run([pip_path, "install"] + required_packages, check=True)
    
    print("Minimal virtual environment created successfully")
    return venv_path

def build_app(venv_path):
    """Build the app with extreme size optimizations"""
    print("Building app with extreme size optimizations...")
    
    # Determine Python and PyInstaller paths
    if platform.system() == "Windows":
        python_path = f"{venv_path}\\Scripts\\python"
        pyinstaller_path = f"{venv_path}\\Scripts\\pyinstaller"
    else:
        python_path = f"{venv_path}/bin/python"
        pyinstaller_path = f"{venv_path}/bin/pyinstaller"
    
    # Basic PyInstaller command
    build_cmd = [
        pyinstaller_path,
        "--clean",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--noconsole",
        "--strip",
    ]
    
    # Extreme exclusions - exclude everything not absolutely needed
    exclusions = [
        "--exclude-module=tkinter",
        "--exclude-module=matplotlib",
        "--exclude-module=numpy",
        "--exclude-module=scipy",
        "--exclude-module=pandas",
        "--exclude-module=cryptography",
        "--exclude-module=PySide6",
        "--exclude-module=PyQt5",
        "--exclude-module=wx",
        "--exclude-module=PIL.ImageQt",
        "--exclude-module=PIL.ImageTk",
        "--exclude-module=PyQt6.QtNetwork",
        "--exclude-module=PyQt6.QtSql",
        "--exclude-module=PyQt6.QtMultimedia",
        "--exclude-module=PyQt6.QtQml",
        "--exclude-module=PyQt6.QtWebEngineCore",
        "--exclude-module=PyQt6.QtWebEngineWidgets",
        "--exclude-module=PyQt6.QtXml",
        "--exclude-module=email",
        "--exclude-module=html",
        "--exclude-module=http",
        "--exclude-module=logging",
        "--exclude-module=multiprocessing",
        "--exclude-module=unittest",
        "--exclude-module=xml",
        "--exclude-module=xmlrpc",
        "--exclude-module=pydoc",
        "--exclude-module=asyncio",
        "--exclude-module=concurrent",
        "--exclude-module=ctypes",
        "--exclude-module=curses",
        "--exclude-module=dbm",
        "--exclude-module=distutils",
        "--exclude-module=ensurepip",
        "--exclude-module=idlelib",
        "--exclude-module=lib2to3",
        "--exclude-module=pkg_resources",
        "--exclude-module=setuptools",
        "--exclude-module=sqlite3",
        "--exclude-module=test",
        "--exclude-module=turtledemo",
        "--exclude-module=venv",
        "--exclude-module=wheel",
    ]
    
    # Only include what we absolutely need
    inclusions = [
        "--hidden-import=PIL.Image",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
    ]
    
    # Add platform-specific hidden imports
    if platform.system() == "Windows":
        inclusions.extend([
            "--hidden-import=win32api",
            "--hidden-import=win32con",
            "--hidden-import=win32gui",
            "--hidden-import=ctypes",
        ])
    elif platform.system() == "Darwin":
        inclusions.extend([
            "--hidden-import=Cocoa",
        ])
    
    # Add all options to build command
    build_cmd.extend(exclusions)
    build_cmd.extend(inclusions)
    
    # Add UPX compression if available
    try:
        upx_result = subprocess.run(["which", "upx"], capture_output=True, text=True)
        if upx_result.returncode == 0:
            upx_path = upx_result.stdout.strip()
            build_cmd.extend(["--upx-dir", os.path.dirname(upx_path)])
    except Exception:
        print("UPX not found, continuing without UPX compression")
    
    # Add name and icon
    build_cmd.extend([
        "--name", "CustomCursorApp",
        "--icon", "icons/icon.icns",
    ])
    
    # Add data files - only include what's absolutely necessary
    build_cmd.extend(["--add-data", "README.md:."])
    
    # Platform-specific options
    if platform.system() == "Darwin":  # macOS
        # Only include the absolute minimum Qt libraries
        build_cmd.extend([
            # Only essential Qt core libraries
            "--add-binary", f"{venv_path}/lib/python*/site-packages/PyQt6/Qt6/lib/QtCore.framework/Versions/A/QtCore:PyQt6/Qt6/lib/QtCore.framework/Versions/A/",
            "--add-binary", f"{venv_path}/lib/python*/site-packages/PyQt6/Qt6/lib/QtGui.framework/Versions/A/QtGui:PyQt6/Qt6/lib/QtGui.framework/Versions/A/",
            "--add-binary", f"{venv_path}/lib/python*/site-packages/PyQt6/Qt6/lib/QtWidgets.framework/Versions/A/QtWidgets:PyQt6/Qt6/lib/QtWidgets.framework/Versions/A/",
            
            # Only the essential platform plugin
            "--add-binary", f"{venv_path}/lib/python*/site-packages/PyQt6/Qt6/plugins/platforms/libqcocoa.dylib:PyQt6/Qt6/plugins/platforms/",
            
            # Bundle identifier
            "--osx-bundle-identifier", "com.customcursor.app",
        ])
    
    # Add main script
    build_cmd.append("src/main.py")
    
    # Run PyInstaller
    print(f"Running: {' '.join(build_cmd)}")
    subprocess.run(build_cmd, check=True)
    
    # Apply additional optimizations
    optimize_output()

def optimize_output():
    """Apply additional optimizations to the output files"""
    print("\nApplying extreme post-build optimizations...")
    
    if platform.system() == "Darwin":  # macOS
        try:
            # Strip the executable
            subprocess.run(["strip", "dist/CustomCursorApp"], check=False)
            
            # Apply UPX with maximum compression
            try:
                upx_result = subprocess.run(["which", "upx"], capture_output=True, text=True)
                if upx_result.returncode == 0:
                    upx_path = upx_result.stdout.strip()
                    print("Applying maximum UPX compression...")
                    subprocess.run([upx_path, "--best", "--ultra-brute", "--force-macos", "dist/CustomCursorApp"], check=False)
            except Exception as e:
                print(f"Warning: UPX compression failed: {e}")
            
            # Create highly compressed DMG
            create_compressed_dmg()
            
        except Exception as e:
            print(f"Warning: Post-build optimization failed: {e}")

def create_compressed_dmg():
    """Create a highly compressed DMG file"""
    print("\nCreating extremely compressed DMG file...")
    
    # First try with maximum compression using UDBZ format (bzip2)
    try:
        # Create a temporary directory for DMG contents
        dmg_contents = Path("dist/dmg_contents")
        dmg_contents.mkdir(exist_ok=True)
        
        # Copy the app to the temporary directory
        if Path("dist/CustomCursorApp.app").exists():
            shutil.copytree("dist/CustomCursorApp.app", dmg_contents / "CustomCursorApp.app", symlinks=True)
        else:
            # For onefile mode, create an Applications symlink and copy the executable
            os.symlink("/Applications", dmg_contents / "Applications")
            shutil.copy2("dist/CustomCursorApp", dmg_contents / "CustomCursorApp")
        
        # Create the DMG with maximum compression
        subprocess.run([
            "hdiutil", "create",
            "-volname", "Custom Cursor App",
            "-srcfolder", str(dmg_contents),
            "-ov", "-format", "UDBZ",  # Use bzip2 compression (best compression)
            "dist/CustomCursorApp-Tiny.dmg"
        ], check=True)
        
        # Report the size
        dmg_size = os.path.getsize("dist/CustomCursorApp-Tiny.dmg") / (1024 * 1024)  # Convert to MB
        print(f"Extremely compressed DMG created: dist/CustomCursorApp-Tiny.dmg ({dmg_size:.2f} MB)")
        
        # Clean up temporary directory
        shutil.rmtree(dmg_contents)
        
    except Exception as e:
        print(f"Warning: Could not create compressed DMG: {e}")

def main():
    parser = argparse.ArgumentParser(description="Build Custom Cursor App with extreme size optimizations")
    parser.add_argument("--skip-venv", action="store_true", help="Skip creating a new virtual environment")
    args = parser.parse_args()
    
    # Create minimal virtual environment
    if not args.skip_venv:
        venv_path = create_minimal_venv()
    else:
        venv_path = Path("minimal_venv")
        if not venv_path.exists():
            print("Error: minimal_venv does not exist. Run without --skip-venv first.")
            sys.exit(1)
    
    # Build the app
    build_app(venv_path)
    
    print("\nExtreme optimization completed!")
    print("Check the dist directory for the optimized app and DMG file.")

if __name__ == "__main__":
    main()
