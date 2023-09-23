import streamlit as st
from PIL import Image
import io

# Function to add watermark to the background image
def add_watermark(background_path, watermark_path):
    background = Image.open(background_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")

    # Get the current width and height of the background image
    width, height = background.size
    watermark_width, watermark_height = watermark.size

    back = Image.new(mode="RGBA", size=(width, height + 40), color=(255, 255, 255))
    back.paste(background, (0, 0), background)

    # Check if the width is greater than 1800 pixels
    if width > 1800:
        # Calculate the new height while maintaining the aspect ratio
        new_width = 1800
        new_height = int(height * (1800 / width))
        position = (0, new_height - watermark_height)
        # Resize the image to a maximum width of 1800 pixels
        back = back.resize((new_width, new_height), Image.ANTIALIAS)
    else:
        new_width = width
        new_height = height
        position = (0, new_height - watermark_height + 40)

    # Calculate the position to paste the watermark at the bottom
    watermark_cropped = watermark.crop(
        (
            (watermark_width - new_width) / 2,
            0,
            (watermark_width - new_width) / 2 + new_width + 1,
            new_height,
        )
    )

    # Paste the watermark onto the background image
    back.paste(watermark_cropped, position, watermark_cropped)

    # Convert the result to RGB format
    back = back.convert("RGB")

    return back

# Streamlit app
st.title("Watermark App")

# Upload background image
background_image = st.file_uploader("Upload a background image", type=["jpg", "jpeg", "png"])

if background_image is not None:
    watermark_path = "blue-watermark.png"  # Path to the fixed watermark

    # Apply watermark to the background image
    watermarked_image = add_watermark(background_image, watermark_path)

    # Save the watermarked image to a temporary file
    temp_buffer = io.BytesIO()
    watermarked_image.save(temp_buffer, format="PNG")

    # Display the watermarked image
    st.image(temp_buffer, caption="Watermarked Image", use_column_width=True)

    # Provide a download link for the watermarked image
    st.download_button(
        label="Download Watermarked Image",
        data=temp_buffer.getvalue(),
        file_name="watermarked_image.png",
        key="download-button",
    )
