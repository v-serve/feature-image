import streamlit as st
from PIL import Image

# Function to apply watermark to the uploaded image
def apply_watermark(background_image):
    watermark = Image.open("blue-watermark.png").convert("RGBA")

    # Get the current width and height of the image
    width, height = background_image.size
    watermark_width, watermark_height = watermark.size

    back = Image.new(mode="RGBA", size=(width, height + 40), color=(255, 255, 255))
    back.paste(background_image, (0, 0), background_image)

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
    watermark_cropped = watermark.crop(((watermark_width - new_width) / 2, 0,
                                        (watermark_width - new_width) / 2 + new_width + 1, new_height))

    # Paste the watermark onto the back image
    back.paste(watermark_cropped, position, watermark_cropped)

    # Save the result as a PNG
    back = back.convert("RGB")
    return back

# Streamlit UI
st.title("Watermark App")
st.write("Upload a background image or paste an image link below:")
uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
image_url = st.text_input("Or paste an image URL")

if uploaded_image is not None:
    background_image = Image.open(uploaded_image).convert("RGBA")
    result = apply_watermark(background_image)
    st.image(result, use_column_width=True, caption="Watermarked Image")
    st.markdown("### Download Watermarked Image")
    st.write("Click the link below to download the watermarked image:")
    st.download_button("Download Watermarked Image", result.tobytes(), file_name="watermarked_image.png", key="watermarked")

if image_url:
    try:
        from urllib.request import urlopen
        background_image = Image.open(urlopen(image_url)).convert("RGBA")
        result = apply_watermark(background_image)
        st.image(result, use_column_width=True, caption="Watermarked Image")
        st.markdown("### Download Watermarked Image")
        st.write("Click the link below to download the watermarked image:")
        st.download_button("Download Watermarked Image", result.tobytes(), file_name="watermarked_image.png", key="watermarked")
    except Exception as e:
        st.error("Error: Unable to load the image from the provided URL.")
