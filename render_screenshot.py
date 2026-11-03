import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def draw_envelope_icon(draw, cx, cy, size, color):
    w = size * 0.95
    h = size * 0.70
    x0 = cx - w / 2
    y0 = cy - h / 2
    x1 = cx + w / 2
    y1 = cy + h / 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=2, outline=color, width=2)
    draw.line([(x0, y0), (cx, cy + 3)], fill=color, width=2)
    draw.line([(x1, y0), (cx, cy + 3)], fill=color, width=2)

def draw_phone_icon(draw, cx, cy, size, color):
    w = size * 0.62
    h = size * 0.96
    x0 = cx - w / 2
    y0 = cy - h / 2
    x1 = cx + w / 2
    y1 = cy + h / 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=3, outline=color, width=2)
    draw.line([(cx - 3, y0 + 3), (cx + 3, y0 + 3)], fill=color, width=1)
    draw.ellipse([cx - 2, y1 - 4, cx + 2, y1 - 1], fill=color)

def draw_location_icon(draw, cx, cy, size, color):
    r = size * 0.40
    draw.ellipse([cx - r, cy - size * 0.52, cx + r, cy - size * 0.52 + 2 * r], outline=color, width=2)
    draw.polygon([(cx - r * 0.85, cy - size * 0.12), (cx + r * 0.85, cy - size * 0.12), (cx, cy + size * 0.44)], fill=color)
    ir = 2.5
    draw.ellipse([cx - ir, cy - size * 0.52 + r - ir, cx + ir, cy - size * 0.52 + r + ir], fill=(255, 255, 255, 255))

def create_profile_screenshot(output_path):
    width = 390
    height = 780
    img = Image.new("RGBA", (width, height), (243, 244, 249, 255))
    draw = ImageDraw.Draw(img)

    font_dir = r"C:\Windows\Fonts"
    font_time = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 14)
    font_status = ImageFont.truetype(os.path.join(font_dir, "arial.ttf"), 12)
    font_appbar = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 19)
    font_avatar = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 30)
    font_name = ImageFont.truetype(os.path.join(font_dir, "arialbd.ttf"), 22)
    font_role = ImageFont.truetype(os.path.join(font_dir, "arial.ttf"), 15)
    font_contact = ImageFont.truetype(os.path.join(font_dir, "arial.ttf"), 14)

    # 1. Top status bar
    draw.text((24, 12), "9:41", font=font_time, fill=(30, 32, 45, 255))
    draw.text((width - 80, 12), "LTE  100%", font=font_status, fill=(30, 32, 45, 255))

    # 2. Material 3 AppBar
    appbar_top = 44
    appbar_height = 56
    title = "My Profile"
    bbox = draw.textbbox((0, 0), title, font=font_appbar)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, appbar_top + 16), title, font=font_appbar, fill=(28, 30, 48, 255))
    draw.line([(0, appbar_top + appbar_height), (width, appbar_top + appbar_height)], fill=(225, 228, 238, 255), width=1)

    # 3. Card specifications
    card_w = 340
    card_h = 350
    card_x0 = (width - card_w) // 2
    card_y0 = appbar_top + appbar_height + (height - (appbar_top + appbar_height) - card_h) // 2 - 20
    card_x1 = card_x0 + card_w
    card_y1 = card_y0 + card_h
    corner_radius = 20

    # Soft subtle Material elevation shadow
    shadow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(shadow)
    sdraw.rounded_rectangle(
        [card_x0 + 2, card_y0 + 6, card_x1 - 2, card_y1 + 10],
        radius=corner_radius,
        fill=(50, 65, 130, 32)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=10))
    img = Image.alpha_composite(img, shadow)
    draw = ImageDraw.Draw(img)

    # Card Body
    draw.rounded_rectangle(
        [card_x0, card_y0, card_x1, card_y1],
        radius=corner_radius,
        fill=(255, 255, 255, 255)
    )

    # 4. Avatar (CircleAvatar)
    avatar_radius = 40
    avatar_cx = width // 2
    avatar_cy = card_y0 + 62

    # Theme indigo color
    indigo_seed = (63, 81, 181, 255)
    indigo_light = (238, 241, 252, 255)

    draw.ellipse(
        [avatar_cx - avatar_radius, avatar_cy - avatar_radius, avatar_cx + avatar_radius, avatar_cy + avatar_radius],
        fill=indigo_seed
    )
    # Initials
    av_text = "KW"
    abox = draw.textbbox((0, 0), av_text, font=font_avatar)
    atw = abox[2] - abox[0]
    ath = abox[3] - abox[1]
    draw.text((avatar_cx - atw // 2, avatar_cy - ath // 2 - 3), av_text, font=font_avatar, fill=(255, 255, 255, 255))

    # 5. Name
    name_text = "Kamaleshwaran"
    nbox = draw.textbbox((0, 0), name_text, font=font_name)
    ntw = nbox[2] - nbox[0]
    name_y = avatar_cy + avatar_radius + 14
    draw.text((avatar_cx - ntw // 2, name_y), name_text, font=font_name, fill=(24, 26, 40, 255))

    # 6. Role
    role_text = "Flutter Developer Intern"
    rbox = draw.textbbox((0, 0), role_text, font=font_role)
    rtw = rbox[2] - rbox[0]
    role_y = name_y + 28
    draw.text((avatar_cx - rtw // 2, role_y), role_text, font=font_role, fill=indigo_seed)

    # 7. Divider
    div_y = role_y + 30
    draw.line([(card_x0 + 20, div_y), (card_x1 - 20, div_y)], fill=(236, 239, 246, 255), width=1)

    # 8. Contact Rows (Reusable ContactRow widget)
    contacts = [
        ("email", "kamalesh.dev@example.com"),
        ("phone", "+91 98765 43210"),
        ("location", "Chennai, India"),
    ]

    contact_start_y = div_y + 14
    row_gap = 10
    box_size = 34

    for i, (ctype, ctext) in enumerate(contacts):
        box_y = contact_start_y + (i * (box_size + row_gap))
        box_x = card_x0 + 24
        
        # Icon background box
        draw.rounded_rectangle(
            [box_x, box_y, box_x + box_size, box_y + box_size],
            radius=8,
            fill=indigo_light
        )
        
        icx = box_x + box_size / 2
        icy = box_y + box_size / 2

        if ctype == "email":
            draw_envelope_icon(draw, icx, icy, 18, (63, 81, 181, 255))
        elif ctype == "phone":
            draw_phone_icon(draw, icx, icy, 18, (63, 81, 181, 255))
        elif ctype == "location":
            draw_location_icon(draw, icx, icy, 18, (63, 81, 181, 255))

        # Text
        draw.text((box_x + box_size + 14, box_y + 8), ctext, font=font_contact, fill=(40, 44, 60, 255))

    # 9. Phone Home Indicator
    draw.rounded_rectangle([(width - 120) // 2, height - 16, (width + 120) // 2, height - 12], radius=2, fill=(190, 195, 205, 255))

    img.save(output_path, "PNG")
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    out1 = r"C:\Users\kamal\.gemini\antigravity\scratch\profile-card-app\profile_card_screenshot.png"
    out2 = r"C:\Users\kamal\.gemini\antigravity\brain\25af918f-982f-40a5-b272-1c402d469ed0\profile_card_screenshot.png"
    create_profile_screenshot(out1)
    create_profile_screenshot(out2)
