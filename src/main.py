#!/usr/bin/env python3
"""
Custom Cursors - Main Entry Point
A cross-platform application that allows users to upload PNG files and use them as custom cursors.
"""

import sys
import os
import traceback
import platform

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
            from custom_cursor_app.app import run_app
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
