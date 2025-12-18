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
        
        # Descriptions mapping (could be moved to separate file)
        self.rule_descriptions = {
            'oas3-schema': 'Object does not match the schema.',
            'oas3-valid-media-example': 'Examples must be valid against their defined schema.',
            'oas3-valid-schema-example': 'Schema examples must be valid against the schema.',
            'path-params': 'Path parameters must be defined and valid.',
            'operation-description': 'Operation must have a description.',
            'info-description': 'Info object must have a description.',
            'operation-tags': 'Operation should have tags.',
            'operation-operationId': 'Operation should have a unique operationId.',
            'typed-enum': 'Enum values must respect the specified type.',
            'no-unused-components': 'Component is defined but never used.',
            # Add more defaults/generic fallback
        }
        
        self.bind("<Configure>", self.draw)
        self.bind("<Map>", self.draw) # Ensure draw when mapped
        self.bind("<Visibility>", self.draw)
        self.canvas.bind("<Motion>", self.on_mouse_move)
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

    def draw(self, event=None):
        self.update_idletasks() # Force geometry update
        self.canvas.delete("all")
        self.canvas.delete("tooltip_tag") # clear tooltip
        self.slices = []
        
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w < 50 or h < 50: return

        padding = 20
        cx = w / 2
        cy = h / 2
        radius = min(w, h) / 2 - padding
        
        total = sum(d['count'] for d in self.data.values())
        
        if total == 0:
            self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill="#E0E0E0", outline="")
            self.canvas.create_text(cx, cy, text="No Data", fill="gray", font=("Arial", 12))
            return

        # Separate items by severity to generate gradients
        errors = {k:v for k,v in self.data.items() if v['severity'] == 'error'}
        warnings = {k:v for k,v in self.data.items() if v['severity'] == 'warning'}
        others = {k:v for k,v in self.data.items() if v['severity'] not in ('error', 'warning')}
        
        # Sort internal groups by count desc
        errors = dict(sorted(errors.items(), key=lambda item: item[1]['count'], reverse=True))
        warnings = dict(sorted(warnings.items(), key=lambda item: item[1]['count'], reverse=True))
        
        # Color Palettes
        # Red Hue = 0.0/1.0. Yellow/Gold Hue ~= 0.12
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
        
        for code, info, color in final_list:
            cnt = info['count']
            extent = (cnt / total) * 360
            
            tag = f"slice_{code}"
            self.canvas.create_arc(
                cx - radius, cy - radius, cx + radius, cy + radius,
                start=start_angle, extent=extent,
                fill=color, outline="white", width=1.5, tags=tag
            )
            
            self.slices.append({
                'start': start_angle % 360,
                'end': (start_angle + extent) % 360,
                'code': code,
                'count': cnt,
                'severity': info['severity'],
                'cx': cx, 'cy': cy, 'r': radius,
                'color': color
            })
            
            start_angle += extent

    def on_mouse_move(self, event):
        x, y = event.x, event.y
        hovered = None
        for s in self.slices:
            dx = x - s['cx']
            dy = s['cy'] - y 
            dist = math.sqrt(dx*dx + dy*dy)
            if dist <= s['r']:
                angle = math.degrees(math.atan2(dy, dx))
                if angle < 0: angle += 360
                start, end = s['start'], s['end']
                
                # Check angle
                if start < end:
                    if start <= angle <= end: hovered = s
                else:
                    if angle >= start or angle <= end: hovered = s
                if hovered: break
        
        if hovered: self.show_tooltip(x, y, hovered)
        else: self.hide_tooltip()

    def show_tooltip(self, x, y, slice_data):
        code = slice_data['code']
        desc = self.rule_descriptions.get(code, "No description available.")
        
        text = f"{code}\n"
        text += f"Severity: {slice_data['severity'].upper()}\n"
        text += f"Count: {slice_data['count']}\n"
        text += f"----------------\n{desc}"
        
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
