#!/usr/bin/env python3
"""
Generate images for the Custom Cursor App website
"""

import os
from PIL import Image, ImageDraw, ImageFont

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)

def create_logo():
    """Create a simple logo for the website"""
    img = Image.new('RGBA', (200, 200), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw a cursor shape
    cursor_points = [
        (40, 40),       # Top-left
        (100, 160),     # Bottom-middle
        (120, 120),     # Middle-right
        (160, 160),     # Bottom-right
        (120, 100),     # Middle-middle
        (160, 40),      # Top-right
    ]
    
    # Draw filled cursor shape
    draw.polygon(cursor_points, fill=(74, 134, 232, 255))  # Primary color
    
    # Add a border
    draw.polygon(cursor_points, outline=(108, 92, 231, 255), width=3)  # Secondary color
    
    # Save in different sizes
    img.save('website/images/logo.png')
    
    # Create favicon
    favicon = img.resize((32, 32), Image.LANCZOS)
    favicon.save('website/images/favicon.png')
    
    print("Created logo.png and favicon.png")

def create_os_icons():
    """Create macOS and Windows icons"""
    # macOS icon
    img_macos = Image.new('RGBA', (200, 200), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img_macos)
    
    # Draw Apple-like logo
    center_x, center_y = 100, 100
    radius = 80
    
    # Draw circle
    draw.ellipse((center_x - radius, center_y - radius, 
                  center_x + radius, center_y + radius), 
                 fill=(74, 134, 232, 255))
    
    # Draw bite
    bite_radius = radius * 0.7
    draw.ellipse((center_x, center_y - radius * 0.8, 
                  center_x + bite_radius * 1.3, center_y + bite_radius * 0.8), 
                 fill=(255, 255, 255, 0))
    
    img_macos.save('website/images/macos-icon.png')
    
    # Windows icon
    img_windows = Image.new('RGBA', (200, 200), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img_windows)
    
    # Draw Windows-like logo
    window_size = 80
    gap = 10
    
    # Top-left window
    draw.rectangle((center_x - window_size - gap/2, center_y - window_size - gap/2, 
                   center_x - gap/2, center_y - gap/2), 
                  fill=(74, 134, 232, 255))
    
    # Top-right window
    draw.rectangle((center_x + gap/2, center_y - window_size - gap/2, 
                   center_x + window_size + gap/2, center_y - gap/2), 
                  fill=(108, 92, 231, 255))
    
    # Bottom-left window
    draw.rectangle((center_x - window_size - gap/2, center_y + gap/2, 
                   center_x - gap/2, center_y + window_size + gap/2), 
                  fill=(0, 206, 201, 255))
    
    # Bottom-right window
    draw.rectangle((center_x + gap/2, center_y + gap/2, 
                   center_x + window_size + gap/2, center_y + window_size + gap/2), 
                  fill=(45, 52, 54, 255))
    
    img_windows.save('website/images/windows-icon.png')
    
    print("Created OS icons")

def create_app_screenshot():
    """Create a mock screenshot of the application"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(245, 246, 250))
    draw = ImageDraw.Draw(img)
    
    # Draw app window
    window_margin = 20
    draw.rectangle((window_margin, window_margin, width - window_margin, height - window_margin), 
                  fill=(255, 255, 255))
    
    # Draw header
    draw.rectangle((window_margin, window_margin, width - window_margin, window_margin + 50), 
                  fill=(74, 134, 232, 255))
    
    # Draw title
    try:
        # Try to use a font if available
        font = ImageFont.truetype("Arial", 20)
        draw.text((window_margin + 20, window_margin + 15), "Custom Cursor App", 
                 fill=(255, 255, 255), font=font)
    except:
        # Fallback if font not available
        draw.text((window_margin + 20, window_margin + 15), "Custom Cursor App", 
                 fill=(255, 255, 255))
    
    # Draw upload button
    button_width = 150
    button_height = 40
    button_x = width // 4
    button_y = height // 3
    draw.rectangle((button_x, button_y, button_x + button_width, button_y + button_height), 
                  fill=(74, 134, 232, 255))
    
    try:
        font = ImageFont.truetype("Arial", 16)
        draw.text((button_x + 30, button_y + 10), "Upload PNG", 
                 fill=(255, 255, 255), font=font)
    except:
        draw.text((button_x + 30, button_y + 10), "Upload PNG", 
                 fill=(255, 255, 255))
    
    # Draw apply button
    button_x = width // 4
    button_y = height // 3 + 60
    draw.rectangle((button_x, button_y, button_x + button_width, button_y + button_height), 
                  fill=(108, 92, 231, 255))
    
    try:
        font = ImageFont.truetype("Arial", 16)
        draw.text((button_x + 20, button_y + 10), "Apply as Cursor", 
                 fill=(255, 255, 255), font=font)
    except:
        draw.text((button_x + 20, button_y + 10), "Apply as Cursor", 
                 fill=(255, 255, 255))
    
    # Draw reset button
    button_x = width // 4
    button_y = height // 3 + 120
    draw.rectangle((button_x, button_y, button_x + button_width, button_y + button_height), 
                  fill=(45, 52, 54, 255))
    
    try:
        font = ImageFont.truetype("Arial", 16)
        draw.text((button_x + 15, button_y + 10), "Reset to Default", 
                 fill=(255, 255, 255), font=font)
    except:
        draw.text((button_x + 15, button_y + 10), "Reset to Default", 
                 fill=(255, 255, 255))
    
    # Draw preview area
    preview_x = width // 2 + 50
    preview_y = height // 3 - 30
    preview_size = 200
    draw.rectangle((preview_x, preview_y, preview_x + preview_size, preview_y + preview_size), 
                  fill=(245, 246, 250), outline=(74, 134, 232, 255), width=2)
    
    # Draw a cursor in the preview area
    cursor_points = [
        (preview_x + 50, preview_y + 50),
        (preview_x + 100, preview_y + 150),
        (preview_x + 120, preview_y + 120),
        (preview_x + 150, preview_y + 150),
        (preview_x + 120, preview_y + 100),
        (preview_x + 150, preview_y + 50),
    ]
    
    draw.polygon(cursor_points, fill=(74, 134, 232, 255))
    
    # Draw "Preview" text
    try:
        font = ImageFont.truetype("Arial", 16)
        draw.text((preview_x + 70, preview_y - 25), "Preview", 
                 fill=(45, 52, 54, 255), font=font)
    except:
        draw.text((preview_x + 70, preview_y - 25), "Preview", 
                 fill=(45, 52, 54, 255))
    
    # Save the screenshot
    img.save('website/images/app-screenshot.png')
    print("Created app screenshot")

def main():
    # Create images directory if it doesn't exist
    create_directory('website/images')
    
    # Create all the images
    create_logo()
    create_os_icons()
    create_app_screenshot()
    
    print("All website images created successfully!")

if __name__ == "__main__":
    main()
