import streamlit as st
import os
from PIL import Image, ImageDraw, ImageFont
import io

# Function to process the uploaded image and text based on the selected background color
def process_image(background_color, uploaded_image, text_input):
    # Create a copy of the background image
    back = Image.open(background_color).convert("RGBA")

    # Open the uploaded icon image
    icon = Image.open(uploaded_image).convert("RGBA")

    # Create a copy of the icon to work with
    whited_icon = icon.copy()

    # Iterate through the pixels of the icon and change non-transparent pixels to white or dark based on the background color
    for x in range(icon.width):
        for y in range(icon.height):
            r, g, b, a = whited_icon.getpixel((x, y))
            if a > 0:
                if background_color == "white-frame.png":
                    whited_icon.putpixel((x, y), (25, 52, 152, a))
                else:
                    whited_icon.putpixel((x, y), (255, 255, 255, a))

    # Resize the modified icon
    whited_icon = whited_icon.resize((250, 250))

    # Calculate the X-coordinate to center the icon horizontally
    x_centered = (back.width - whited_icon.width) // 2

    # Paste the modified icon onto the background at the calculated X-coordinate
    back.paste(whited_icon, (x_centered, 100), whited_icon)

    text_on = text_input
    font = ImageFont.truetype("IRYekan.ttf", size=60, layout_engine=ImageFont.LAYOUT_RAQM)
    I1 = ImageDraw.Draw(back)

    lines = []
    current_line = ""
    for word in text_on.split():
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
        if background_color == "white-frame.png":
            I1.text((x, y - 15), line, fill=(25, 52, 152), font=font, align="center", direction="rtl")
        else:
            I1.text((x, y - 15), line, fill=(255, 255, 255), font=font, align="center", direction="rtl")
        y += h

    return back

# Streamlit UI
st.title("Image Generator")
st.write("Upload an icon image and enter text to generate an image with different backgrounds.")

background_color_option = st.radio("Select background color:", ("White", "Dark"))

uploaded_image = st.file_uploader("Upload an icon image:", type=["jpg", "png"])
text_input = st.text_input("Enter text:")

if uploaded_image is not None and text_input:
    if background_color_option == "White":
        background_color = "white-frame.png"
    else:
        background_color = "dark-frame.png"

    generated_image = process_image(background_color, uploaded_image, text_input)

    st.image(generated_image, caption="Generated Image", use_column_width=True)

# To clear cache and prevent image caching issues
if st.button("Clear Cache"):
    st.caching.clear_cache()

st.write("Note: Due to caching, you might need to click 'Clear Cache' after changing the background color or uploading a new image.")
