import streamlit as st
from PIL import Image, ImageOps
import io

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Image Processing Studio",
    page_icon="🖼️",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: gray;
    margin-bottom: 30px;
}

.info-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f0f2f6;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🖼️ Image Processing Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Resize, Compress, Rotate, Crop and Convert Your Images'
    '</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Image Operations")

operation = st.sidebar.selectbox(
    "Choose an operation",
    [
        "Resize Image",
        "Compress Image",
        "Increase Image Size",
        "Rotate Image",
        "Flip Image",
        "Crop Image",
        "Convert Image Format"
    ]
)

# --------------------------------------------------
# IMAGE UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📤 Upload your image",
    type=["jpg", "jpeg", "png", "webp"]
)

# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

if uploaded_file is not None:

    # Open image
    image = Image.open(uploaded_file)

    # Convert image to RGB for JPEG compatibility
    original_image = image.copy()

    # --------------------------------------------------
    # ORIGINAL IMAGE INFORMATION
    # --------------------------------------------------

    st.subheader("📊 Original Image Information")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Width", f"{image.width}px")

    with col2:
        st.metric("Height", f"{image.height}px")

    with col3:
        st.metric("Format", image.format)

    with col4:
        st.metric(
            "File Size",
            f"{uploaded_file.size / 1024:.2f} KB"
        )

    st.divider()

    # --------------------------------------------------
    # DISPLAY ORIGINAL IMAGE
    # --------------------------------------------------

    st.subheader("🖼️ Original Image")

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    # --------------------------------------------------
    # RESIZE IMAGE
    # --------------------------------------------------

    if operation == "Resize Image":

        st.subheader("📏 Resize Image")

        col1, col2 = st.columns(2)

        with col1:
            new_width = st.number_input(
                "Enter Width (pixels)",
                min_value=1,
                max_value=10000,
                value=image.width
            )

        with col2:
            new_height = st.number_input(
                "Enter Height (pixels)",
                min_value=1,
                max_value=10000,
                value=image.height
            )

        if st.button("Resize Image"):

            resized_image = image.resize(
                (new_width, new_height)
            )

            st.success("Image resized successfully!")

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    image,
                    caption="Original Image",
                    use_container_width=True
                )

            with col2:
                st.image(
                    resized_image,
                    caption="Resized Image",
                    use_container_width=True
                )

            # Save image in memory
            output = io.BytesIO()

            resized_image.save(
                output,
                format="PNG"
            )

            st.download_button(
                label="⬇️ Download Resized Image",
                data=output.getvalue(),
                file_name="resized_image.png",
                mime="image/png"
            )

    # --------------------------------------------------
    # COMPRESS IMAGE
    # --------------------------------------------------

    elif operation == "Compress Image":

        st.subheader("📦 Compress Image")

        quality = st.slider(
            "Select Image Quality",
            min_value=10,
            max_value=100,
            value=70,
            step=5
        )

        st.write(
            "Lower quality → Smaller file size"
        )

        if st.button("Compress Image"):

            output = io.BytesIO()

            # Convert to RGB
            compressed_image = image.convert("RGB")

            compressed_image.save(
                output,
                format="JPEG",
                quality=quality,
                optimize=True
            )

            compressed_size = len(
                output.getvalue()
            )

            original_size = uploaded_file.size

            st.success("Image compressed successfully!")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Original Size",
                    f"{original_size / 1024:.2f} KB"
                )

            with col2:
                st.metric(
                    "Compressed Size",
                    f"{compressed_size / 1024:.2f} KB"
                )

            with col3:

                reduction = (
                    1 - compressed_size / original_size
                ) * 100

                st.metric(
                    "Size Reduction",
                    f"{reduction:.2f}%"
                )

            st.download_button(
                label="⬇️ Download Compressed Image",
                data=output.getvalue(),
                file_name="compressed_image.jpg",
                mime="image/jpeg"
            )

    # --------------------------------------------------
    # INCREASE IMAGE SIZE
    # --------------------------------------------------

    elif operation == "Increase Image Size":

        st.subheader("🔍 Increase Image Size")

        scale = st.slider(
            "Select Enlargement Factor",
            min_value=1.1,
            max_value=5.0,
            value=2.0,
            step=0.1
        )

        new_width = int(image.width * scale)
        new_height = int(image.height * scale)

        st.info(
            f"New dimensions: "
            f"{new_width} × {new_height} pixels"
        )

        if st.button("Increase Image Size"):

            enlarged_image = image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

            st.success(
                "Image size increased successfully!"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    image,
                    caption="Original Image",
                    use_container_width=True
                )

            with col2:
                st.image(
                    enlarged_image,
                    caption="Enlarged Image",
                    use_container_width=True
                )

            output = io.BytesIO()

            enlarged_image.save(
                output,
                format="PNG"
            )

            st.download_button(
                label="⬇️ Download Enlarged Image",
                data=output.getvalue(),
                file_name="enlarged_image.png",
                mime="image/png"
            )

    # --------------------------------------------------
    # ROTATE IMAGE
    # --------------------------------------------------

    elif operation == "Rotate Image":

        st.subheader("🔄 Rotate Image")

        angle = st.selectbox(
            "Select Rotation Angle",
            [90, 180, 270]
        )

        if st.button("Rotate Image"):

            rotated_image = image.rotate(
                angle,
                expand=True
            )

            st.success(
                f"Image rotated by {angle}°"
            )

            st.image(
                rotated_image,
                caption="Rotated Image",
                use_container_width=True
            )

            output = io.BytesIO()

            rotated_image.save(
                output,
                format="PNG"
            )

            st.download_button(
                label="⬇️ Download Rotated Image",
                data=output.getvalue(),
                file_name="rotated_image.png",
                mime="image/png"
            )

    # --------------------------------------------------
    # FLIP IMAGE
    # --------------------------------------------------

    elif operation == "Flip Image":

        st.subheader("↔️ Flip Image")

        flip_type = st.radio(
            "Choose Flip Direction",
            [
                "Horizontal",
                "Vertical"
            ]
        )

        if st.button("Flip Image"):

            if flip_type == "Horizontal":

                flipped_image = ImageOps.mirror(
                    image
                )

            else:

                flipped_image = ImageOps.flip(
                    image
                )

            st.success("Image flipped successfully!")

            col1, col2 = st.columns(2)

            with col1:
                st.image(
                    image,
                    caption="Original",
                    use_container_width=True
                )

            with col2:
                st.image(
                    flipped_image,
                    caption="Flipped",
                    use_container_width=True
                )

            output = io.BytesIO()

            flipped_image.save(
                output,
                format="PNG"
            )

            st.download_button(
                label="⬇️ Download Flipped Image",
                data=output.getvalue(),
                file_name="flipped_image.png",
                mime="image/png"
            )

    # --------------------------------------------------
    # CROP IMAGE
    # --------------------------------------------------

    elif operation == "Crop Image":

        st.subheader("✂️ Crop Image")

        col1, col2 = st.columns(2)

        with col1:

            left = st.number_input(
                "Left",
                min_value=0,
                max_value=image.width - 1,
                value=0
            )

            top = st.number_input(
                "Top",
                min_value=0,
                max_value=image.height - 1,
                value=0
            )

        with col2:

            right = st.number_input(
                "Right",
                min_value=1,
                max_value=image.width,
                value=image.width
            )

            bottom = st.number_input(
                "Bottom",
                min_value=1,
                max_value=image.height,
                value=image.height
            )

        if st.button("Crop Image"):

            if right > left and bottom > top:

                cropped_image = image.crop(
                    (left, top, right, bottom)
                )

                st.success(
                    "Image cropped successfully!"
                )

                st.image(
                    cropped_image,
                    caption="Cropped Image",
                    use_container_width=True
                )

                output = io.BytesIO()

                cropped_image.save(
                    output,
                    format="PNG"
                )

                st.download_button(
                    label="⬇️ Download Cropped Image",
                    data=output.getvalue(),
                    file_name="cropped_image.png",
                    mime="image/png"
                )

            else:

                st.error(
                    "Please provide valid crop coordinates."
                )

    # --------------------------------------------------
    # FORMAT CONVERSION
    # --------------------------------------------------

    elif operation == "Convert Image Format":

        st.subheader("🎨 Convert Image Format")

        target_format = st.selectbox(
            "Select Output Format",
            ["JPEG", "PNG", "WEBP"]
        )

        if st.button("Convert Image"):

            output = io.BytesIO()

            converted_image = image

            # JPEG does not support RGBA
            if target_format == "JPEG":
                converted_image = image.convert("RGB")

            converted_image.save(
                output,
                format=target_format
            )

            st.success(
                f"Image converted to {target_format} successfully!"
            )

            st.image(
                converted_image,
                caption=f"{target_format} Image",
                use_container_width=True
            )

            extension = target_format.lower()

            mime_type = (
                "image/jpeg"
                if target_format == "JPEG"
                else f"image/{extension}"
            )

            st.download_button(
                label=f"⬇️ Download {target_format} Image",
                data=output.getvalue(),
                file_name=f"converted_image.{extension}",
                mime=mime_type
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

else:

    st.info(
        "👆 Please upload an image to start processing."
    )

st.divider()

st.markdown(
    """
    <center>
    <small>
    Image Processing Studio | Built with Streamlit & Python
    </small>
    </center>
    """,
    unsafe_allow_html=True
)