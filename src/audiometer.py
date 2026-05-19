"""Audio meter visualization widget using gradient canvas."""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class GradientAudioMeter(ttk.Canvas):
    """A vertical audio meter using a canvas to reveal a static gradient."""

    def __init__(self, master, width=20, height=200, bg_color="#121212", **kwargs):
        """Initialize gradient audio meter."""
        super().__init__(
            master,
            width=width,
            height=height,
            bg=bg_color,
            highlightthickness=0,
            **kwargs,
        )
        self.width = width
        self.height = height
        # Define color zones (start_percent, end_percent, hex_color)
        self.zones = [
            (0.0, 0.60, "#00FF00"),  # Neon Green (Bottom 60%)
            (0.60, 0.85, "#FFFF00"),  # Bright Yellow (Next 25%)
            (0.85, 1.00, "#FF0000"),  # Bright Red (Top 15%)
        ]
        self._draw_static_gradient()
        self.mask_id = None
        self.set_level(0)

    def _draw_static_gradient(self):
        """Draws the permanent multi-color background gradient."""
        for start_pct, end_pct, color in self.zones:
            # Calculate Y coordinates for this zone (inverted for canvas)
            y_start = self.height * (1.0 - end_pct)
            y_end = self.height * (1.0 - start_pct)

            self.create_rectangle(
                0, y_start, self.width, y_end, fill=color, outline=color, tags="gradient"
            )

    def set_level(self, value_0_to_100):
        """Updates the black mask to reveal the gradient."""
        # Ensure value is between 0 and 100
        val = max(0, min(100, value_0_to_100))

        # Calculate the Y position where the colored part should end
        visible_height = (val / 100.0) * self.height
        target_y = self.height - visible_height

        # Remove previous mask
        if self.mask_id:
            self.delete(self.mask_id)

        mask_color = "#2b2b2b"  # Dark gray to match the background

        self.mask_id = self.create_rectangle(
            0, 0, self.width, target_y, fill=mask_color, outline=mask_color, tags="mask"
        )
