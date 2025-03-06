#!/usr/bin/env python3
"""
Build script for Custom Cursor App
Creates standalone executables for Windows or macOS
"""

import os
import sys
import platform
import subprocess
import shutil
import argparse
from pathlib import Path

def create_default_icon():
    """Create a default icon for the application if none exists"""
    from PIL import Image, ImageDraw
    
    # Create icon directory if it doesn't exist
    icon_dir = Path("icons")
    icon_dir.mkdir(exist_ok=True)
    
    # Define icon paths based on platform
    system = platform.system()
    if system == "Windows":
        icon_path = icon_dir / "icon.ico"
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
    elif system == "Darwin":  # macOS
        icon_path = icon_dir / "icon.icns"
        sizes = [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512)]
    else:
        icon_path = icon_dir / "icon.png"
        sizes = [(128, 128)]
    
    # Skip if icon already exists
    if icon_path.exists():
        print(f"Using existing icon: {icon_path}")
        return str(icon_path)
    
    # Create a simple cursor icon
    print(f"Creating default icon at: {icon_path}")
    
    # For macOS, we need to create a .iconset directory with multiple sizes
    if system == "Darwin":
        iconset_dir = icon_dir / "icon.iconset"
        iconset_dir.mkdir(exist_ok=True)
        
        for size in sizes:
            img = Image.new('RGBA', size, color=(255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Draw a simple cursor arrow
            width, height = size
            cursor_points = [
                (width * 0.2, height * 0.2),  # Top-left
                (width * 0.5, height * 0.8),  # Bottom-middle
                (width * 0.6, height * 0.6),  # Middle-right
                (width * 0.8, height * 0.8),  # Bottom-right
                (width * 0.6, height * 0.5),  # Middle-middle
                (width * 0.8, height * 0.2),  # Top-right
            ]
            
            # Draw filled cursor shape
            draw.polygon(cursor_points, fill=(50, 153, 255, 255))
            
            # Save the icon at this size
            icon_size_path = iconset_dir / f"icon_{size[0]}x{size[1]}.png"
            img.save(icon_size_path)
        
        # Use iconutil to convert the iconset to icns (macOS only)
        try:
            subprocess.run(["iconutil", "-c", "icns", str(iconset_dir)], check=True)
            print(f"Created macOS icon: {icon_path}")
        except (subprocess.SubprocessError, FileNotFoundError):
            print("Warning: iconutil not found. Using PNG icon instead.")
            # Create a single PNG as fallback
            img = Image.new('RGBA', (128, 128), color=(255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            cursor_points = [
                (25, 25),      # Top-left
                (64, 102),    # Bottom-middle
                (77, 77),     # Middle-right
                (102, 102),   # Bottom-right
                (77, 64),     # Middle-middle
                (102, 25),    # Top-right
            ]
            draw.polygon(cursor_points, fill=(50, 153, 255, 255))
            icon_path = icon_dir / "icon.png"
            img.save(icon_path)
    else:
        # For Windows, create a simple .ico file
        img = Image.new('RGBA', (128, 128), color=(255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        cursor_points = [
            (25, 25),      # Top-left
            (64, 102),    # Bottom-middle
            (77, 77),     # Middle-right
            (102, 102),   # Bottom-right
            (77, 64),     # Middle-middle
            (102, 25),    # Top-right
        ]
        draw.polygon(cursor_points, fill=(50, 153, 255, 255))
        img.save(icon_path)
    
    return str(icon_path)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Build Custom Cursor App executable")
    parser.add_argument("--onedir", action="store_true", help="Build as directory instead of single file")
    parser.add_argument("--debug", action="store_true", help="Build with console for debugging")
    parser.add_argument("--icon", help="Path to custom icon file")
    parser.add_argument("--name", default="CustomCursorApp", help="Name of the output executable")
    parser.add_argument("--optimize", action="store_true", default=True, help="Apply size optimizations")
    parser.add_argument("--skip-security-fix", action="store_true", help="Skip macOS security fixes")
    args = parser.parse_args()
    
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Determine platform
    system = platform.system()
    
    # Create dist directory if it doesn't exist
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)
    
    # Build command base
    build_cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",  # Don't ask for confirmation
    ]
    
    # Add onefile/onedir option
    if not args.onedir:
        build_cmd.append("--onefile")
    
    # Add windowed/console option
    if not args.debug:
        build_cmd.append("--windowed")
        # Additional options to ensure no console appears
        build_cmd.append("--noconsole")
    
    # Size optimization options - more aggressive approach
    build_cmd.extend([
        "--strip",                  # Strip symbols from executables and shared libraries
        "--exclude-module=tkinter",  # Exclude unused modules
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
        "--collect-submodules=PIL",  # Only include used PIL modules
        "--collect-data=PIL",        # Only include necessary PIL data
        "--collect-submodules=PyQt6.QtCore",  # Only include necessary Qt modules
        "--collect-submodules=PyQt6.QtGui",
        "--collect-submodules=PyQt6.QtWidgets",
        "--collect-data=PyQt6.QtCore",
        "--collect-data=PyQt6.QtGui",
        "--collect-data=PyQt6.QtWidgets",
    ])
    
    # Use UPX for compression if available
    try:
        # Check if UPX is installed
        upx_result = subprocess.run(["which", "upx"], capture_output=True, text=True)
        if upx_result.returncode == 0:
            print("UPX found, using for compression")
            build_cmd.extend(["--upx-dir", os.path.dirname(upx_result.stdout.strip())])
        else:
            print("UPX not found, skipping compression")
    except Exception as e:
        print(f"Warning: Could not check for UPX: {e}")
    
    # Add name
    build_cmd.extend(["--name", args.name])
    
    # Handle icon
    icon_path = args.icon
    if not icon_path:
        # Create default icon if none provided
        icon_path = create_default_icon()
    
    if icon_path and os.path.exists(icon_path):
        build_cmd.extend(["--icon", icon_path])
    
    # Add data files
    build_cmd.extend(["--add-data", f"README.md:."])
    
    # Platform-specific options with more aggressive optimizations
    if system == "Windows":
        print("Building for Windows...")
        # Add Windows-specific options
        build_cmd.extend(["--add-binary", "venv/Lib/site-packages/PyQt6/Qt6/bin/*:PyQt6/Qt6/bin/"])
    elif system == "Darwin":  # macOS
        print("Building for macOS...")
        # Add macOS-specific options with minimal Qt libraries
        build_cmd.extend([
            # Only include essential Qt libraries
            "--add-binary", "venv/lib/python*/site-packages/PyQt6/Qt6/lib/QtCore.framework/Versions/A/QtCore:PyQt6/Qt6/lib/QtCore.framework/Versions/A/",
            "--add-binary", "venv/lib/python*/site-packages/PyQt6/Qt6/lib/QtGui.framework/Versions/A/QtGui:PyQt6/Qt6/lib/QtGui.framework/Versions/A/",
            "--add-binary", "venv/lib/python*/site-packages/PyQt6/Qt6/lib/QtWidgets.framework/Versions/A/QtWidgets:PyQt6/Qt6/lib/QtWidgets.framework/Versions/A/",
            # Add only essential plugins
            "--add-binary", "venv/lib/python*/site-packages/PyQt6/Qt6/plugins/platforms/libqcocoa.dylib:PyQt6/Qt6/plugins/platforms/",
            "--add-binary", "venv/lib/python*/site-packages/PyQt6/Qt6/plugins/styles/libqmacstyle.dylib:PyQt6/Qt6/plugins/styles/"
        ])
        # Add Info.plist with permissions for cursor access
        plist_file = Path("Info.plist")
        if not plist_file.exists():
            with open(plist_file, "w") as f:
                f.write('''
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>Custom Cursor App</string>
    <key>CFBundleIdentifier</key>
    <string>com.customcursor.app</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>NSHumanReadableCopyright</key>
    <string>Copyright © 2025</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>LSUIElement</key>
    <false/>
    <key>NSPrincipalClass</key>
    <string>NSApplication</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
</dict>
</plist>
''')
        build_cmd.extend(["--osx-bundle-identifier", "com.customcursor.app"])
    else:
        print(f"Unsupported platform: {system}")
        return 1
    
    # Add main script path
    build_cmd.append("src/main.py")
    
    # Run PyInstaller
    print(f"Running: {' '.join(build_cmd)}")
    subprocess.check_call(build_cmd)
    
    # Apply additional size optimizations after build
    if system == "Darwin" and args.optimize:  # macOS
        print("\nApplying additional size optimizations...")
        try:
            # Compress the app bundle if it exists
            if args.onedir and os.path.exists(f"dist/{args.name}.app"):
                print("Optimizing app bundle size...")
                # Remove unnecessary files - more aggressive cleanup
                for pattern in ["**/__pycache__", "**/*.pyc", "**/*.pyo", "**/*.pyi", "**/*.dist-info", "**/*.egg-info", 
                              "**/*.so", "**/*.dylib", "**/*.h", "**/*.hpp", "**/*.c", "**/*.cpp", "**/*.o", "**/*.a", 
                              "**/*.mo", "**/*.pot", "**/*.po", "**/*.txt", "**/*.md", "**/*.rst", "**/*.html", "**/*.css", 
                              "**/*.js", "**/*.json", "**/*.xml", "**/*.yaml", "**/*.yml", "**/*.ini", "**/*.cfg",
                              "**/*.qm", "**/*.ts", "**/*.qml"]:
                    for file in Path(f"dist/{args.name}.app").glob(pattern):
                        if file.is_file() and not file.name.startswith("libq") and not "QtCore" in file.name and not "QtGui" in file.name and not "QtWidgets" in file.name:
                            try:
                                file.unlink()
                            except Exception:
                                pass
                        elif file.is_dir() and file.name not in ["platforms", "styles", "QtCore.framework", "QtGui.framework", "QtWidgets.framework"]:
                            try:
                                shutil.rmtree(file)
                            except Exception:
                                pass
                
                # Remove all Qt plugins except essential ones
                qt_dirs = list(Path(f"dist/{args.name}.app").glob("**/PyQt6/Qt6/plugins"))
                for qt_dir in qt_dirs:
                    # Keep only essential Qt plugins
                    essential_plugins = ["platforms", "styles"]
                    for plugin_dir in qt_dir.iterdir():
                        if plugin_dir.is_dir() and plugin_dir.name not in essential_plugins:
                            print(f"Removing unused Qt plugin: {plugin_dir.name}")
                            try:
                                shutil.rmtree(plugin_dir)
                            except Exception:
                                pass
                
                # Remove all Qt frameworks except essential ones
                qt_framework_dirs = list(Path(f"dist/{args.name}.app").glob("**/PyQt6/Qt6/lib"))
                for framework_dir in qt_framework_dirs:
                    essential_frameworks = ["QtCore.framework", "QtGui.framework", "QtWidgets.framework"]
                    for item in framework_dir.iterdir():
                        if item.is_dir() and item.name not in essential_frameworks:
                            print(f"Removing unused Qt framework: {item.name}")
                            try:
                                shutil.rmtree(item)
                            except Exception:
                                pass
                
                # Remove unnecessary files from Python standard library
                python_lib_dirs = list(Path(f"dist/{args.name}.app").glob("**/lib-dynload"))
                for lib_dir in python_lib_dirs:
                    for file in lib_dir.glob("*.so"):
                        # Keep only essential modules
                        essential_modules = ["_datetime", "_random", "_socket", "_struct", "_posixsubprocess", "_pickle", "_ssl"]
                        if not any(module in file.name for module in essential_modules):
                            try:
                                file.unlink()
                                print(f"Removed unused Python module: {file.name}")
                            except Exception:
                                pass
            
            # If it's a single file executable, try to compress it
            elif os.path.exists(f"dist/{args.name}"):
                print("Compressing executable...")
                try:
                    # Use built-in compression tools
                    subprocess.run(["strip", f"dist/{args.name}"], check=False)
                    
                    # Try to use UPX for additional compression if available
                    try:
                        upx_result = subprocess.run(["which", "upx"], capture_output=True, text=True)
                        if upx_result.returncode == 0:
                            print("Using UPX for additional compression")
                            upx_path = upx_result.stdout.strip()
                            # Force UPX compression on macOS
                            subprocess.run([upx_path, "--best", "--force-macos", f"dist/{args.name}"], check=False)
                    except Exception as e:
                        print(f"Warning: UPX compression failed: {e}")
                except Exception as e:
                    print(f"Warning: Could not strip executable: {e}")
        except Exception as e:
            print(f"Warning: Size optimization failed: {e}")
    
    # Fix macOS security issues
    if system == "Darwin":
        print("\nFixing macOS security attributes...")
        try:
            # For single file executable
            if os.path.exists(f"dist/{args.name}"):
                print(f"Adding execute permissions to {args.name}")
                subprocess.run(["chmod", "+x", f"dist/{args.name}"], check=False)
                
                # Remove quarantine attribute
                print("Removing quarantine attribute")
                subprocess.run(["xattr", "-d", "com.apple.quarantine", f"dist/{args.name}"], check=False)
                
            # For app bundle
            if os.path.exists(f"dist/{args.name}.app"):
                print(f"Adding execute permissions to {args.name}.app")
                subprocess.run(["chmod", "-R", "+x", f"dist/{args.name}.app"], check=False)
                
                # Remove quarantine attribute
                print("Removing quarantine attribute")
                subprocess.run(["xattr", "-d", "com.apple.quarantine", f"dist/{args.name}.app"], check=False)
                
                # Ad-hoc signing (doesn't require a developer certificate)
                print("Applying ad-hoc code signing")
                subprocess.run(["codesign", "--force", "--deep", "--sign", "-", f"dist/{args.name}.app"], check=False)
        except Exception as e:
            print(f"Warning: Could not fix macOS security attributes: {e}")
    
    # Create a ZIP archive for distribution
    if system == "Windows":
        output_file = f"dist/{args.name}.exe"
        zip_file = f"dist/{args.name}_Windows.zip"
    else:  # macOS
        if args.onedir:
            output_file = f"dist/{args.name}.app"
            
            # For macOS, ensure the Info.plist is properly set up in the .app bundle
            app_plist = Path(f"dist/{args.name}.app/Contents/Info.plist")
            if app_plist.exists():
                try:
                    # Add LSUIElement to Info.plist if needed
                    subprocess.run(["defaults", "write", str(app_plist.absolute()), "LSUIElement", "0"], check=True)
                    print(f"Updated Info.plist in {args.name}.app")
                except Exception as e:
                    print(f"Warning: Could not update Info.plist: {e}")
                    
            # Create an optimized DMG file
            print("\nCreating optimized DMG file...")
            try:
                # First try with maximum compression using UDBZ format
                dmg_path = f"dist/{args.name}.dmg"
                subprocess.run([
                    "hdiutil", "create", 
                    "-volname", "Custom Cursor App", 
                    "-srcfolder", output_file,
                    "-ov", "-format", "UDBZ",  # Use bzip2 compression (best compression)
                    dmg_path
                ], check=True)
                print(f"Created optimized DMG: {dmg_path}")
                
                # Report the size of the DMG
                dmg_size = os.path.getsize(dmg_path) / (1024 * 1024)  # Convert to MB
                print(f"DMG size: {dmg_size:.2f} MB")
            except Exception as e:
                print(f"Warning: Could not create optimized DMG: {e}")
        else:
            output_file = f"dist/{args.name}"
        zip_file = f"dist/{args.name}_macOS.zip"
        
        # Add a README file with instructions for macOS users
        readme_path = Path("dist/README_MACOS.txt")
        with open(readme_path, "w") as f:
            f.write('''
IMPORTANT INSTRUCTIONS FOR MACOS USERS
====================================

If you see a message that the app is damaged or can't be opened:

1. Open Terminal (Applications > Utilities > Terminal)
2. Run the following command (copy and paste the entire line):
   xattr -d com.apple.quarantine /path/to/CustomCursorApp.app
   
   (Replace /path/to/CustomCursorApp.app with the actual path to the app)

3. Try opening the app again

This is necessary because macOS has strict security measures for apps not from the App Store.
''')
    
    if os.path.exists(output_file):
        print(f"\nCreating distribution archive: {zip_file}")
        shutil.make_archive(zip_file[:-4], 'zip', os.path.dirname(output_file), os.path.basename(output_file))
        print(f"Archive created: {zip_file}")
    
    print(f"\nBuild completed successfully!")
    print(f"Executable can be found in: {os.path.abspath('dist')}")
    print(f"Distribution ZIP file: {os.path.abspath(zip_file)}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
