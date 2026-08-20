# 🔍 CivicLens: Document Cropper & Validator

A lightweight, automated image verification and cropping tool designed for field officers and administrative staff. Built with Python, Streamlit, and OpenCV, this application streamlines the collection of vendor ID cards and field documents. It allows users to interactively crop images to standard ID ratios and automatically runs quality diagnostics before saving, ensuring all submitted data is sharp, readable, and properly formatted.

## 🚀 Features

* **Interactive Auto-Cropping:** Drag-and-drop bounding box with predefined aspect ratios (3:4 Standard ID, 1:1, 16:9, or Freeform) to perfectly isolate the document from background noise.
* **Blur Detection:** Utilizes the Variance of the Laplacian method to calculate an image sharpness score on the cropped area, instantly flagging blurry or unreadable photos.
* **Exposure Warning:** Analyzes pixel intensity to warn users of severe overexposure (flash glare) or underexposure (poor lighting).
* **Auto-QR Code Scanning:** Automatically detects and decodes QR codes present within the cropped ID to verify data integrity on the spot.
* **Flexible Input:** Upload existing images from local storage or seamlessly switch to live camera capture.
* **Instant Export:** One-click download of the verified, cleanly cropped JPEG file.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Frontend UI:** Streamlit
* **Interactive Components:** Streamlit-Cropper
* **Computer Vision:** OpenCV (`opencv-python-headless`)
* **Image Processing:** NumPy, Pillow (PIL)

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/civiclens-validator.git](https://github.com/yourusername/civiclens-validator.git)
   cd civiclens-validator
