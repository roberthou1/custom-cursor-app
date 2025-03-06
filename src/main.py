#!/usr/bin/env python3
"""
Custom Cursors - Main Entry Point
A cross-platform application that allows users to upload PNG files and use them as custom cursors.
"""

import sys
import os
import traceback
import platform
import importlib.util
from pathlib import Path

# Set up basic logging to a file for debugging
import logging
log_dir = os.path.expanduser("~/Library/Logs/CustomCursors") if platform.system() == "Darwin" else os.path.join(os.path.expanduser("~"), "CustomCursors", "logs")
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Entry point for the application"""
    try:
        logging.info("Starting Custom Cursors application")
        logging.info(f"Python version: {sys.version}")
        logging.info(f"Platform: {platform.platform()}")
        logging.info(f"System: {platform.system()}")
        logging.info(f"Current directory: {os.getcwd()}")
        logging.info(f"Executable path: {sys.executable}")
        
        # Import the app module
        try:
            logging.info("Importing app module")
            
            # First try the normal import
            try:
                from custom_cursor_app.app import run_app
                logging.info("Successfully imported app module using normal import")
            except ImportError:
                logging.info("Normal import failed, trying alternative methods")
                
                # Try to find the module in the current directory or executable directory
                base_dirs = [
                    os.path.dirname(os.path.abspath(__file__)),  # Current script directory
                    os.path.dirname(sys.executable),  # Executable directory
                    os.getcwd(),  # Current working directory
                    # For packaged app, check in the bundle resources
                    os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
                ]
                
                module_found = False
                for base_dir in base_dirs:
                    logging.info(f"Trying to import from: {base_dir}")
                    
                    # Try direct import of app.py
                    app_path = os.path.join(base_dir, 'custom_cursor_app', 'app.py')
                    if os.path.exists(app_path):
                        logging.info(f"Found app.py at: {app_path}")
                        spec = importlib.util.spec_from_file_location("app", app_path)
                        app_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(app_module)
                        run_app = app_module.run_app
                        module_found = True
                        logging.info("Successfully imported app module from file")
                        break
                    
                    # Try to add the directory to sys.path
                    if os.path.exists(os.path.join(base_dir, 'custom_cursor_app')):
                        logging.info(f"Found custom_cursor_app directory at: {base_dir}")
                        if base_dir not in sys.path:
                            sys.path.insert(0, base_dir)
                        try:
                            from custom_cursor_app.app import run_app
                            module_found = True
                            logging.info("Successfully imported app module after path adjustment")
                            break
                        except ImportError as e:
                            logging.warning(f"Import still failed after path adjustment: {e}")
                
                if not module_found:
                    # Last resort: try to find app.py anywhere in the bundle
                    logging.info("Searching for app.py in the entire bundle")
                    for root, dirs, files in os.walk(os.path.dirname(sys.executable)):
                        if 'app.py' in files:
                            app_path = os.path.join(root, 'app.py')
                            logging.info(f"Found app.py at: {app_path}")
                            spec = importlib.util.spec_from_file_location("app", app_path)
                            app_module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(app_module)
                            if hasattr(app_module, 'run_app'):
                                run_app = app_module.run_app
                                module_found = True
                                logging.info("Successfully imported app module from search")
                                break
                    
                    if not module_found:
                        raise ImportError("Could not find the app module after trying all methods")
            
            logging.info("Successfully imported app module")
        except ImportError as e:
            logging.error(f"Failed to import app module: {e}")
            logging.error(traceback.format_exc())
            sys.exit(1)
        
        # Run the app
        logging.info("Running the application")
        run_app()
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")
        logging.critical(traceback.format_exc())
        # Display error message to user if possible
        try:
            from PyQt6.QtWidgets import QApplication, QMessageBox
            app = QApplication(sys.argv)
            error_box = QMessageBox()
            error_box.setIcon(QMessageBox.Icon.Critical)
            error_box.setWindowTitle("Custom Cursors - Error")
            error_box.setText("An error occurred while starting the application.")
            error_box.setDetailedText(f"Error: {str(e)}\n\nTraceback: {traceback.format_exc()}")
            error_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            error_box.exec()
        except Exception:
            # If we can't show a GUI error, at least print to console
            print(f"Critical error: {e}")
            print(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
