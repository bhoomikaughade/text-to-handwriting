import argparse
import textwrap
import random
from PIL import Image, ImageDraw, ImageFont

def jittered_draw_text(draw, x, y, text, font, max_jitter=2, angle_jitter=3, spacing_jitter=0.9):
    cur_x = x
    for ch in text:
        bbox = draw.textbbox((0,0), ch, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        ox = random.uniform(-max_jitter, max_jitter)
        oy = random.uniform(-max_jitter, max_jitter)
        char_w = max(12, int(w * 3))
        char_h = max(12, int(h * 3))
        char_img = Image.new("RGBA", (char_w, char_h), (255,255,255,0))
        cd = ImageDraw.Draw(char_img)
        # center-ish position inside the small image
        cd.text((w/2, h/4), ch, font=font, fill=(0,0,0,255))
        angle = random.uniform(-angle_jitter, angle_jitter)
        char_img = char_img.rotate(angle, resample=Image.BICUBIC, expand=True)
        draw.im.paste(char_img, (int(cur_x + ox - w/2), int(y + oy - h/2)), char_img)
        spacing = max(1, w * random.uniform(0.8, 1.15) * spacing_jitter)
        cur_x += spacing

def render_text_to_image(text, font_path="handwriting.ttf", font_size=42,
                         page_width=1654, margin=60, line_spacing=1.25,
                         bg_color="white", jitter=True):
    # load font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print("Font load failed:", e)
        font = ImageFont.load_default()

    # use a temporary draw to measure text (compatible across Pillow versions)
    tmp_img = Image.new("RGB", (10, 10))
    tmp_draw = ImageDraw.Draw(tmp_img)
    bbox = tmp_draw.textbbox((0,0), "x", font=font)
    avg_char_w = bbox[2] - bbox[0]
  


    usable = page_width - 2*margin
    chars_per_line = max(20, int(usable / max(1, avg_char_w)))

    wrapper = textwrap.TextWrapper(width=chars_per_line, replace_whitespace=False)
    lines = []
    for para in text.splitlines():
        if para.strip() == "":
            lines.append("")
        else:
            wrapped = wrapper.wrap(para)
            lines.extend(wrapped if wrapped else [""])

    line_h = int(font_size * line_spacing)
    height = margin*2 + line_h * (len(lines) + 1)
    img = Image.new("RGB", (page_width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    draw.im = img  # helper so we can paste RGBA char images

    x0 = margin
    y = margin
    for ln in lines:
        if ln.strip() == "":
            y += line_h
            continue
        if jitter:
            jittered_draw_text(draw, x0, y, ln, font,
                               max_jitter=max(1, font_size//24),
                               angle_jitter=2 + font_size//24,
                               spacing_jitter=1.0)
        else:
            draw.text((x0, y), ln, font=font, fill="black")
        y += line_h

    return img

def main():
    parser = argparse.ArgumentParser(description="Convert text to handwriting-style image.")
    parser.add_argument("infile")
    parser.add_argument("outfile")
    parser.add_argument("--font", default="handwriting.ttf")
    parser.add_argument("--size", type=int, default=42)
    parser.add_argument("--width", type=int, default=1654)
    parser.add_argument("--margin", type=int, default=60)
    parser.add_argument("--no-jitter", action="store_true")
    args = parser.parse_args()

    with open(args.infile, "r", encoding="utf-8") as f:
        text = f.read()

    img = render_text_to_image(text, font_path=args.font, font_size=args.size,
                               page_width=args.width, margin=args.margin, jitter=not args.no_jitter)

    out = args.outfile.lower()
    if out.endswith(".pdf"):
        rgb = img.convert("RGB")
        rgb.save(args.outfile, "PDF", resolution=100.0)
        print("Saved PDF:", args.outfile)
    else:
        img.save(args.outfile)
        print("Saved image:", args.outfile)

if __name__ == "__main__":
    main()
