import customtkinter as ctk
import tkinter as tk
import math

class PieChart(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.canvas = tk.Canvas(self, bg=self._apply_appearance_mode(self._fg_color), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Colors for severity
        self.colors = {
            'error': '#FF4444',   # Red
            'warning': '#FFBB33', # Orange/Yellow
            'info': '#33B5E5',    # Blue
            'hint': '#00C851',    # Green
            'empty': '#CCCCCC'    # Grey
        }
        
    def _get_color(self, key):
        if key in self.colors: return self.colors[key]
        # Generate hash-based pastel color for unknown keys
        import hashlib
        h = hashlib.md5(str(key).encode()).hexdigest()
        r = int(h[0:2], 16) % 127 + 128
        g = int(h[2:4], 16) % 127 + 128
        b = int(h[4:6], 16) % 127 + 128
        return f'#{r:02x}{g:02x}{b:02x}'
        
        self.data = {}
        self.bind("<Configure>", self.draw)

    def set_data(self, data):
        """
        Sets data for the chart.
        Args:
            data (dict): {'error': 10, 'warning': 5, ...}
        """
        self.data = data
        self.draw()

    def draw(self, event=None):
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width < 10 or height < 10:
            return

        x = width // 2
        y = height // 2
        radius = min(width, height) // 2 - 20
        
        total = sum(self.data.values())
        
        # If no data, draw empty circle
        if total == 0:
            self.canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=self.colors['empty'], outline=""
            )
            self.canvas.create_text(x, y, text="No Data", fill="black")
            return

        start_angle = 90
        
        for category, value in self.data.items():
            if value == 0:
                continue
                
            extent = (value / total) * 360
            extent = (value / total) * 360
            color = self._get_color(category)
            
            self.canvas.create_arc(
                x - radius, y - radius, x + radius, y + radius,
                start=start_angle, extent=extent,
                fill=color, outline="white", width=2
            )
            
            # Draw Labels (simple placement)
            if extent > 15: # Only label if slice is big enough
                mid_angle = math.radians(start_angle + extent / 2)
                label_r = radius * 0.6
                text_x = x + label_r * math.cos(mid_angle)
                text_y = y - label_r * math.sin(mid_angle) # Y is inverted in canvas
                
                self.canvas.create_text(
                    text_x, text_y,
                    text=str(value), fill="white", font=("Arial", 10, "bold")
                )
            
            start_angle += extent
