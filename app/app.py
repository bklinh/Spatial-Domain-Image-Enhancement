from flask import Flask, request, send_file, render_template, jsonify
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
from io import BytesIO
import numpy as np
import cv2
from skimage.filters import threshold_otsu
from skimage.morphology import dilation, erosion, square
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift
from sklearn.decomposition import PCA

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

def dft_filtering(image, filter_type='lowpass', cutoff=30):
    img_array = np.array(image.convert('L'))
    dft = fftshift(fft2(img_array))
    rows, cols = img_array.shape
    crow, ccol = rows // 2, cols // 2

    mask = np.zeros_like(img_array)
    if filter_type == 'lowpass':
        mask[crow-cutoff:crow+cutoff, ccol-cutoff:ccol+cutoff] = 1
    elif filter_type == 'highpass':
        mask[:, :] = 1
        mask[crow-cutoff:crow+cutoff, ccol-cutoff:ccol+cutoff] = 0

    dft_filtered = dft * mask
    img_back = np.abs(ifft2(ifftshift(dft_filtered)))
    return Image.fromarray(np.clip(img_back, 0, 255).astype(np.uint8))

def pca_object_recognition(image, num_components=10):
    img_array = np.array(image.convert('L')).reshape(-1, 1)
    pca = PCA(n_components=num_components)
    transformed = pca.fit_transform(img_array)
    reconstructed = pca.inverse_transform(transformed).reshape(image.size[::-1])
    return Image.fromarray(np.clip(reconstructed, 0, 255).astype(np.uint8))

def image_restoration(image, kernel_size=3):
    img_array = np.array(image.convert('L'))
    restored_img = cv2.medianBlur(img_array, kernel_size)
    return Image.fromarray(restored_img)

def morphological_operation(image, operation='dilation', kernel_size=3):
    img_array = np.array(image.convert('L'))
    kernel = square(kernel_size)
    if operation == 'dilation':
        processed_img = dilation(img_array, kernel)
    elif operation == 'erosion':
        processed_img = erosion(img_array, kernel)
    return Image.fromarray((processed_img * 255).astype(np.uint8))

def otsu_thresholding(image):
    img_array = np.array(image.convert('L'))
    threshold = threshold_otsu(img_array)
    binary_img = img_array > threshold
    return Image.fromarray((binary_img * 255).astype(np.uint8))

def dct_image_compression(image, quality=50):
    img_array = np.array(image)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encimg = cv2.imencode('.jpg', img_array, encode_param)
    decimg = cv2.imdecode(encimg, 1)
    return Image.fromarray(decimg)

# Routes

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/process-image", methods=["POST"])
def process_image():
    if 'file' not in request.files or 'transformation' not in request.form:
        return jsonify({"error": "File or transformation not provided"}), 400

    file = request.files['file']
    transformation = request.form['transformation']

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
        elif transformation == "Low-pass Filter":
            img = dft_filtering(img, filter_type='lowpass')
        elif transformation == "High-pass Filter":
            img = dft_filtering(img, filter_type='highpass')
        elif transformation == "PCA Object Recognition":
            img = pca_object_recognition(img)
        elif transformation == "Image Restoration":
            img = image_restoration(img)
        elif transformation == "Dilation":
            img = morphological_operation(img, operation='dilation')
        elif transformation == "Erosion":
            img = morphological_operation(img, operation='erosion')
        elif transformation == "Otsu Thresholding":
            img = otsu_thresholding(img)
        elif transformation == "DCT Compression":
            img = dct_image_compression(img)
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
