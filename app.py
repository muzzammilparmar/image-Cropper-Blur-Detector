import streamlit as st
from streamlit_cropper import st_cropper
import cv2
import numpy as np
from PIL import Image
import io

# --- 1. Page Setup ---
st.set_page_config(page_title="ID Cropper & Validator", page_icon="🔍", layout="centered")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. Diagnostic Function ---
def analyze_image(pil_image, threshold=100.0):
    # Convert cropped PIL Image to NumPy array for OpenCV
    img_array = np.array(pil_image.convert('RGB'))
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # Blur Detection
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    is_blurry = variance < threshold
    
    # Exposure Detection
    avg_brightness = np.mean(gray)
    exposure_status = "Normal"
    if avg_brightness > 220:
        exposure_status = "Overexposed"
    elif avg_brightness < 50:
        exposure_status = "Underexposed"
        
    # QR Code Detection
    qr_decoder = cv2.QRCodeDetector()
    data, bbox, _ = qr_decoder.detectAndDecode(img_array)
    qr_found = bbox is not None and bool(data)
    
    return variance, is_blurry, exposure_status, qr_found, data

# --- 3. Main UI ---
st.title("🔍 Field Document Validator")
st.markdown("Capture, crop, and verify image clarity in one seamless workflow.")

# Swapped the order here so "Upload Image" is first
input_method = st.radio("Select Input Method:", ("Upload Image", "Use Camera"), horizontal=True)

img_file = None
if input_method == "Upload Image":
    img_file = st.file_uploader('Upload a file', type=['png', 'jpg', 'jpeg'])
else:
    img_file = st.camera_input("Capture Document")

if img_file is not None:
    img = Image.open(img_file)
    
    st.write("---")
    st.subheader("Step 1: Crop the Document")
    
    # Ratio Selection
    ratio_options = {
        "3:4 (Standard ID)": (3, 4),
        "Freeform (Drag freely)": None,
        "1:1 (Square)": (1, 1),
        "16:9 (Wide)": (16, 9)
    }
    selected_ratio = st.radio("Aspect Ratio:", list(ratio_options.keys()), index=0, horizontal=True)
    
    # Interactive Cropper
    cropped_img = st_cropper(
        img,
        realtime_update=True,
        box_color='#0066cc',
        aspect_ratio=ratio_options[selected_ratio]
    )
    
    st.write("---")
    st.subheader("Step 2: Diagnostics & Download")
    
    # Display the final cropped preview
    st.image(cropped_img, caption="Cropped Preview", use_container_width=True)
    
    # Diagnostics Controls
    threshold = st.slider("Blur Strictness", 10.0, 500.0, 100.0)
    
    if st.button("Run Diagnostics on Cropped Image", type="primary", use_container_width=True):
        with st.spinner("Analyzing cropped image..."):
            variance, is_blurry, exposure, qr_found, qr_data = analyze_image(cropped_img, threshold)
            
            # Display Results
            st.metric(label="Sharpness Score", value=f"{variance:.1f}")
            
            if is_blurry:
                st.error("🚨 REJECTED: The cropped area is too blurry.")
            else:
                st.success("✅ PASSED: Image is appropriately sharp.")
                
            if exposure != "Normal":
                st.warning(f"⚠️ {exposure} detected. Watch out for glare or dark shadows.")
                
            if qr_found:
                st.info(f"✅ QR Code Scanned: {qr_data}")
            else:
                st.warning("No readable QR code found in the cropped area.")
    
    # Prepare download buffer
    buf = io.BytesIO()
    rgb_im = cropped_img.convert('RGB')
    rgb_im.save(buf, format="JPEG", quality=95)
    
    st.write("") # Spacer
    st.download_button(
        label="📥 Download Verified Image",
        data=buf.getvalue(),
        file_name="verified_vendor_id.jpg",
        mime="image/jpeg",
        use_container_width=True
    )