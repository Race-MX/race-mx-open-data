"""Render 1080x1920 Race.mx Short frames from a JSON spec: {name: {theme, pages:[[(text,size,color,font),...],...]}}."""
import json, math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H = 1080, 1920
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
C = {"ink": (30, 27, 24), "orange": (217, 84, 30), "cream": (246, 238, 225), "rust": (176, 72, 24), "teal": (40, 200, 190)}

def grad(top, bot, p=1.0):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        t = (y / H) ** p
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return img

def desert(seed):
    rnd = random.Random(seed); img = grad(C["cream"], C["rust"], 1.6); d = ImageDraw.Draw(img, "RGBA")
    for _ in range(9000):
        d.point((rnd.randrange(W), rnd.randrange(H)), fill=(120, 60, 20, rnd.randrange(10, 45)))
    cloud = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(cloud)
    for _ in range(60):
        cx, cy, r = rnd.randrange(600, 1150), rnd.randrange(1150, 1750), rnd.randrange(60, 180)
        cd.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(205, 110, 50, rnd.randrange(18, 40)))
    cloud = cloud.filter(ImageFilter.GaussianBlur(40)); img.paste(cloud, (0, 0), cloud)
    d = ImageDraw.Draw(img, "RGBA")
    for off in (-70, 70):
        for i in range(120):
            t = i / 120; y = H + 40 - t * 820
            x = W * 0.42 + off * (1 - t * 0.7) + math.sin(t * 3.2 + seed) * 160 * t; w = 46 * (1 - t * 0.75)
            d.rectangle((x - w / 2, y - 5 * (1 - t * .6), x + w / 2, y + 5 * (1 - t * .6)), fill=(60, 30, 12, int(150 * (1 - t))))
    return img, C["ink"]

def night(seed, accent=None):
    rnd = random.Random(seed); img = grad((22, 20, 26), (12, 10, 12), 1.0)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    acc = accent or C["orange"]
    for k in range(9):  # light streaks sweeping through the lower half
        y0 = 1150 + k * 55 + rnd.randrange(-20, 20)
        pts = [(x, y0 + math.sin(x / 260 + seed + k) * 70 - x * 0.12) for x in range(-50, W + 60, 20)]
        col = acc if k % 3 else C["cream"]
        g.line(pts, fill=col + (rnd.randrange(90, 170),), width=rnd.randrange(3, 9))
    glow = glow.filter(ImageFilter.GaussianBlur(6)); img.paste(glow, (0, 0), glow)
    d = ImageDraw.Draw(img, "RGBA")
    # kerb stripes along the bottom curve
    for i in range(22):
        x = i * 60 - 40; y = 1760 - math.sin(i / 3.0) * 40
        d.polygon([(x, y), (x + 60, y - 6), (x + 60, y + 34), (x, y + 40)], fill=(200, 40, 30, 200) if i % 2 else (240, 235, 225, 200))
    for _ in range(4000):
        d.point((rnd.randrange(W), rnd.randrange(H)), fill=(255, 255, 255, rnd.randrange(4, 18)))
    return img, C["cream"]

def text(img, s, y, size, color, font, squash=0.82, max_w=W - 150):
    while True:
        f = ImageFont.truetype(font, size); l, t, r, b = f.getbbox(s)
        if (r - l) * squash <= max_w or size < 20: break
        size -= 4
    lay = Image.new("RGBA", (r - l + 10, b - t + 20), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((5 - l, 10 - t), s, font=f, fill=color + (255,))
    lay = lay.resize((max(1, int(lay.width * squash)), lay.height), Image.LANCZOS)
    img.paste(lay, ((W - lay.width) // 2, int(y)), lay)
    return y + lay.height

def pill(img, s, y, fg, bg):
    f = ImageFont.truetype(BOLD, 42); l, t, r, b = f.getbbox(s); w, h = r - l + 60, b - t + 32; x = (W - w) // 2
    d = ImageDraw.Draw(img); d.polygon([(x + 14, y), (x + w + 14, y), (x + w - 14, y + h), (x - 14, y + h)], fill=bg)
    d.text((x + 30 - l, y + 16 - t), s, font=f, fill=fg); return y + h

spec = json.load(open(sys.argv[1])); out = sys.argv[2]
for name, sh in spec.items():
    for n, page in enumerate(sh["pages"], 1):
        seed = hash((name, n)) % 1000
        img, ink = desert(seed) if sh["theme"] == "desert" else night(seed, C["teal"] if sh["theme"] == "electric" else None)
        ImageDraw.Draw(img).text((70, 90), "RACE.MX", font=ImageFont.truetype(BOLD, 34), fill=ink)
        y = 300
        for item in page:
            kind, s = item[0], item[1]
            if kind == "pill":
                y = pill(img, s, y + 30, C["cream"] if sh["theme"] == "desert" else C["ink"], C["ink"] if sh["theme"] == "desert" else C["orange"]) + 10
            else:
                size = {"h": 160, "big": 260, "sub": 62, "small": 48}[kind]
                col = C["orange"] if kind == "big" else ink
                y = text(img, s, y + (40 if kind in ("big", "sub") else 6), size, col, REG if kind == "small" else BOLD, squash=1.0 if kind == "small" else 0.82)
        img.save(os.path.join(out, f"{name}_p{n}.png"))
    print(name, len(sh["pages"]))
