import random
from loguru import logger

from app.engine.aspose_slides import Color

class ColorManager:
    def __init__(self, coloring_background: bool = False):
        self.reset()
        self.coloring_background = coloring_background

    def get_color(self):
        """生成随机不重复的颜色。"""
        color_range = [[1, 1, 1], [254, 254, 254]]

        def generate_color():
            r_l = min([color_range[0][0], color_range[1][0]])
            r_r = max(color_range[0][0], color_range[1][0])
            r = random.randint(r_l, r_r)

            g_l = min([color_range[0][1], color_range[1][1]])
            g_r = max(color_range[0][1], color_range[1][1])
            g = random.randint(g_l, g_r)

            b_l = min([color_range[0][2], color_range[1][2]])
            b_r = max(color_range[0][2], color_range[1][2])
            b = random.randint(b_l, b_r)
            return (r, g, b)

        color = generate_color()
        n = 0
        while color in self.used_colors:
            color = generate_color()
            n += 1
            if n > 10:
                logger.error("Too many paragraphs lead to the exhaustion of colors.")
                break
        self.used_colors.add(color)

        return Color(*color)

    def reset(self):
        self.used_colors = set()
