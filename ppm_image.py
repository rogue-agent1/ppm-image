#!/usr/bin/env python3
"""PPM image creator and manipulator (no deps, raw pixel format)."""
import sys

class Image:
    def __init__(self, w, h, fill=(0,0,0)):
        self.w, self.h = w, h
        self.pixels = [[fill for _ in range(w)] for _ in range(h)]
    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h: self.pixels[y][x] = color
    def get_pixel(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h: return self.pixels[y][x]
        return None
    def fill_rect(self, x, y, w, h, color):
        for dy in range(h):
            for dx in range(w): self.set_pixel(x+dx, y+dy, color)
    def line(self, x0, y0, x1, y1, color):
        dx, dy = abs(x1-x0), abs(y1-y0)
        sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1: break
            e2 = 2 * err
            if e2 > -dy: err -= dy; x0 += sx
            if e2 < dx: err += dx; y0 += sy
    def to_ppm(self):
        lines = [f"P3\n{self.w} {self.h}\n255"]
        for row in self.pixels:
            lines.append(" ".join(f"{r} {g} {b}" for r, g, b in row))
        return "\n".join(lines) + "\n"
    def grayscale(self):
        img = Image(self.w, self.h)
        for y in range(self.h):
            for x in range(self.w):
                r, g, b = self.pixels[y][x]
                v = int(0.299*r + 0.587*g + 0.114*b)
                img.pixels[y][x] = (v, v, v)
        return img

def main():
    if len(sys.argv) < 2: print("Usage: ppm_image.py <demo|test>"); return
    if sys.argv[1] == "test":
        img = Image(10, 10, (255,255,255))
        assert img.get_pixel(0, 0) == (255,255,255)
        img.set_pixel(5, 5, (255, 0, 0))
        assert img.get_pixel(5, 5) == (255, 0, 0)
        assert img.get_pixel(-1, 0) is None
        img.fill_rect(0, 0, 3, 3, (0, 255, 0))
        assert img.get_pixel(2, 2) == (0, 255, 0)
        img.line(0, 0, 9, 9, (0, 0, 255))
        assert img.get_pixel(0, 0) == (0, 0, 255)
        ppm = img.to_ppm()
        assert ppm.startswith("P3"); assert "10 10" in ppm
        gray = img.grayscale()
        r, g, b = gray.get_pixel(0, 0)
        assert r == g == b
        print("All tests passed!")
    else:
        img = Image(20, 20, (0,0,0))
        img.fill_rect(2, 2, 16, 16, (255, 128, 0))
        img.line(0, 0, 19, 19, (255, 255, 255))
        print(img.to_ppm()[:200] + "...")

if __name__ == "__main__": main()
