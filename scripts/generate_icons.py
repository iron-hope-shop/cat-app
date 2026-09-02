import zlib
import struct
import math
import os

def create_png(width, height, get_pixel):
    # get_pixel(x, y) -> (r, g, b, a) values 0-255
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0) # Filter type 0 (None)
        for x in range(width):
            r, g, b, a = get_pixel(x, y)
            raw_data.extend((r, g, b, a))
    
    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = zlib.crc32(c) & 0xffffffff
        return struct.pack('>I', len(data)) + c + struct.pack('>I', crc)
    
    ihdr = struct.pack('>IIBBBBB', width, height, 8, 6, 0, 0, 0)
    idat = zlib.compress(bytes(raw_data), level=9)
    
    png = b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')
    return png

def render_icon(size):
    # Render quarry beetle icon on dark slate #10161c background
    bg_r, bg_g, bg_b = 0x10, 0x16, 0x1c
    gold_r, gold_g, gold_b = 0xf0, 0xde, 0x6b
    sky_r, sky_g, sky_b = 0x62, 0xb4, 0xe0
    dark_line_r, dark_line_g, dark_line_b = 0x1a, 0x24, 0x30

    scale = size / 512.0
    cx, cy = size / 2.0, size / 2.0

    def get_pixel(x, y):
        # Normalized coordinates from center (-1 to 1)
        nx = (x - cx) / (size * 0.42)
        ny = (y - cy) / (size * 0.42)

        # Background base
        r, g, b, a = bg_r, bg_g, bg_b, 255

        # Rounded background card glow
        d_center = math.hypot(nx, ny)
        if d_center < 1.1:
            glow = max(0.0, 1.0 - d_center) * 0.25
            r = int(r + (sky_r - r) * glow)
            g = int(g + (sky_g - g) * glow)
            b = int(b + (sky_b - b) * glow)

        # Beetle anatomy
        # 1. Main body ellipse
        body_val = (nx / 0.40) ** 2 + ((ny - 0.08) / 0.52) ** 2
        
        # 2. Head ellipse
        head_val = (nx / 0.28) ** 2 + ((ny + 0.52) / 0.22) ** 2

        # 3. Antennae
        ant_left_dist = abs(nx - (-0.2 - 0.25 * (ny + 0.6)**2)) if ny < -0.5 else 99
        ant_right_dist = abs(nx - (0.2 + 0.25 * (ny + 0.6)**2)) if ny < -0.5 else 99

        # 4. Legs
        leg_hit = False
        for i, ly in enumerate([-0.25, 0.0, 0.28]):
            sweep = 0.15 if i % 2 == 0 else -0.1
            for dir_x in [-1, 1]:
                lx1 = dir_x * 0.30
                lx2 = dir_x * 0.75
                ly2 = ly + sweep
                # distance to line segment
                dx = lx2 - lx1
                dy = ly2 - ly
                length_sq = dx*dx + dy*dy
                t = max(0, min(1, ((nx - lx1)*dx + (ny - ly)*dy) / length_sq))
                proj_x = lx1 + t * dx
                proj_y = ly + t * dy
                dist = math.hypot(nx - proj_x, ny - proj_y)
                if dist < 0.045:
                    leg_hit = True

        # Center seam line on beetle back
        is_seam = abs(nx) < 0.025 and (-0.3 < ny < 0.48)

        if body_val <= 1.0 or head_val <= 1.0 or leg_hit or (ant_left_dist < 0.04 and ny > -0.95) or (ant_right_dist < 0.04 and ny > -0.95):
            if is_seam:
                r, g, b = dark_line_r, dark_line_g, dark_line_b
            else:
                # Golden wheat color with subtle gradient
                grad = 0.9 + 0.2 * (1.0 - ny)
                r = min(255, int(gold_r * grad))
                g = min(255, int(gold_g * grad))
                b = min(255, int(gold_b * grad))

        return r, g, b, a

    return create_png(size, size, get_pixel)

def main():
    sizes = {
        'icon-192.png': 192,
        'icon-512.png': 512,
        'apple-touch-icon.png': 180,
        'AppIcon-1024.png': 1024,
        'AppIcon-167.png': 167,
        'AppIcon-152.png': 152,
        'AppIcon-120.png': 120,
        'AppIcon-76.png': 76,
    }
    
    os.makedirs('Quarry/www', exist_ok=True)
    os.makedirs('Quarry/Assets.xcassets/AppIcon.appiconset', exist_ok=True)

    for name, sz in sizes.items():
        print(f"Generating {name} ({sz}x{sz})...")
        png_data = render_icon(sz)
        
        # Save to www if PWA icon
        if name in ['icon-192.png', 'icon-512.png', 'apple-touch-icon.png']:
            with open(os.path.join('Quarry/www', name), 'wb') as f:
                f.write(png_data)
            with open(name, 'wb') as f:
                f.write(png_data)
                
        # Save to xcassets
        with open(os.path.join('Quarry/Assets.xcassets/AppIcon.appiconset', name), 'wb') as f:
            f.write(png_data)

    print("All icons generated successfully.")

if __name__ == '__main__':
    main()
