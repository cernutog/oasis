"""
Splash Screen for OASIS - OAS Integration Suite.
Logo integrated as the 'O' in OASIS with matching rounded font.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import sys
import time

try:
    from src.version import VERSION
except ImportError:
    from version import VERSION


def remove_background(img, threshold=220):
    """Remove light background from image, making it transparent."""
    img = img.convert("RGBA")
    data = img.getdata()
    
    new_data = []
    for item in data:
        # If pixel is near-white or light gray, make transparent
        if item[0] > threshold and item[1] > threshold and item[2] > threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    
    img.putdata(new_data)
    return img


class SplashScreen:
    """Professional splash with logo integrated as 'O' in OASIS."""
    
    def __init__(self, root=None, wait_for_click=False):
        self.wait_for_click = wait_for_click
        self.clicked = False
        
        if root:
            self.root = tk.Toplevel(root)
            self.is_toplevel = True
        else:
            self.root = tk.Tk()
            self.is_toplevel = False
            
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        splash_width = 580
        splash_height = 400
        
        x = (screen_width - splash_width) // 2
        y = (screen_height - splash_height) // 2
        self.root.geometry(f"{splash_width}x{splash_height}+{x}+{y}")
        
        # Colors
        self.accent = '#0891B2'
        self.text_dark = '#0F172A'
        self.text_secondary = '#475569'
        self.shadow = '#94A3B8'
        
        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=splash_width,
            height=splash_height,
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Gradient background
        self._draw_gradient(splash_width, splash_height)
        
        # Border
        self._draw_border(splash_width, splash_height)
        
        # Click binding
        self.root.bind('<Button-1>', self._on_click)
        self.canvas.bind('<Button-1>', self._on_click)
        
        self.images = {}
        
        # Draw the integrated OASIS with logo as O
        self._draw_oasis_with_logo(splash_width)
        
        # Subtitle
        self.canvas.create_text(
            splash_width // 2,
            215,  # Lifted from 255 to align with new layout
            text="OAS Integration Suite",
            font=('Segoe UI', 15),
            fill=self.text_secondary
        )
        
        # Progress bar
        self.progress_y = 320
        self._draw_progress_bar(splash_width)
        
        # Status
        self.status_id = self.canvas.create_text(
            splash_width // 2,
            self.progress_y + 35,
            text="",
            font=('Segoe UI', 9),
            fill=self.text_secondary
        )
        
        # Version
        self.version_id = self.canvas.create_text(
            splash_width // 2,
            splash_height - 15,
            text=f"v{VERSION}",
            font=('Segoe UI', 8),
            fill=self.shadow
        )
        
        # Hint
        self.hint_id = self.canvas.create_text(
            splash_width // 2,
            splash_height - 35,
            text="",
            font=('Segoe UI', 9, 'italic'),
            fill=self.shadow
        )
        
        self.root.update()
    
    def _draw_gradient(self, width, height):
        """Smooth gradient background."""
        for i in range(height):
            ratio = i / height
            r = int(248 + (226 - 248) * ratio)
            g = int(250 + (232 - 250) * ratio)
            b = int(252 + (240 - 252) * ratio)
            self.canvas.create_line(0, i, width, i, fill=f'#{r:02x}{g:02x}{b:02x}')
    
    def _draw_border(self, width, height):
        """Subtle border."""
        self.canvas.create_rectangle(0, 0, width-1, height-1, outline='#CBD5E1', width=1)
        self.canvas.create_line(1, 1, width-2, 1, fill='#FFFFFF')
        self.canvas.create_line(1, 1, 1, height-2, fill='#FFFFFF')
    
    def _draw_oasis_with_logo(self, width):
        """Draw OASIS with logo replacing the O."""
        # Load logo
        logo_loaded = False
        logo_size = 155  # Exaclty 155px to match User Guide
        
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            logo_path = os.path.join(base_path, 'src', 'resources', 'oasis_logo.png')
            
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                img = img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                img = remove_background(img, threshold=220)
                self.images['logo'] = ImageTk.PhotoImage(img)
                logo_loaded = True
        except Exception as e:
            print(f"Could not load logo: {e}")
        
        # Use lighter font to match the thin circle outline
        font_name = 'Segoe UI Light'
        font_size = 130  # Increased to 130px to match User Guide
        text_font = (font_name, font_size)
        
        # "ASIS" text (the part after the logo/O)
        asis_text = "ASIS"
        
        # Vertical center (Lifted from 145 to 130 to balance space)
        center_y = 130
        
        # Measure ASIS text width and get O width for reference
        temp_id = self.canvas.create_text(0, 0, text=asis_text, font=text_font)
        bbox = self.canvas.bbox(temp_id)
        self.canvas.delete(temp_id)
        asis_width = bbox[2] - bbox[0] if bbox else 200
        asis_height = bbox[3] - bbox[1] if bbox else 90
        
        # Measure "O" to get natural letter spacing
        temp_o = self.canvas.create_text(0, 0, text="O", font=text_font)
        bbox_o = self.canvas.bbox(temp_o)
        self.canvas.delete(temp_o)
        o_width = bbox_o[2] - bbox_o[0] if bbox_o else 80
        
        # Kerning: Fixed at 35px to match HTML "margin-right: -35px" style
        # In HTML we pull them closer. Here we calculate Position = start_x + logo - kerning.
        # However, HTML logic was "Logo margin-right: -35px".
        # Meaning the Text starts 35px BEFORE the Logo ends? 
        # No, margin-right on Logo pulls the NEXT element left.
        # So Text Start = Logo End - 35. This means OVERLAP.
        # let's try kerning = 35 (overlap).
        kerning = 35 
        
        # Total visual width of logo + ASIS (Logo Width + Text Width - Overlap)
        total_width = logo_size + asis_width - kerning
        
        # Center the whole thing
        # Apply +20px visual offset (Right) to compensate for the wide Logo ('O')
        # pulling the geometric center to the left.
        start_x = (width - total_width) // 2 + 20
        
        # Position logo
        logo_center_x = start_x + logo_size // 2
        
        # Draw logo as O
        # Apply visual offset: 
        # Y: Moved UP by 6px from previous (+8) -> Net +2
        # X: Moved RIGHT by 2px
        logo_visual_y = center_y + 2
        logo_visual_x = logo_center_x + 2
        
        if logo_loaded:
            self.canvas.create_image(
                logo_visual_x,
                logo_visual_y,
                image=self.images['logo'],
                anchor='center'
            )
        else:
            # Fallback: draw O
            self.canvas.create_text(
                logo_center_x,
                center_y,
                text="O",
                font=text_font,
                fill=self.accent
            )
        
        # Position ASIS right after logo with natural spacing
        asis_x = start_x + logo_size - kerning
        
        # Create gradient text image
        try:
            gradient_img = self._create_gradient_text(
                asis_text, 
                asis_width + 20, 
                asis_height + 20,
                font_size
            )
            self.images['asis'] = ImageTk.PhotoImage(gradient_img)
            
            # Draw gradient text
            self.canvas.create_image(
                asis_x,
                center_y,
                image=self.images['asis'],
                anchor='w'
            )
        except Exception as e:
            # Fallback to regular text if gradient fails
            print(f"Gradient text failed: {e}")
            self.canvas.create_text(
                asis_x,
                center_y,
                text=asis_text,
                font=text_font,
                fill=self.accent,
                anchor='w'
            )
    
    def _create_gradient_asis(self, font, text_w, text_h, bbox):
        """Create gradient ASIS text image."""
        # Create image exact size of text
        img = Image.new('RGBA', (text_w, text_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw text in white (mask)
        x = -bbox[0]
        y = -bbox[1]
        draw.text((x, y), "ASIS", font=font, fill=(255, 255, 255, 255))
        
        # Apply diagonal gradient
        gradient = Image.new('RGBA', (text_w, text_h), (0, 0, 0, 0))
        color_sw = (5, 90, 120)
        color_ne = (40, 200, 220)
        
        for i in range(text_h):
            for j in range(text_w):
                alpha = img.getpixel((j, i))[3]
                if alpha > 0:
                    ratio = (j / text_w + (1 - i / text_h)) / 2
                    r = int(color_sw[0] + (color_ne[0] - color_sw[0]) * ratio)
                    g = int(color_sw[1] + (color_ne[1] - color_sw[1]) * ratio)
                    b = int(color_sw[2] + (color_ne[2] - color_sw[2]) * ratio)
                    gradient.putpixel((j, i), (r, g, b, alpha))
        
        return gradient
    
    def _create_gradient_text_tight(self, text, font_size):
        """Create gradient text with minimal padding."""
        # Load font
        try:
            font_path = "C:/Windows/Fonts/segoeuil.ttf"
            if not os.path.exists(font_path):
                font_path = "C:/Windows/Fonts/segoeui.ttf"
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Measure text precisely
        temp_img = Image.new('RGBA', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Create image with exact text size (minimal padding)
        pad = 2
        img_width = text_width + pad * 2
        img_height = text_height + pad * 2
        
        img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Draw text at correct position (accounting for bbox offset)
        x = pad - bbox[0]
        y = pad - bbox[1]
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        # Apply diagonal gradient
        gradient = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        color_sw = (5, 90, 120)
        color_ne = (40, 200, 220)
        
        for i in range(img_height):
            for j in range(img_width):
                alpha = img.getpixel((j, i))[3]
                if alpha > 0:
                    rel_x = j / img_width
                    rel_y = i / img_height
                    ratio = (rel_x + (1 - rel_y)) / 2
                    r = int(color_sw[0] + (color_ne[0] - color_sw[0]) * ratio)
                    g = int(color_sw[1] + (color_ne[1] - color_sw[1]) * ratio)
                    b = int(color_sw[2] + (color_ne[2] - color_sw[2]) * ratio)
                    gradient.putpixel((j, i), (r, g, b, alpha))
        
        return gradient
    
    def _create_gradient_text(self, text, img_width, img_height, font_size):
        """Create gradient text image matching logo colors."""
        # Create transparent image
        img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Try to load Segoe UI Light font
        try:
            # Windows font path
            font_path = "C:/Windows/Fonts/segoeuil.ttf"  # Segoe UI Light
            if not os.path.exists(font_path):
                font_path = "C:/Windows/Fonts/segoeui.ttf"  # Fallback to regular
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Get text bounding box for centering
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        
        # Position text
        x = 5
        y = (img_height - text_h) // 2 - text_bbox[1]
        
        # Draw text in white first (will be used as mask)
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
        # Find actual text bounds (non-transparent pixels)
        min_x, min_y, max_x, max_y = img_width, img_height, 0, 0
        for py in range(img_height):
            for px in range(img_width):
                if img.getpixel((px, py))[3] > 0:
                    min_x = min(min_x, px)
                    min_y = min(min_y, py)
                    max_x = max(max_x, px)
                    max_y = max(max_y, py)
        
        text_width = max_x - min_x if max_x > min_x else img_width
        text_height = max_y - min_y if max_y > min_y else img_height
        
        # Create gradient overlay (diagonal SW→NE like logo)
        gradient = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        
        # Gradient colors - wider range for VISIBLE effect (SW darker → NE lighter)
        color_sw = (5, 90, 120)        # Dark teal (bottom-left) 
        color_ne = (40, 200, 220)      # Light cyan (top-right)
        
        # Diagonal gradient: calculate ratio based on TEXT BOUNDS, not image bounds
        for i in range(img_height):
            for j in range(img_width):
                if img.getpixel((j, i))[3] > 0:  # If not transparent
                    # Calculate position relative to text bounds (0-1 range)
                    rel_x = (j - min_x) / text_width if text_width > 0 else 0.5
                    rel_y = (i - min_y) / text_height if text_height > 0 else 0.5
                    # Diagonal ratio: 0 at SW (rel_x=0, rel_y=1), 1 at NE (rel_x=1, rel_y=0)
                    ratio = (rel_x + (1 - rel_y)) / 2
                    r = int(color_sw[0] + (color_ne[0] - color_sw[0]) * ratio)
                    g = int(color_sw[1] + (color_ne[1] - color_sw[1]) * ratio)
                    b = int(color_sw[2] + (color_ne[2] - color_sw[2]) * ratio)
                    gradient.putpixel((j, i), (r, g, b, img.getpixel((j, i))[3]))
        
        return gradient
    
    def _create_gradient_text_per_letter(self, text, img_width, img_height, font_size):
        """Create gradient text with gradient applied PER LETTER."""
        # Create transparent image
        final_img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        
        # Try to load Segoe UI Light font
        try:
            font_path = "C:/Windows/Fonts/segoeuil.ttf"
            if not os.path.exists(font_path):
                font_path = "C:/Windows/Fonts/segoeui.ttf"
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()
        
        # Gradient colors
        color_sw = (5, 90, 120)        # Dark teal (bottom-left) 
        color_ne = (40, 200, 220)      # Light cyan (top-right)
        
        # Draw each letter with its own gradient
        temp_draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))  # For measuring
        
        # Calculate total width
        total_text_width = 0
        letter_widths = []
        for letter in text:
            bbox = temp_draw.textbbox((0, 0), letter, font=font)
            w = bbox[2] - bbox[0]
            letter_widths.append(w)
            total_text_width += w
        
        # Starting position (centered)
        current_x = (img_width - total_text_width) // 2
        y_offset = img_height // 4  # Approximate vertical centering
        
        for idx, letter in enumerate(text):
            letter_width = letter_widths[idx]
            letter_height = img_height
            
            # Create letter image
            letter_img = Image.new('RGBA', (letter_width + 10, letter_height), (0, 0, 0, 0))
            letter_draw = ImageDraw.Draw(letter_img)
            
            # Draw letter in white
            bbox = letter_draw.textbbox((0, 0), letter, font=font)
            lx = 5
            ly = y_offset - bbox[1]
            letter_draw.text((lx, ly), letter, font=font, fill=(255, 255, 255, 255))
            
            # Find letter bounds
            min_x, min_y, max_x, max_y = letter_width + 10, letter_height, 0, 0
            for py in range(letter_height):
                for px in range(letter_width + 10):
                    if letter_img.getpixel((px, py))[3] > 0:
                        min_x = min(min_x, px)
                        min_y = min(min_y, py)
                        max_x = max(max_x, px)
                        max_y = max(max_y, py)
            
            lw = max_x - min_x if max_x > min_x else 1
            lh = max_y - min_y if max_y > min_y else 1
            
            # Apply gradient to this letter
            for py in range(letter_height):
                for px in range(letter_width + 10):
                    alpha = letter_img.getpixel((px, py))[3]
                    if alpha > 0:
                        # Calculate ratio relative to THIS LETTER's bounds
                        rel_x = (px - min_x) / lw
                        rel_y = (py - min_y) / lh
                        ratio = (rel_x + (1 - rel_y)) / 2
                        r = int(color_sw[0] + (color_ne[0] - color_sw[0]) * ratio)
                        g = int(color_sw[1] + (color_ne[1] - color_sw[1]) * ratio)
                        b = int(color_sw[2] + (color_ne[2] - color_sw[2]) * ratio)
                        letter_img.putpixel((px, py), (r, g, b, alpha))
            
            # Paste letter into final image
            final_img.paste(letter_img, (current_x, 0), letter_img)
            current_x += letter_width
        
        return final_img
    
    def _draw_progress_bar(self, width):
        """Custom progress bar."""
        bar_width = 400
        bar_height = 8
        x1 = (width - bar_width) // 2
        y1 = self.progress_y
        
        self.bg_bar_id = self.canvas.create_rectangle(
            x1, y1, x1 + bar_width, y1 + bar_height,
            fill='#E2E8F0', outline='#CBD5E1', width=1
        )
        
        self.progress_bar = self.canvas.create_rectangle(
            x1 + 1, y1 + 1, x1 + 1, y1 + bar_height - 1,
            fill=self.accent, outline=''
        )
        
        self.bar_x1 = x1 + 1
        self.bar_y1 = y1 + 1
        self.bar_y2 = y1 + bar_height - 1
        self.bar_max_width = bar_width - 2
    
    def _on_click(self, event):
        self.clicked = True
    
    def update_progress(self, value, status_text=None):
        fill_width = int((value / 100) * self.bar_max_width)
        self.canvas.coords(
            self.progress_bar,
            self.bar_x1, self.bar_y1,
            self.bar_x1 + fill_width, self.bar_y2
        )
        if status_text:
            self.canvas.itemconfig(self.status_id, text=status_text)
        self.root.update()
    
    def set_about_mode(self, version_text, description):
        """Configure splash screen for 'About' dialog specific layout."""
        # Hide progress elements and bottom version
        self.canvas.itemconfigure(self.progress_bar, state='hidden')
        self.canvas.itemconfigure(self.bg_bar_id, state='hidden')
        self.canvas.itemconfigure(self.hint_id, state='hidden')
        self.canvas.itemconfigure(self.version_id, state='hidden') # Hide bottom version
        
        # Move Status to center and restyle for Version
        self.canvas.itemconfigure(self.status_id, state='hidden')
        
        # Center coordinates
        center_x = self.root.winfo_width() // 2
        
        # Draw Version (Smaller, Normal Weight, Gray, Closer to Title)
        self.canvas.create_text(
            center_x, 250,  # Lifted to 250 (below 215 subtitle)
            text=version_text,
            font=('Segoe UI', 11),
            fill='#64748B',
            anchor='center'
        )
        
        # Draw Description (Clean, Spaced)
        self.canvas.create_text(
            center_x, 310,  # Lifted to 310
            text=description,
            font=('Segoe UI', 10),
            fill='#64748B',
            anchor='center',
            justify='center'
        )

    def wait_for_user_click(self):
        self.canvas.itemconfig(self.hint_id, text="Click anywhere to continue...")
        self.root.update()
        while not self.clicked:
            self.root.update()
            time.sleep(0.05)
    
    def close(self):
        self.root.destroy()


def show_splash_and_load_app(debug_mode=False):
    """Show splash and load main app using single-root architecture."""
    try:
        from src.gui import OASGenApp
    except ImportError:
        from gui import OASGenApp
    
    # 1. Create App first (The Single Root)
    # Note: OASGenApp is a CTk/Tk root. 
    # Use alpha=0 to hide it effectively without removing it from window manager geometry calculation
    app = OASGenApp()
    app.attributes('-alpha', 0.0)
    
    # 2. Create Splash as Toplevel of App
    splash = SplashScreen(root=app, wait_for_click=debug_mode)
    
    stages = [
        (10, "Initializing..."),
        (25, "Loading UI framework..."),
        (40, "Loading parsers..."),
        (55, "Loading generators..."),
        (70, "Loading validators..."),
        (85, "Preparing workspace..."),
        (95, "Almost ready..."),
    ]
    
    for progress, status in stages:
        splash.update_progress(progress, status)
        time.sleep(0.1)
    
    import customtkinter as ctk
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    splash.update_progress(100, "Starting OASIS...")
    time.sleep(0.15)
    
    # 3. Show App Window (Gapless transition)
    # Ensure geometry is calculated
    app.update_idletasks()
    
    # Reveal app
    app.attributes('-alpha', 1.0)
    app.deiconify() # Just in case it was iconified or hidden by system
    
    # 4. Destroy Splash
    splash.close()
    
    # 5. Focus
    app.lift()
    
    return app


if __name__ == "__main__":
    splash = SplashScreen(wait_for_click=True)
    for i in range(0, 101, 5):
        splash.update_progress(i, f"Loading... {i}%")
        time.sleep(0.06)
    splash.wait_for_user_click()
    splash.close()
