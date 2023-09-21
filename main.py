import streamlit as st
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import io

# Function to apply code 1 to the image
def apply_code_1(icon_img, text):
    back = Image.open("frame.png").convert("RGBA")

    # Create a copy of the icon to work with
    whited_icon = icon_img.copy()

    # Iterate through the pixels of the icon and change non-transparent pixels to white
    for x in range(icon_img.width):
        for y in range(icon_img.height):
            r, g, b, a = whited_icon.getpixel((x, y))
            if a > 0:
                whited_icon.putpixel((x, y), (255, 255, 255, a))

    # Resize the modified icon
    whited_icon = whited_icon.resize((250, 250))

    # Calculate the X-coordinate to center the icon horizontally
    x_centered = (back.width - whited_icon.width) // 2

    # Paste the modified icon onto the background at the calculated X-coordinate
    back.paste(whited_icon, (x_centered, 100), whited_icon)

    font = ImageFont.truetype("IRYekan.ttf", size=60, layout_engine=ImageFont.Layout.RAQM)
    I1 = ImageDraw.Draw(back)

    lines = []
    current_line = ""
    for word in text.split():
        if I1.textsize(current_line + word + " ", font=font)[0] > 900:
            lines.append(current_line.strip())
            current_line = ""
        current_line += word + " "
    if current_line:
        lines.append(current_line.strip())

    y = 375
    for line in lines:
        _, _, w, h = I1.textbbox((0, 0), line, font=font)
        x = (back.width - w) / 2
        I1.text((x, y - 15), line, fill=(255, 255, 255), font=font, align="center", direction="rtl")
        y += h

    return back

# Function to apply code 2 to the image
def apply_code_2(icon_img, text):
    back = Image.open("white-frame.png").convert("RGBA")

    # Create a copy of the icon to work with
    whited_icon = icon_img.copy()

    # Iterate through the pixels of the icon and change non-transparent pixels to a dark color
    for x in range(icon_img.width):
        for y in range(icon_img.height):
            r, g, b, a = whited_icon.getpixel((x, y))
            if a > 0:
                whited_icon.putpixel((x, y), (25, 52, 152, a))

    # Resize the modified icon
    whited_icon = whited_icon.resize((250, 250))

    # Calculate the X-coordinate to center the icon horizontally
    x_centered = (back.width - whited_icon.width) // 2

    # Paste the modified icon onto the background at the calculated X-coordinate
    back.paste(whited_icon, (x_centered, 100), whited_icon)

    font = ImageFont.truetype("IRYekan.ttf", size=60, layout_engine=ImageFont.Layout.RAQM)
    I1 = ImageDraw.Draw(back)

    lines = []
    current_line = ""
    for word in text.split():
        if I1.textsize(current_line + word + " ", font=font)[0] > 900:
            lines.append(current_line.strip())
            current_line = ""
        current_line += word + " "
    if current_line:
        lines.append(current_line.strip())

    y = 375
    for line in lines:
        _, _, w, h = I1.textbbox((0, 0), line, font=font)
        x = (back.width - w) / 2
        I1.text((x, y - 15), line, fill=(25, 52, 152), font=font, align="center", direction="rtl")
        y += h

    return back

# Main Streamlit app
def main():
    st.title("Image Generator")

    # Upload icon image
    icon_image = st.file_uploader("Upload Icon Image", type=["jpg", "png", "jpeg"])
    if icon_image:
        icon_img = Image.open(icon_image).convert("RGBA")

        # Input text
        text = st.text_input("Enter Text", "معاملات اسپات چیست؟")

        # Background style selection
        background_style = st.selectbox("Select Background Style", ["White", "Dark"])

        if st.button("Generate Image"):
            if background_style == "White":
                generated_image = apply_code_1(icon_img, text)
            else:
                generated_image = apply_code_2(icon_img, text)

            st.image(generated_image, use_column_width=True)

if __name__ == "__main__":
    main()
