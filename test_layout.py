"""
Test script to measure and verify splash screen layout dimensions.
This runs a Tkinter window and measures actual rendered dimensions.
"""
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import sys

def measure_layout():
    """Measure all layout elements and find correct values."""
    
    # Create hidden root for measurements
    root = tk.Tk()
    root.withdraw()
    
    # Canvas for text measurements
    canvas = tk.Canvas(root, width=600, height=400)
    
    # Configuration
    logo_size = 170
    splash_width = 580
    
    # Test different font sizes to find one that matches logo height visually
    print("=" * 60)
    print("MEASURING TEXT DIMENSIONS AT DIFFERENT FONT SIZES")
    print("=" * 60)
    print(f"Logo size: {logo_size}px")
    print()
    
    font_name = 'Segoe UI Light'
    
    results = []
    for font_size in range(100, 200, 10):
        text_font = (font_name, font_size)
        
        # Measure ASIS
        temp_id = canvas.create_text(0, 0, text="ASIS", font=text_font)
        bbox = canvas.bbox(temp_id)
        canvas.delete(temp_id)
        
        if bbox:
            asis_width = bbox[2] - bbox[0]
            asis_height = bbox[3] - bbox[1]
            
            results.append({
                'font_size': font_size,
                'width': asis_width,
                'height': asis_height,
                'diff': abs(asis_height - logo_size)
            })
            
            print(f"Font {font_size}pt: ASIS = {asis_width}w x {asis_height}h (diff from logo: {abs(asis_height - logo_size)}px)")
    
    # Find best match
    best = min(results, key=lambda x: x['diff'])
    
    print()
    print("=" * 60)
    print(f"BEST MATCH: {best['font_size']}pt -> height {best['height']}px (logo is {logo_size}px)")
    print("=" * 60)
    
    # Fine-tune around best match
    print()
    print("Fine-tuning:")
    fine_results = []
    for font_size in range(best['font_size'] - 10, best['font_size'] + 11):
        text_font = (font_name, font_size)
        temp_id = canvas.create_text(0, 0, text="ASIS", font=text_font)
        bbox = canvas.bbox(temp_id)
        canvas.delete(temp_id)
        
        if bbox:
            asis_height = bbox[3] - bbox[1]
            asis_width = bbox[2] - bbox[0]
            fine_results.append({
                'font_size': font_size,
                'width': asis_width,
                'height': asis_height,
                'diff': abs(asis_height - logo_size)
            })
            print(f"  {font_size}pt: {asis_width}w x {asis_height}h")
    
    optimal = min(fine_results, key=lambda x: x['diff'])
    
    print()
    print("=" * 60)
    print(f"OPTIMAL FONT SIZE: {optimal['font_size']}pt")
    print(f"  Text height: {optimal['height']}px")
    print(f"  Logo height: {logo_size}px")
    print(f"  Difference: {optimal['diff']}px")
    print("=" * 60)
    
    # Now calculate gap
    print()
    print("CALCULATING GAP:")
    
    # The gap should position ASIS right after the logo circle
    # Logo is centered, so right edge is at logo_center_x + logo_size/2
    # ASIS should start immediately after with minimal spacing
    
    # For visual balance with a circle, gap should be small (like 5-10px)
    recommended_gap = 8
    
    print(f"  Logo right edge offset from center: {logo_size // 2}px")
    print(f"  Recommended gap: {recommended_gap}px")
    
    # Total layout calculation
    total_width = logo_size + recommended_gap + optimal['width']
    start_x = (splash_width - total_width) // 2
    
    print()
    print("FINAL LAYOUT:")
    print(f"  Splash width: {splash_width}px")
    print(f"  Total content width: {total_width}px")
    print(f"  Start X: {start_x}px")
    print(f"  Logo center X: {start_x + logo_size // 2}px")
    print(f"  ASIS X: {start_x + logo_size + recommended_gap}px")
    
    root.destroy()
    
    return {
        'font_size': optimal['font_size'],
        'gap': recommended_gap,
        'text_height': optimal['height'],
        'text_width': optimal['width']
    }

if __name__ == "__main__":
    result = measure_layout()
    print()
    print("=" * 60)
    print("COPY THESE VALUES TO splash_screen.py:")
    print("=" * 60)
    print(f"font_size = {result['font_size']}")
    print(f"gap = {result['gap']}")
