from flask import Flask, request, send_file, render_template, jsonify
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
from io import BytesIO
import numpy as np

app = Flask(__name__, static_folder="dist", template_folder="dist")

# Image Processing Functions

def linear_transform(image):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(1.5)

def logarithmic_transform(image):
    img_array = np.array(image).astype(np.float32)
    img_array = 255 * np.log1p(img_array) / np.log(256)
    return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))

def power_law_transform(image, gamma=2.0):
    img_array = np.array(image).astype(np.float32) / 255.0
    img_gamma = np.power(img_array, gamma) * 255
    return Image.fromarray(np.clip(img_gamma, 0, 255).astype(np.uint8))

def thresholding(image, threshold=128):
    img_array = np.array(image.convert('L'))
    thresholded = (img_array > threshold) * 255
    return Image.fromarray(thresholded.astype(np.uint8))

def gray_level_slicing(image, min_val=100, max_val=200):
    img_array = np.array(image.convert('L'))
    sliced = np.where((img_array >= min_val) & (img_array <= max_val), 255, img_array)
    return Image.fromarray(sliced.astype(np.uint8))

def bit_plane_slicing(image, plane=4):
    img_array = np.array(image.convert('L'))
    bit_plane = (img_array >> plane) & 1
    bit_plane_img = bit_plane * 255
    return Image.fromarray(bit_plane_img.astype(np.uint8))

def histogram_equalization(image):
    img_array = np.array(image.convert('L'))
    histogram, bins = np.histogram(img_array.flatten(), bins=256, range=[0, 256])
    cdf = histogram.cumsum()
    cdf_normalized = 255 * cdf / cdf[-1]
    img_equalized = np.interp(img_array.flatten(), bins[:-1], cdf_normalized)
    return Image.fromarray(img_equalized.reshape(img_array.shape).astype(np.uint8))

def histogram_matching(image):
    # Placeholder: here, using histogram equalization for demonstration
    return histogram_equalization(image)

def smoothing(image):
    return image.filter(ImageFilter.SMOOTH)

def sharpening(image):
    return image.filter(ImageFilter.SHARPEN)

def edge_detection(image):
    return image.filter(ImageFilter.FIND_EDGES)

# Routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process-image", methods=["POST"])
def process_image():
    if 'file' not in request.files or 'transformation' not in request.form:
        return jsonify({"error": "File or transformation not provided"}), 400

    file = request.files['file']
    transformation = request.form['transformation']
    
    print(f"Received transformation: {transformation}")
    print(f"Received file: {file.filename}")

    try:
        # Open the uploaded image
        img = Image.open(file.stream)

        # Apply selected transformation
        if transformation == "Linear":
            img = linear_transform(img)
        elif transformation == "Logarithmic":
            img = logarithmic_transform(img)
        elif transformation == "Power Law":
            img = power_law_transform(img)
        elif transformation == "Thresholding":
            img = thresholding(img)
        elif transformation == "Gray-level Slicing":
            img = gray_level_slicing(img)
        elif transformation == "Bit Plane Slicing":
            img = bit_plane_slicing(img)
        elif transformation == "Histogram Equalization":
            img = histogram_equalization(img)
        elif transformation == "Histogram Matching":
            img = histogram_matching(img)
        elif transformation == "Smoothing":
            img = smoothing(img)
        elif transformation == "Sharpening":
            img = sharpening(img)
        elif transformation == "Edge Detection":
            img = edge_detection(img)
        else:
            return jsonify({"error": f"Transformation '{transformation}' not recognized"}), 400

        # Save processed image to a BytesIO object
        img_io = BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)

        return send_file(img_io, mimetype="image/png")
    except Exception as e:
        print(f"Processing error: {e}")
        return jsonify({"error": "Processing failed"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
