# Spatial-Domain-Image-Enhancement
This repository contains a web-based application for enhancing images with various techniques in the spatial domain. The core functionality includes image enhancement methods, which are accessible through an intuitive GUI built with Flask. This application allows users to apply transformations to images, making it easier to explore image enhancement techniques.

This project is part of the "**CSE3062: Computer Vision**" course.

## Image Enhancement Methods
The image enhancement techniques covered in this application include several methods from the spatial domain, such as:

- **Point Processing**: Direct manipulation of pixel values, which allows transformations like brightness adjustment and contrast enhancement.
- **Histogram Manipulation**: Techniques for enhancing image contrast through histogram equalization and histogram matching.
- **Spatial Filtering**: Application of filters for smoothing, sharpening, and edge detection.

These methods are demonstrated in the **Image_Enhancement.ipynb Jupyter Notebook**, where each technique is applied to images in a step-by-step approach. The notebook serves as a foundation for the transformations available in the web application.

## Web Application Features
- **Image Upload**: Upload images from the local machine or capture using a camera.
- **Dynamic Image Enhancement**: Apply various enhancement techniques from the spatial domain.
- **Responsive Interface**: View the original and transformed images side-by-side.
- **Smooth UI Interactions**: Animated buttons, hover effects, and intuitive dropdown selections for transformation options.

### Run the Application
**1. Clone the repository**
```bash
git clone https://github.com/bklinh/Spatial-Domain-Image-Enhancement.git
```
**2. Set up virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
```
**3. Install dependencies**
```bash
pip install Flask
pip install opencv-python
pip install numpy
```
**4. Run Flask application**
```bash
flask run
```
**5. Access the application**
Open a browser and go to http://127.0.0.1:5000/

### Usage
1. **Upload an Image**: Click "Choose File" or use "Capture from Camera".
2. **Select Transformation**: Choose a transformation from the "Image Enhancement" dropdown.
3. **Submit**: Click "Submit" to apply the transformation.
4. **View Results**: The original and enhanced images appear side-by-side with visual effects.
