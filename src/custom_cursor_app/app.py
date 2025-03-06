#!/usr/bin/env python3
"""
Custom Cursor App - Main Application
A cross-platform application that allows users to upload PNG files and use them as custom cursors.
"""

import os
import sys
import io
import platform
from pathlib import Path
from PIL import Image
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                            QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, 
                            QMessageBox, QSpinBox, QGroupBox, QFormLayout)
from PyQt6.QtGui import QPixmap, QIcon, QImage, QCursor, QGuiApplication, QPainter, QColor
from PyQt6.QtCore import Qt, QSize, QBuffer, QIODevice, QEvent, QObject, QTimer, QPoint

# Platform-specific imports
if platform.system() == 'Windows':
    import win32api
    import win32con
    import win32gui
    import ctypes
    from ctypes import wintypes
elif platform.system() == 'Darwin':  # macOS
    from PyQt6.QtCore import QByteArray
    try:
        from Cocoa import NSCursor, NSImage, NSData, NSBitmapImageRep, NSPoint
    except ImportError:
        print("Error: pyobjc-framework-Cocoa is required for macOS. Install with: pip install pyobjc-framework-Cocoa")
        sys.exit(1)


class CursorOverlay(QWidget):
    """A borderless, transparent window that follows the mouse cursor to create a system-wide custom cursor effect"""
    def __init__(self):
        super().__init__()
        # Create a borderless, transparent window that stays on top of everything
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | 
                           Qt.WindowType.Tool | 
                           Qt.WindowType.WindowStaysOnTopHint | 
                           Qt.WindowType.WindowTransparentForInput | 
                           Qt.WindowType.NoDropShadowWindowHint)
        
        # Make sure the window is completely transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
        
        # Set initial size
        self.resize(32, 32)
        
        # Initialize variables
        self.cursor_pixmap = None
        self.hotspot_x = 0
        self.hotspot_y = 0
        
        # Hide the actual system cursor when over our window
        self.setCursor(Qt.CursorShape.BlankCursor)
        
        # Create a timer to update the overlay position
        self.position_timer = QTimer(self)
        self.position_timer.timeout.connect(self.update_position)
        self.position_timer.start(1)  # Update extremely frequently for smooth movement
    
    def set_cursor_image(self, pixmap, hotspot_x=0, hotspot_y=0):
        """Set the cursor image and hotspot"""
        self.cursor_pixmap = pixmap
        self.hotspot_x = hotspot_x
        self.hotspot_y = hotspot_y
        self.resize(pixmap.width(), pixmap.height())
        self.show()
        self.update()
    
    def update_position(self):
        """Update the overlay position to follow the mouse cursor"""
        if self.cursor_pixmap:
            cursor_pos = QCursor.pos()
            # Adjust position by hotspot
            self.move(cursor_pos.x() - self.hotspot_x, cursor_pos.y() - self.hotspot_y)
            
            # Ensure we're always on top and visible
            if not self.isVisible():
                self.show()
                self.raise_()
    
    def paintEvent(self, event):
        """Draw the cursor image"""
        if self.cursor_pixmap:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawPixmap(0, 0, self.cursor_pixmap)
            painter.end()
    
    def hide_overlay(self):
        """Hide the cursor overlay"""
        self.hide()
        self.cursor_pixmap = None


class CustomCursorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Cursors")
        self.setMinimumSize(500, 600)
        
        # Set application name for proper macOS integration
        QApplication.setApplicationName("Custom Cursors")
        QApplication.setOrganizationName("CustomCursor")
        QApplication.setOrganizationDomain("customcursorapp.com")      
        # Initialize variables
        self.current_image_path = None
        self.hotspot_x = 0
        self.hotspot_y = 0
        self.custom_cursor = None
        self.original_cursors = {}
        
        # Create cursor overlay for system-wide cursor
        self.cursor_overlay = CursorOverlay()
        
        # Install event filter for the entire application
        QApplication.instance().installEventFilter(self)
        
        # Setup UI
        self.init_ui()
    
    def eventFilter(self, obj, event):
        """Event filter to help maintain custom cursor"""
        if hasattr(self, 'ns_cursor') and self.ns_cursor is not None:
            # Only handle application activation events to reduce flickering
            # Handling too many events causes cursor flickering
            if event.type() in [QEvent.Type.ApplicationActivate, QEvent.Type.WindowActivate]:
                try:
                    # Push the cursor again when the application regains focus
                    self.ns_cursor.push()
                except Exception as e:
                    print(f"Error in event filter: {e}")
        return super().eventFilter(obj, event)
    
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Windsurf branding label - smaller and subtle with new color
        windsurf_label = QLabel("Made with Windsurf")
        windsurf_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        windsurf_label.setStyleSheet("color: #71E9D8; font-size: 12px; margin: 4px 0;")
        
        # Image preview section - improved spacing and padding
        self.preview_group = QGroupBox("Cursor Preview")
        self.preview_group.setStyleSheet("QGroupBox { padding-top: 15px; margin-top: 5px; }")
        preview_layout = QVBoxLayout()
        preview_layout.setContentsMargins(15, 15, 15, 15)  # Add proper padding inside the group box
        
        self.image_preview = QLabel("No image selected")
        self.image_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_preview.setMinimumSize(400, 400)
        self.image_preview.setStyleSheet("border: 1px solid #ccc; background-color: #333;")
        
        preview_layout.addWidget(self.image_preview)
        self.preview_group.setLayout(preview_layout)
        
        # Initialize hotspot spinboxes but don't show them in the UI
        self.hotspot_x_spin = QSpinBox()
        self.hotspot_x_spin.setRange(0, 256)
        self.hotspot_x_spin.valueChanged.connect(self.update_hotspot)
        self.hotspot_x_spin.hide()
        
        self.hotspot_y_spin = QSpinBox()
        self.hotspot_y_spin.setRange(0, 256)
        self.hotspot_y_spin.valueChanged.connect(self.update_hotspot)
        self.hotspot_y_spin.hide()
        
        # Buttons section with improved spacing
        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(10, 10, 10, 10)  # Add margins around buttons
        buttons_layout.setSpacing(10)  # Add spacing between buttons
        
        self.upload_btn = QPushButton("Upload PNG")
        self.upload_btn.clicked.connect(self.upload_image)
        self.upload_btn.setMinimumHeight(30)  # Make buttons taller
        
        self.apply_btn = QPushButton("Apply as Cursor")
        self.apply_btn.clicked.connect(self.apply_cursor)
        self.apply_btn.setEnabled(False)
        self.apply_btn.setMinimumHeight(30)  # Make buttons taller
        
        self.reset_btn = QPushButton("Reset to Default")
        self.reset_btn.clicked.connect(self.reset_cursor)
        self.reset_btn.setMinimumHeight(30)  # Make buttons taller
        
        buttons_layout.addWidget(self.upload_btn)
        buttons_layout.addWidget(self.apply_btn)
        buttons_layout.addWidget(self.reset_btn)
        
        # Add all sections to main layout with improved spacing
        main_layout.setSpacing(15)  # Add spacing between layout elements
        main_layout.setContentsMargins(20, 10, 20, 20)  # Add margins around the entire layout
        main_layout.addWidget(windsurf_label, 0, Qt.AlignmentFlag.AlignCenter)  # Place the label at the top center
        main_layout.addSpacing(5)  # Small space after the label
        main_layout.addWidget(self.preview_group, 9)  # Give preview 90% of the weight
        main_layout.addSpacing(10)  # Space between preview and buttons
        main_layout.addLayout(buttons_layout, 1)  # Give buttons 10% of the weight
        
        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def upload_image(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, "Select PNG Image", "", "PNG Files (*.png)"
        )
        
        if image_path:
            try:
                # Load and display the image
                self.current_image_path = image_path
                pixmap = QPixmap(image_path)
                
                # Resize if too large for preview
                if pixmap.width() > 200 or pixmap.height() > 200:
                    pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                
                self.image_preview.setPixmap(pixmap)
                
                # Reset hotspot values and enable apply button
                self.hotspot_x_spin.setMaximum(pixmap.width() - 1)
                self.hotspot_y_spin.setMaximum(pixmap.height() - 1)
                self.hotspot_x_spin.setValue(0)
                self.hotspot_y_spin.setValue(0)
                self.apply_btn.setEnabled(True)
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load image: {str(e)}")
    
    def update_hotspot(self):
        self.hotspot_x = self.hotspot_x_spin.value()
        self.hotspot_y = self.hotspot_y_spin.value()
    
    def apply_cursor(self):
        if not self.current_image_path:
            QMessageBox.warning(self, "Warning", "Please upload an image first.")
            return
        
        try:
            # Get the current OS
            current_os = platform.system()
            
            if current_os == 'Windows':
                self.apply_cursor_windows()
            elif current_os == 'Darwin':  # macOS
                self.apply_cursor_macos()
            else:
                QMessageBox.warning(self, "Unsupported OS", 
                                   f"Your operating system ({current_os}) is not supported.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply cursor: {str(e)}")
    
    def apply_cursor_windows(self):
        """Apply the cursor on Windows systems"""
        try:
            # Load the image
            img = Image.open(self.current_image_path)
            
            # Ensure image is in the right format
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a temporary .cur file
            temp_dir = os.path.join(os.path.expanduser("~"), ".custom_cursor_app")
            os.makedirs(temp_dir, exist_ok=True)
            
            cursor_path = os.path.join(temp_dir, "custom_cursor.cur")
            
            # Save as .cur file with hotspot
            self._save_as_cur(img, cursor_path, self.hotspot_x, self.hotspot_y)
            
            # Load and apply the cursor
            cursor_handle = win32gui.LoadImage(
                0, cursor_path, win32con.IMAGE_CURSOR,
                0, 0, win32con.LR_LOADFROMFILE
            )
            
            # Set the cursor
            ctypes.windll.user32.SetSystemCursor(cursor_handle, win32con.OCR_NORMAL)
            
            QMessageBox.information(self, "Success", "Custom cursor applied successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply Windows cursor: {str(e)}")
    
    def _save_as_cur(self, img, path, hotspot_x, hotspot_y):
        """Save an image as a Windows .cur file"""
        # Ensure image is not too large (Windows limitation)
        if img.width > 256 or img.height > 256:
            img = img.resize((256, 256), Image.LANCZOS)
        
        # Cursor file format header
        header = bytearray([
            0, 0,  # Reserved, must be 0
            2, 0,  # Type (1 for ICO, 2 for CUR)
            1, 0,  # Number of images
        ])
        
        # Directory entry
        width = img.width if img.width < 256 else 0  # 0 means 256
        height = img.height if img.height < 256 else 0  # 0 means 256
        
        directory = bytearray([
            width,  # Width
            height,  # Height
            0,  # Color count (0 for 32bpp)
            0,  # Reserved
            hotspot_x & 0xFF, (hotspot_x >> 8) & 0xFF,  # Hotspot X
            hotspot_y & 0xFF, (hotspot_y >> 8) & 0xFF,  # Hotspot Y
            0, 0, 0, 0,  # Size of image data (filled in later)
            0, 0, 0, 0,  # Offset to image data (filled in later)
        ])
        
        # Convert image to BMP format in memory
        import io
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_data = img_byte_arr.getvalue()
        
        # Update directory with size and offset
        img_size = len(img_data)
        img_offset = len(header) + len(directory)
        
        directory[8:12] = img_size.to_bytes(4, byteorder='little')
        directory[12:16] = img_offset.to_bytes(4, byteorder='little')
        
        # Write the cursor file
        with open(path, 'wb') as f:
            f.write(header)
            f.write(directory)
            f.write(img_data)
    
    def apply_cursor_macos(self):
        """Apply the cursor on macOS systems using the NSCursor approach"""
        try:
            # Stop any existing cursor timers
            if hasattr(self, 'cursor_timer') and self.cursor_timer.isActive():
                self.cursor_timer.stop()
            
            # Load the image
            img = Image.open(self.current_image_path)
            
            # Convert PIL Image to RGBA if needed
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Resize image to standard cursor size if needed
            max_size = 32  # Standard cursor size
            if img.width > max_size or img.height > max_size:
                # Calculate new dimensions while preserving aspect ratio
                ratio = min(max_size / img.width, max_size / img.height)
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Save the cursor to a temporary directory for persistence
            temp_dir = os.path.join(os.path.expanduser("~"), ".custom_cursor_app")
            os.makedirs(temp_dir, exist_ok=True)
            cursor_path = os.path.join(temp_dir, "custom_cursor.png")
            img.save(cursor_path)
            
            # For macOS, we need to use NSCursor for system-wide cursor
            # Convert PIL image to NSImage
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_data = img_byte_arr.getvalue()
            
            # Create NSData from the image bytes
            ns_data = NSData.dataWithBytes_length_(img_data, len(img_data))
            
            # Create NSImage from NSData
            ns_image_rep = NSBitmapImageRep.imageRepWithData_(ns_data)
            ns_image = NSImage.alloc().initWithSize_((img.width, img.height))
            ns_image.addRepresentation_(ns_image_rep)
            
            # Create NSCursor with the NSImage
            hotspot_x = min(self.hotspot_x, img.width - 1)
            hotspot_y = min(self.hotspot_y, img.height - 1)
            ns_cursor = NSCursor.alloc().initWithImage_hotSpot_(ns_image, NSPoint(hotspot_x, hotspot_y))
            
            # Store the cursor for future reference
            self.ns_cursor = ns_cursor
            
            # Push the cursor onto the cursor stack instead of just setting it
            # This helps prevent flickering
            ns_cursor.push()
            
            # Create a timer to periodically check if the cursor needs to be reapplied
            # but with a much lower frequency to prevent flickering
            self.cursor_timer = QTimer(self)
            
            def reapply_cursor():
                try:
                    # Only reapply if absolutely necessary
                    # This reduces flickering by minimizing cursor changes
                    if hasattr(self, 'ns_cursor') and self.ns_cursor is not None:
                        # No need to constantly set() the cursor, which causes flickering
                        # Instead, we'll rely on the push() we did earlier and the event filter
                        pass
                except Exception as e:
                    print(f"Cursor reapply error: {e}")
            
            # Connect and start the timer with very low frequency to prevent flickering
            self.cursor_timer.timeout.connect(reapply_cursor)
            self.cursor_timer.start(2000)  # Very infrequent checks (2 seconds) to minimize flickering
            
            QMessageBox.information(self, "Success", "Custom cursor applied system-wide!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply macOS cursor: {str(e)}")
            
    def reset_cursor(self):
        """Reset to the default system cursor"""
        try:
            # Stop the timer if it exists
            if hasattr(self, 'cursor_timer') and self.cursor_timer.isActive():
                self.cursor_timer.stop()
            
            # For macOS, reset the NSCursor to the system default if we were using it
            if hasattr(self, 'ns_cursor'):
                # Pop all cursors from the stack to get back to the default
                while True:
                    try:
                        NSCursor.pop()
                    except:
                        break  # Break when we've popped all cursors
                
                # Set the arrow cursor
                NSCursor.arrowCursor().set()
                self.ns_cursor = None
            
            # Restore any override cursor from QApplication
            while QApplication.instance().overrideCursor() is not None:
                QApplication.instance().restoreOverrideCursor()
            
            # Reset cursor to default
            self.unsetCursor()
            
            # Remove the reference to the custom cursor
            if hasattr(self, 'custom_cursor'):
                self.custom_cursor = None
            
            QMessageBox.information(self, "Success", "Cursor reset to default successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reset cursor: {str(e)}")


