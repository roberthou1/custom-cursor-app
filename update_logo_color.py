#!/usr/bin/env python3
"""
Script to update the logo color from blue to orange for the website
"""

from PIL import Image, ImageDraw

def create_orange_logo():
    """Create an orange version of the cursor logo"""
    # Create a new image with transparency
    img = Image.new('RGBA', (512, 512), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Define the cursor points (scaled for 512x512 image)
    cursor_points = [
        (102, 102),      # Top-left
        (256, 410),      # Bottom-middle
        (307, 307),      # Middle-right
        (410, 410),      # Bottom-right
        (307, 256),      # Middle-middle
        (410, 102),      # Top-right
    ]
    
    # Draw filled cursor shape with the orange accent color from the website
    # Using #FF9A8B as defined in the CSS
    orange_color = (255, 154, 139, 255)  # #FF9A8B in RGBA
    draw.polygon(cursor_points, fill=orange_color)
    
    # Save the new orange logo
    img.save('website/images/logo_orange.png')
    print("Created orange logo at website/images/logo_orange.png")

if __name__ == "__main__":
    create_orange_logo()
