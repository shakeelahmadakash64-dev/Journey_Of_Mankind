from PIL import Image, ImageDraw

def create_game_icon():
    sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    
    for size in sizes:
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        w, h = size
        
        # Outer Earth/Globe circle: Deep earth brown / terracotta
        margin = int(w * 0.05)
        draw.ellipse([margin, margin, w - margin, h - margin], fill=(45, 25, 15, 255), outline=(210, 140, 50, 255), width=max(1, int(w * 0.04)))
        
        # Inner warm primordial fire sun / flame
        inner_m = int(w * 0.22)
        draw.ellipse([inner_m, inner_m, w - inner_m, h - inner_m], fill=(235, 110, 25, 255), outline=(255, 215, 0, 255), width=max(1, int(w * 0.03)))
        
        # Center core: glowing embers
        core_m = int(w * 0.38)
        draw.ellipse([core_m, core_m, w - core_m, h - core_m], fill=(255, 240, 150, 255))
        
        # Spear silhouette diagonal across the circle
        spear_w = max(2, int(w * 0.06))
        draw.line([(int(w * 0.2), int(h * 0.8)), (int(w * 0.8), int(h * 0.2))], fill=(240, 240, 240, 255), width=spear_w)
        # Spear tip arrowhead
        tip_x, tip_y = int(w * 0.82), int(h * 0.18)
        draw.polygon([(tip_x, tip_y - int(w*0.06)), (tip_x + int(w*0.06), tip_y), (tip_x - int(w*0.02), tip_y + int(w*0.02))], fill=(180, 50, 30, 255))
        
        images.append(img)
        
    images[0].save("app_icon.ico", format="ICO", sizes=[(s[0], s[1]) for s in sizes], append_images=images[1:])
    print("Successfully created app_icon.ico with multi-resolution support!")

if __name__ == '__main__':
    create_game_icon()