def run_app():
    """Run the Custom Cursor Application"""
    print("Starting Custom Cursor App...")
    if not QApplication.instance():
        print("Creating QApplication instance...")
        app = QApplication(sys.argv)
    else:
        print("Using existing QApplication instance...")
        app = QApplication.instance()
    
    print("Creating main window...")
    window = CustomCursorApp()
    print("Showing main window...")
    window.show()
    
    # Ensure cursor is restored on application exit
    def cleanup():
        print("Cleaning up...")
        try:
            # For macOS, reset the NSCursor to the system default
            if platform.system() == 'Darwin':
                # Pop all cursors from the stack to get back to the default
                while True:
                    try:
                        NSCursor.pop()
                    except:
                        break  # Break when we've popped all cursors
                
                # Set the arrow cursor
                NSCursor.arrowCursor().set()
            
            # Restore any override cursor from QApplication
            while QApplication.instance().overrideCursor() is not None:
                QApplication.instance().restoreOverrideCursor()
        except Exception as e:
            print(f"Error during cleanup: {e}")
    
    app.aboutToQuit.connect(cleanup)
    
    # Import necessary modules for event filtering
    from PyQt6.QtCore import QEvent, QTimer
    
    # Create a more robust application-wide event filter
    class AppEventFilter(QObject):
        def eventFilter(self, watched, event):
            # Handle application activation/deactivation events specially
            if event.type() in [QEvent.Type.ApplicationActivate, QEvent.Type.WindowActivate]:
                # When app regains focus, force cursor update
                try:
                    if platform.system() == 'Darwin' and hasattr(window, 'ns_cursor') and window.ns_cursor is not None:
                        # Force reapply the cursor
                        NSCursor.hide()
                        window.ns_cursor.set()
                        NSCursor.unhide()
                except Exception as e:
                    print(f"Error in activation event: {e}")
            
            # Handle all mouse events
            if hasattr(window, 'custom_cursor') and window.custom_cursor is not None:
                if event.type() in [QEvent.Type.MouseMove, QEvent.Type.MouseButtonPress, 
                                  QEvent.Type.MouseButtonRelease, QEvent.Type.HoverMove]:
                    try:
                        # For macOS, use NSCursor
                        if platform.system() == 'Darwin' and hasattr(window, 'ns_cursor'):
                            window.ns_cursor.set()
                        
                        # Also ensure Qt cursor is applied
                        if QApplication.instance().overrideCursor() is None:
                            QApplication.instance().setOverrideCursor(window.custom_cursor)
                    except Exception as e:
                        print(f"Error in mouse event: {e}")
            return False
    
    # Create and install the event filter
    app_filter = AppEventFilter()
    app.installEventFilter(app_filter)
    
    # Create a global timer to periodically reapply the cursor
    # This helps maintain the cursor even when the app loses focus
    global_cursor_timer = QTimer()
    
    def global_reapply_cursor():
        try:
            # Handle NSCursor for macOS
            if platform.system() == 'Darwin' and hasattr(window, 'ns_cursor') and window.ns_cursor is not None:
                # Force reapply the cursor by hiding/showing
                NSCursor.hide()
                window.ns_cursor.set()
                NSCursor.unhide()
            
            # Handle Qt cursor as backup
            if hasattr(window, 'custom_cursor') and window.custom_cursor is not None:
                if QApplication.instance().overrideCursor() is None:
                    QApplication.instance().setOverrideCursor(window.custom_cursor)
        except Exception as e:
            print(f"Error in global timer: {e}")
    
    global_cursor_timer.timeout.connect(global_reapply_cursor)
    global_cursor_timer.start(20)  # Check more frequently for better responsiveness
    
    sys.exit(app.exec())

if __name__ == '__main__':
    run_app()
