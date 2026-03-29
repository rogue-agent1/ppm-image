#!/usr/bin/env python3
"""ppm_image - PPM/PGM image creation and manipulation (no deps)."""
import sys, math

class Image:
    def __init__(self, width, height, fill=(0,0,0)):
        self.w = width
        self.h = height
        self.pixels = [[fill for _ in range(width)] for _ in range(height)]
    
    def set_pixel(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.pixels[y][x] = color
    
    def get_pixel(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.pixels[y][x]
        return (0,0,0)
    
    def fill_rect(self, x, y, w, h, color):
        for dy in range(h):
            for dx in range(w):
                self.set_pixel(x+dx, y+dy, color)
    
    def draw_line(self, x0, y0, x1, y1, color):
        dx, dy = abs(x1-x0), abs(y1-y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy; x0 += sx
            if e2 < dx:
                err += dx; y0 += sy
    
    def draw_circle(self, cx, cy, r, color):
        x, y = r, 0
        err = 1 - r
        while x >= y:
            for dx, dy in [(x,y),(-x,y),(x,-y),(-x,-y),(y,x),(-y,x),(y,-x),(-y,-x)]:
                self.set_pixel(cx+dx, cy+dy, color)
            y += 1
            if err < 0:
                err += 2*y + 1
            else:
                x -= 1
                err += 2*(y-x) + 1
    
    def grayscale(self):
        img = Image(self.w, self.h)
        for y in range(self.h):
            for x in range(self.w):
                r, g, b = self.pixels[y][x]
                v = int(0.299*r + 0.587*g + 0.114*b)
                img.pixels[y][x] = (v, v, v)
        return img
    
    def flip_h(self):
        img = Image(self.w, self.h)
        for y in range(self.h):
            img.pixels[y] = list(reversed(self.pixels[y]))
        return img
    
    def crop(self, x, y, w, h):
        img = Image(w, h)
        for dy in range(h):
            for dx in range(w):
                img.pixels[dy][dx] = self.get_pixel(x+dx, y+dy)
        return img
    
    def save_ppm(self, path):
        with open(path, "wb") as f:
            f.write(f"P6\n{self.w} {self.h}\n255\n".encode())
            for row in self.pixels:
                for r, g, b in row:
                    f.write(bytes([r, g, b]))
    
    @classmethod
    def load_ppm(cls, path):
        with open(path, "rb") as f:
            magic = f.readline().decode().strip()
            assert magic == "P6"
            line = f.readline().decode().strip()
            while line.startswith("#"):
                line = f.readline().decode().strip()
            w, h = map(int, line.split())
            maxval = int(f.readline().decode().strip())
            img = cls(w, h)
            for y in range(h):
                for x in range(w):
                    img.pixels[y][x] = tuple(f.read(3))
            return img

def test():
    img = Image(100, 100, (255, 255, 255))
    assert img.w == 100 and img.h == 100
    assert img.get_pixel(0, 0) == (255, 255, 255)
    
    img.set_pixel(50, 50, (255, 0, 0))
    assert img.get_pixel(50, 50) == (255, 0, 0)
    
    img.fill_rect(10, 10, 20, 20, (0, 255, 0))
    assert img.get_pixel(15, 15) == (0, 255, 0)
    
    img.draw_line(0, 0, 99, 99, (0, 0, 255))
    assert img.get_pixel(50, 50) == (0, 0, 255)
    
    img.draw_circle(50, 50, 30, (255, 255, 0))
    
    gray = img.grayscale()
    r, g, b = gray.get_pixel(0, 0)
    assert r == g == b
    
    flipped = img.flip_h()
    assert flipped.get_pixel(0, 0) == img.get_pixel(99, 0)
    
    cropped = img.crop(10, 10, 20, 20)
    assert cropped.w == 20 and cropped.h == 20
    
    # Save/load
    import tempfile, os
    tmp = tempfile.mktemp(suffix=".ppm")
    img.save_ppm(tmp)
    loaded = Image.load_ppm(tmp)
    assert loaded.w == 100 and loaded.h == 100
    assert loaded.get_pixel(15, 15) == img.get_pixel(15, 15)
    os.remove(tmp)
    
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: ppm_image.py test")
