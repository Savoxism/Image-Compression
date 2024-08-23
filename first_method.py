from PIL import Image
import numpy as np
from collections import Counter

class ColorAnalyzer:
    def __init__(self, img):
        self.img = img.convert('RGB')
        self.width, self.height = self.img.size

    def most_common_colors(self, num_colors=10):
        img_array = np.array(self.img)
        reshaped_img = img_array.reshape(-1, 3)

        # Convert each pixel to a tuple (so it's hashable)
        pixel_tuples = [tuple(pixel) for pixel in reshaped_img]

        # Count occurrences of each color
        color_counts = Counter(pixel_tuples)

        # Get the top 'num_colors' most common colors
        most_common = color_counts.most_common(num_colors)

        # Convert to hex codes
        cluster_hex_codes = ["#{:02x}{:02x}{:02x}".format(r, g, b) for (r, g, b), _ in most_common]

        return cluster_hex_codes

