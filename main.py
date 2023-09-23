import streamlit as st
from PIL import Image

# Function to add watermark to the image
def add_watermark(background_image):
    backgound = Image.open(background_image).convert("RGBA")
    watermark = Image.open("blue-watermark.png").convert("RGBA")

    # Get the current width and height of the image
    width, height = backgound.size
    watermark_width, watermark_height = watermark.size

    back = Image.new(mode="RGBA", size=(width, height+40), color=(255, 255, 255))
    back.paste(backgound, (0,0), backgound)

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
    watermark_cropped = watermark.crop(((watermark_width-new_width)/2, 0,(watermark_width-new_width)/2 + new_width+1,new_height))
    
    # Paste the watermark onto the back image
    back.paste(watermark_cropped, position, watermark_cropped)

    # Save the result
    back = back.convert("RGB")
    return back

# Streamlit app
st.title("Arzchi Watermarking App")

# Upload background image
background_image = st.file_uploader("Upload background image", type=["jpg", "jpeg", "png"])
if background_image:
    #st.write("Original Image:")
    #st.image(background_image, use_column_width=True)

    st.write("Watermarked Image:")
    watermarked_image = add_watermark(background_image)
    st.image(watermarked_image, use_column_width=True)
