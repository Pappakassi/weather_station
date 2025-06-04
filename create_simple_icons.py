#!/usr/bin/env python3
"""
Simple icon generator for the Weather Station PWA
Generates PNG icons in various sizes needed for PWA installation
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_weather_icon(size, filename):
    """Create a weather-themed icon with gradient background"""
    
    # Create image with RGBA mode for transparency support
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background (blue to purple)
    for y in range(size):
        # Calculate color based on position
        ratio = y / size
        r = int(76 + (123 - 76) * ratio)    # 76 -> 123 (blue to purple red)
        g = int(154 + (104 - 154) * ratio)  # 154 -> 104 (blue to purple green) 
        b = int(255 + (238 - 255) * ratio)  # 255 -> 238 (blue to purple blue)
        
        draw.line([(0, y), (size, y)], fill=(r, g, b, 255))
    
    # Add weather symbol (sun/cloud emoji substitute)
    if size >= 64:
        # Draw a simple sun icon
        center = size // 2
        sun_radius = size // 6
        
        # Sun circle
        draw.ellipse([
            center - sun_radius, center - sun_radius,
            center + sun_radius, center + sun_radius
        ], fill=(255, 255, 255, 255))
        
        # Sun rays
        ray_length = size // 12
        for angle in range(0, 360, 45):
            import math
            x1 = center + (sun_radius + 5) * math.cos(math.radians(angle))
            y1 = center + (sun_radius + 5) * math.sin(math.radians(angle))
            x2 = center + (sun_radius + 5 + ray_length) * math.cos(math.radians(angle))
            y2 = center + (sun_radius + 5 + ray_length) * math.sin(math.radians(angle))
            draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 255), width=2)
    
    # Add "ÓB" text for larger icons
    if size >= 128:
        try:
            # Try to use a nice font, fall back to default
            font_size = size // 8
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        text = "ÓB"
        # Get text bounding box
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position text at bottom center
        text_x = (size - text_width) // 2
        text_y = size - text_height - size // 10
        
        draw.text((text_x, text_y), text, fill=(255, 255, 255, 220), font=font)
    
    # Save the image
    img.save(filename, 'PNG', optimize=True)
    print(f"Created {filename} ({size}x{size})")

def main():
    """Generate all required PWA icons"""
    # Create static/images directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Define required icon sizes and filenames
    icons = [
        (192, 'static/images/icon-192.png'),
        (512, 'static/images/icon-512.png'),
        (180, 'static/images/apple-touch-icon.png'),
        (32, 'static/images/favicon-32x32.png'),
        (16, 'static/images/favicon-16x16.png'),
    ]
    
    print("Generating PWA icons for Veðrið hjá Óla Bj...")
    
    for size, filename in icons:
        create_weather_icon(size, filename)
    
    print("\n✅ All PWA icons generated successfully!")
    print("Your weather station is now ready to be installed as a PWA!")

if __name__ == "__main__":
    main() 