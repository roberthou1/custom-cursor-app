#!/usr/bin/env python3
"""
Ultra Compression Script for Custom Cursor App
This script creates an extremely compressed DMG file from the existing app bundle.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_app_bundle():
    """Aggressively clean the app bundle to remove unnecessary files"""
    print("Aggressively cleaning app bundle...")
    
    app_path = Path("dist/CustomCursorApp.app")
    if not app_path.exists():
        print(f"Error: {app_path} does not exist")
        return False
    
    # Create a copy of the app bundle to work with
    clean_app_path = Path("dist/ultra_compressed/CustomCursorApp.app")
    if clean_app_path.exists():
        shutil.rmtree(clean_app_path)
    
    # Copy the app bundle
    shutil.copytree(app_path, clean_app_path, symlinks=True)
    
    # Remove unnecessary files and directories
    unnecessary_patterns = [
        # Documentation and metadata
        "**/*.txt", "**/*.md", "**/*.rst", "**/*.html", "**/*.pdf", 
        "**/*.css", "**/*.js", "**/*.json", "**/*.xml", "**/*.yaml", 
        "**/*.yml", "**/*.ini", "**/*.cfg", "**/*.plist",
        
        # Python cache files
        "**/__pycache__", "**/*.pyc", "**/*.pyo", "**/*.pyi",
        
        # Package metadata
        "**/*.dist-info", "**/*.egg-info",
        
        # Development files
        "**/*.h", "**/*.hpp", "**/*.c", "**/*.cpp", "**/*.o", "**/*.a",
        
        # Translation files
        "**/*.mo", "**/*.pot", "**/*.po", "**/*.qm", "**/*.ts",
        
        # Qt QML files (not needed for this app)
        "**/*.qml",
        
        # Unused libraries and plugins
        "**/QtNetwork*", "**/QtSql*", "**/QtMultimedia*", "**/QtQml*",
        "**/QtWebEngine*", "**/QtXml*", "**/QtTest*", "**/QtSvg*",
        "**/QtPrintSupport*", "**/QtOpenGL*", "**/QtLocation*",
        
        # Unused plugins
        "**/plugins/imageformats", "**/plugins/bearer", "**/plugins/iconengines",
        "**/plugins/sqldrivers", "**/plugins/multimedia", "**/plugins/webview",
    ]
    
    # Process each pattern
    for pattern in unnecessary_patterns:
        for file_path in clean_app_path.glob(pattern):
            try:
                if file_path.is_file():
                    # Skip essential files
                    if (file_path.name.startswith("libq") or 
                        "QtCore" in file_path.name or 
                        "QtGui" in file_path.name or 
                        "QtWidgets" in file_path.name or
                        file_path.name.endswith(".dylib")):
                        continue
                    file_path.unlink()
                    print(f"Removed file: {file_path.relative_to(clean_app_path)}")
                elif file_path.is_dir():
                    # Skip essential directories
                    if file_path.name in ["platforms", "styles", "QtCore.framework", 
                                         "QtGui.framework", "QtWidgets.framework"]:
                        continue
                    shutil.rmtree(file_path)
                    print(f"Removed directory: {file_path.relative_to(clean_app_path)}")
            except Exception as e:
                print(f"Warning: Could not remove {file_path}: {e}")
    
    # Remove all Qt frameworks except essential ones
    qt_lib_dir = clean_app_path / "Contents" / "Frameworks"
    if qt_lib_dir.exists():
        essential_frameworks = ["QtCore.framework", "QtGui.framework", "QtWidgets.framework"]
        for item in qt_lib_dir.iterdir():
            if item.is_dir() and item.name.startswith("Qt") and item.name not in essential_frameworks:
                try:
                    shutil.rmtree(item)
                    print(f"Removed Qt framework: {item.name}")
                except Exception as e:
                    print(f"Warning: Could not remove {item}: {e}")
    
    # Strip all binaries to remove debug symbols
    print("Stripping binaries to remove debug symbols...")
    for binary in clean_app_path.glob("**/*.so"):
        try:
            subprocess.run(["strip", "-S", str(binary)], check=False)
        except Exception:
            pass
    
    for binary in clean_app_path.glob("**/*.dylib"):
        try:
            subprocess.run(["strip", "-S", str(binary)], check=False)
        except Exception:
            pass
    
    # Apply UPX compression to binaries if available
    try:
        upx_result = subprocess.run(["which", "upx"], capture_output=True, text=True)
        if upx_result.returncode == 0:
            upx_path = upx_result.stdout.strip()
            print("Applying UPX compression to binaries...")
            
            # Compress dylib files
            for dylib in clean_app_path.glob("**/*.dylib"):
                try:
                    subprocess.run([upx_path, "--best", "--ultra-brute", str(dylib)], 
                                  check=False, capture_output=True)
                except Exception:
                    pass
            
            # Compress the main executable
            main_exe = clean_app_path / "Contents" / "MacOS" / "CustomCursorApp"
            if main_exe.exists():
                try:
                    subprocess.run([upx_path, "--best", "--ultra-brute", "--force-macos", str(main_exe)], 
                                  check=False)
                except Exception as e:
                    print(f"Warning: Could not compress main executable: {e}")
    except Exception:
        print("UPX not found, skipping binary compression")
    
    print(f"App bundle cleaning complete: {clean_app_path}")
    return clean_app_path

def create_ultra_compressed_dmg(app_path):
    """Create an ultra-compressed DMG file"""
    print("\nCreating ultra-compressed DMG file...")
    
    # Create a temporary directory for DMG contents
    dmg_contents = Path("dist/ultra_compressed/dmg_contents")
    if dmg_contents.exists():
        shutil.rmtree(dmg_contents)
    dmg_contents.mkdir(exist_ok=True)
    
    # Copy the app to the temporary directory
    shutil.copytree(app_path, dmg_contents / "CustomCursorApp.app", symlinks=True)
    
    # Create a symlink to Applications folder
    os.symlink("/Applications", dmg_contents / "Applications")
    
    # Create the DMG with maximum compression
    dmg_path = "dist/CustomCursorApp-Ultra.dmg"
    
    # Try with UDBZ format first (bzip2 compression - best compression ratio)
    try:
        subprocess.run([
            "hdiutil", "create",
            "-volname", "Custom Cursor App",
            "-srcfolder", str(dmg_contents),
            "-ov", "-format", "UDBZ",  # Use bzip2 compression
            dmg_path
        ], check=True)
        
        print(f"Created ultra-compressed DMG: {dmg_path}")
        
        # Report the size
        dmg_size = os.path.getsize(dmg_path) / (1024 * 1024)  # Convert to MB
        print(f"Ultra-compressed DMG size: {dmg_size:.2f} MB")
        
    except Exception as e:
        print(f"Warning: Could not create ultra-compressed DMG: {e}")
    
    # Clean up temporary directory
    shutil.rmtree(dmg_contents)

def main():
    # Clean the app bundle
    cleaned_app_path = clean_app_bundle()
    if not cleaned_app_path:
        print("Error: App bundle cleaning failed")
        sys.exit(1)
    
    # Create ultra-compressed DMG
    create_ultra_compressed_dmg(cleaned_app_path)
    
    print("\nUltra compression completed!")
    print("Check dist/CustomCursorApp-Ultra.dmg for the ultra-compressed DMG file.")

if __name__ == "__main__":
    main()
