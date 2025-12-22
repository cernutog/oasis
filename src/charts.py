import customtkinter as ctk
import tkinter as tk
import math
import colorsys

class SemanticPieChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.canvas = tk.Canvas(self, bg=self._apply_appearance_mode(self._fg_color), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.data = {}
        self.slices = [] 
        
import webbrowser
from src.rules_data import SPECTRAL_RULES

class SemanticPieChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.canvas = tk.Canvas(self, bg=self._apply_appearance_mode(self._fg_color), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.data = {}
        self.slices = [] 
        
        # Use imported rules
        self.rule_descriptions = SPECTRAL_RULES
        
        self.bind("<Configure>", self.draw)
        self.bind("<Map>", self.draw) # Ensure draw when mapped
        self.bind("<Visibility>", self.draw)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Click to open URL
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.canvas.bind("<Leave>", self.hide_tooltip)

    def set_data(self, code_summary):
        self.data = code_summary
        self.draw()

    def _generate_hsl_gradient(self, base_hue, num_colors):
        """
        Generates 'num_colors' variations centered around a base hue.
        base_hue: 0.0=Red, 0.14=Yellow/Gold
        We want Full Red/Yellow as median.
        Variation: Lightness and Saturation.
        """
        colors = []
        if num_colors == 0: return []
        if num_colors == 1:
            # Return the "Full" base color
            rgb = colorsys.hls_to_rgb(base_hue, 0.5, 1.0)
            return [f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}']
            
        # Distribute lightness around 0.5 (Normal)
        # e.g. 3 colors -> 0.4, 0.5, 0.6
        # Limit to 0.3 (Dark) - 0.8 (Pastel)
        step = 0.4 / max(num_colors - 1, 1)
        start_l = 0.3
        
        for i in range(num_colors):
            l = start_l + (i * step)
            # Clip
            l = max(0.2, min(0.9, l))
            
            # Convert HLS (Hue, Lightness, Saturation) to RGB
            rgb = colorsys.hls_to_rgb(base_hue, l, 1.0) # Full Saturation
            hex_c = f'#{int(rgb[0]*255):02x}{int(rgb[1]*255):02x}{int(rgb[2]*255):02x}'
            colors.append(hex_c)
            
        return list(reversed(colors)) # Dark to Light

    def _darken_color(self, hex_color, factor=0.7):
        """ Darkens a hex color for 3D shadowing. """
        if not hex_color.startswith('#'): return hex_color
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))
            
            return f'#{r:02x}{g:02x}{b:02x}'
        except:
            return hex_color

    def draw(self, event=None):
        self.update_idletasks() # Force geometry update
        self.canvas.delete("all")
        self.canvas.delete("tooltip_tag") # clear tooltip
        self.slices = []
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 50 or h < 50: return

        padding = 20
        depth = 25 # 3D Depth (Increased)
        
        # Center and Radii (Elliptical 3D)
        cx = w / 2
        cy = (h / 2) - (depth / 2)
        rx = min(w, h) / 2 - padding
        ry = rx * 0.6 # Flatten
        
        total = sum(d['count'] for d in self.data.values())
        
        if total == 0:
            # Clean, simple Unicode Checkmark (as requested)
            cx = w / 2
            cy = h / 2
            
            # Using a large font size for the checkmark
            # "✔" U+2714 HEAVY CHECK MARK
            self.canvas.create_text(cx, cy, text="✔", fill="#2e7d32", font=("Segoe UI Symbol", 100))
            return

        # Separate items by severity to generate gradients
        errors = {k:v for k,v in self.data.items() if v['severity'] == 'error'}
        warnings = {k:v for k,v in self.data.items() if v['severity'] == 'warning'}
        others = {k:v for k,v in self.data.items() if v['severity'] not in ('error', 'warning')}
        
        # Sort internal groups by count desc
        errors = dict(sorted(errors.items(), key=lambda item: item[1]['count'], reverse=True))
        warnings = dict(sorted(warnings.items(), key=lambda item: item[1]['count'], reverse=True))
        
        # Color Palettes
        err_colors = self._generate_hsl_gradient(0.0, len(errors))
        warn_colors = self._generate_hsl_gradient(0.13, len(warnings)) # 0.13 is nice gold/amber
        other_colors = self._generate_hsl_gradient(0.55, len(others)) # Blueish

        # Combine for drawing order: Errors -> Warnings -> Others
        final_list = []
        
        i = 0
        for code, info in errors.items():
            final_list.append((code, info, err_colors[i]))
            i+=1
            
        i = 0
        for code, info in warnings.items():
            final_list.append((code, info, warn_colors[i]))
            i+=1

        i = 0
        for code, info in others.items():
            final_list.append((code, info, other_colors[i]))
            i+=1
            
        start_angle = 90
        
        # 1. Prepare Data
        slices_meta = []
        for code, info, color in final_list:
            cnt = info['count']
            extent = (cnt / total) * 360
            if extent < 1: extent = 1 # Min visibility
            
            # Special handling for Full Circle (single slice)
            is_full = (extent >= 359.9)
            
            slices_meta.append({
                'code': code, 'info': info, 'color': color,
                'dark_color': self._darken_color(color, 0.7),
                'start': start_angle, 'extent': extent,
                'is_full': is_full
            })
            start_angle += extent
            
        # 2. Draw Depth (Sides)
        # For full circle, we just need a cylinder background
        if len(slices_meta) == 1 and slices_meta[0]['is_full']:
            s = slices_meta[0]
            # Draw bottom oval (dark)
            self.canvas.create_oval(
                cx - rx, cy - ry + depth, cx + rx, cy + ry + depth,
                fill=s['dark_color'], outline=""
            )
            # Draw rectangle body (simplified cylinder side view)
            self.canvas.create_rectangle(
                cx - rx, cy, cx + rx, cy + depth,
                fill=s['dark_color'], outline=""
            )
        else:
            # Standard Slice Depth
            for z in range(depth, 0, -1):
                 for s in slices_meta:
                     self.canvas.create_arc(
                         cx - rx, cy - ry + z, cx + rx, cy + ry + z,
                         start=s['start'], extent=s['extent'],
                         fill=s['dark_color'], outline=s['dark_color'], width=1, style="pieslice"
                     )

        # 3. Draw Top Face
        for s in slices_meta:
            s_angle = s['start']
            e_angle = s['extent']
            actual_end = (s_angle + e_angle) % 360
            
            tag = f"slice_{s['code']}"
            
            if s['is_full']:
                # Draw OVAL to avoid seam line
                self.canvas.create_oval(
                     cx - rx, cy - ry, cx + rx, cy + ry,
                     fill=s['color'], outline="black", width=1.5, tags=tag
                )
            else:
                self.canvas.create_arc(
                    cx - rx, cy - ry, cx + rx, cy + ry,
                    start=s_angle, extent=e_angle,
                    fill=s['color'], outline="black", width=1.5, tags=tag
                )
            
            self.slices.append({
                'start': s_angle % 360,
                'end': actual_end,
                'code': s['code'],
                'count': s['info']['count'],
                'severity': s['info']['severity'],
                'cx': cx, 'cy': cy, 
                'rx': rx, 'ry': ry, # Elliptical
                'color': s['color'],
                'is_full': s['is_full']
            })

    def on_mouse_move(self, event):
        x, y = event.x, event.y
        hovered = None
        for s in self.slices:
            # Check for Full Circle first
            if s.get('is_full'):
                dx = x - s['cx']
                dy = s['cy'] - y
                norm_x = dx / s['rx']
                norm_y = dy / s['ry']
                if (norm_x*norm_x + norm_y*norm_y) <= 1.05:
                    hovered = s
                    break
            
            # Elliptical Hit Test
            dx = x - s['cx']
            dy = s['cy'] - y # Inverted Y in canvas
            
            norm_x = dx / s['rx']
            norm_y = dy / s['ry']
            
            dist_sq = norm_x*norm_x + norm_y*norm_y
            
            if dist_sq <= 1.05: # Allow small margin
                angle = math.degrees(math.atan2(norm_y, norm_x))
                if angle < 0: angle += 360
                
                start, end = s['start'], s['end']
                
                # Check angle
                if start < end:
                    if start <= angle <= end: hovered = s
                else:
                    if angle >= start or angle <= end: hovered = s
                if hovered: break
        
        if hovered: 
            self.show_tooltip(x, y, hovered)
            self.canvas.config(cursor="hand2")
        else: 
            self.hide_tooltip()
            self.canvas.config(cursor="arrow")

    def on_click(self, event):
        x, y = event.x, event.y
        # Reuse hit test logic (simplified)
        for s in self.slices:
            dx = x - s['cx']
            dy = s['cy'] - y
            norm_x = dx / s['rx']
            norm_y = dy / s['ry']
            dist_sq = norm_x*norm_x + norm_y*norm_y
            
            is_hit = False
            if s.get('is_full') and dist_sq <= 1.05:
                is_hit = True
            elif dist_sq <= 1.05:
                angle = math.degrees(math.atan2(norm_y, norm_x))
                if angle < 0: angle += 360
                start, end = s['start'], s['end']
                if start < end:
                     if start <= angle <= end: is_hit = True
                else:
                     if angle >= start or angle <= end: is_hit = True
            
            if is_hit:
                code = s['code']
                info = self.rule_descriptions.get(code)
                if info and info.get('url'):
                    webbrowser.open(info['url'])
                return

    def show_tooltip(self, x, y, slice_data):
        code = slice_data['code']
        rule_info = self.rule_descriptions.get(code, {})
        desc = rule_info.get('description', "No description available.")
        
        text = f"{code}\n"
        text += f"Severity: {slice_data['severity'].upper()}\n"
        text += f"Count: {slice_data['count']}\n"
        text += f"----------------\n{desc}\n"
        text += f"(Click to view docs)"
        
        tx = x + 20
        ty = y + 20
        tag = "tooltip_tag"
        self.canvas.delete(tag)
        
        # Shadow/Bg
        id_txt = self.canvas.create_text(tx + 5, ty + 5, text=text, anchor="nw", font=("Segoe UI", 9), fill="#202020", tags=tag)
        bbox = self.canvas.bbox(id_txt)
        x1, y1, x2, y2 = bbox
        self.canvas.create_rectangle(x1-5, y1-3, x2+5, y2+3, fill="#F9F9F9", outline="#707070", tags=(tag, "bg"))
        self.canvas.tag_raise(id_txt)

    def hide_tooltip(self, event=None):
        self.canvas.delete("tooltip_tag")
