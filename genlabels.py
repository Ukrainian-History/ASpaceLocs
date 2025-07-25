import qrcode
from PIL import Image, ImageDraw, ImageFont
import textwrap

import aspace_api


### Generate a PNG file for each location in the ArchivesSpace instance with a QR code for the
# flask '/locations/<n>' endpoint and a text block with the description of the location

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Adjust as needed
font_size = 16
flask_endpoint = "https://locs.ukrhec.org"

location_ids = aspace_api.get_all_location_ids()

for location in location_ids:
    qr_payload = f'{flask_endpoint}/locations/{location}'
    location_info = aspace_api.get_location(location)

    # The below code for creating PNGs with QR codes and location info text was generated by perplexity.ai (with
    # minor refactoring)

    # Generate QR code
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(qr_payload)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_width, qr_height = qr_img.size

    # Prepare font
    font = ImageFont.truetype(font_path, font_size)

    # Wrap text to fit QR code width
    max_text_width = qr_width - 10  # Padding
    lines = []
    for paragraph in location_info.splitlines():
        # Use textwrap to split into lines by character count
        lines.extend(textwrap.wrap(paragraph, width=100))

    # Refine wrapping to fit pixel width
    wrapped_lines = []
    for line in lines:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            left, top, right, bottom = font.getbbox(test_line)
            test_width = right - left
            if test_width <= max_text_width:
                current_line = test_line
            else:
                if current_line:
                    wrapped_lines.append(current_line)
                current_line = word
        if current_line:
            wrapped_lines.append(current_line)

    # Calculate text block height
    line_height = font.getbbox("A")[3] - font.getbbox("A")[1] + 2
    text_height = line_height * len(wrapped_lines) + 10  # 10px bottom padding

    # Create new image to hold QR + text
    total_height = qr_height + text_height
    out_img = Image.new("RGB", (qr_width, total_height), "white")
    out_img.paste(qr_img, (0, 0))

    # Draw wrapped text
    draw = ImageDraw.Draw(out_img)
    y = qr_height + 5
    for line in wrapped_lines:
        left, top, right, bottom = font.getbbox(line)
        w = right - left
        x = (qr_width - w) // 2  # Center text
        draw.text((x, y), line, font=font, fill="black")
        y += line_height

    # Save result
    out_img.save(f"qrcodes/qr{location}.png")
    print(f'did {location}')
