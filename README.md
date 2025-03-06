# Custom Cursor App

A cross-platform application that allows you to upload PNG files and use them as your computer's cursor. Works on both macOS and Windows.

## Features

- Upload any PNG image to use as your cursor
- Set the hotspot position (the active point of the cursor)
- Reset to the default system cursor
- Works on both macOS and Windows

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Option 1: Install from Source

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/custom-cursor-app.git
   cd custom-cursor-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

### Option 2: Install as a Package

1. Install the package:
   ```
   pip install .
   ```

2. Run the application:
   ```
   custom-cursor-app
   ```

## Building Standalone Executables

The easiest way to build a standalone executable is to use the included build script:

```bash
# Activate your virtual environment first
source venv/bin/activate  # On macOS/Linux
# or
.\venv\Scripts\activate  # On Windows

# Run the build script
python build_app.py
```

This will:
1. Create a default icon if none exists
2. Package all dependencies
3. Create a standalone executable in the `dist` directory
4. Create a ZIP file for easy distribution

### Advanced Build Options

The build script supports several options:

```bash
# Build with debugging console
python build_app.py --debug

# Build as a directory instead of a single file
python build_app.py --onedir

# Specify a custom icon
python build_app.py --icon path/to/your/icon.png

# Specify a custom name for the executable
python build_app.py --name "MyCursorApp"
```

### Manual Build (Alternative)

#### For Windows

```bash
pyinstaller --onefile --windowed --icon=icons/icon.ico src/main.py
```

#### For macOS

```bash
pyinstaller --onefile --windowed --icon=icons/icon.icns src/main.py
```

## Usage

1. Launch the application
2. Click "Upload PNG" to select a PNG image file
3. Adjust the hotspot position (X and Y coordinates) if needed
4. Click "Apply as Cursor" to set your custom cursor
5. To revert to the default cursor, click "Reset to Default"

## Limitations

- Cursor size is limited to 48x48 pixels for optimal display
- On macOS, the cursor may occasionally revert to default in certain system areas due to security restrictions
- On Windows, cursor changes require appropriate permissions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt6 for the cross-platform GUI
- Pillow for image processing
