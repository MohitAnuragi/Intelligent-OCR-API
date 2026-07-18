# ⚙️ Inference Engine & API

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Headless-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)

This directory houses the core intelligence of the application: a custom Optical Character Recognition (OCR) neural network exposed via a high-performance FastAPI microservice.

## 🧠 Why Build From Scratch?

While using TensorFlow or PyTorch is standard practice, this model was implemented from scratch using **pure mathematics and NumPy matrix operations**. 

**For recruiters and engineers**, this demonstrates:
1. Deep understanding of fundamental Machine Learning concepts (Backpropagation, Gradient Descent, Activation Functions).
2. Ability to optimize memory and execution time without relying on heavy abstract frameworks.
3. Competency in translating raw mathematical formulas into efficient, production-ready Python code.

## 🔄 The Data Pipeline

When an image is submitted to the API, it goes through a strict processing pipeline:

1. **In-Memory Extraction:** Raw bytes are decoded directly into an OpenCV matrix. Zero disk I/O ensures sub-millisecond read times.
2. **Computer Vision (OpenCV):**
   * Converted to grayscale.
   * Otsu's Binarization is applied to separate the character from the background.
   * Contours are analyzed to draw a bounding box around the digit.
   * Cropped and resized strictly to a `20x20` grid.
3. **Matrix Flattening:** The grid is normalized and flattened into a 400-element vector.
4. **Feedforward Neural Network:** The vector passes through the hidden layers of our custom network to produce a prediction (0-9).

## 📡 API Contract

**Endpoint:** `POST /predict`  
**Content-Type:** `multipart/form-data`

**Request Example:**
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/digit.png"
```

**JSON Response:**
```json
{
  "prediction": 7,
  "status": "success"
}
```

## 🛠️ Development

To test the backend locally without the frontend:
```bash
cd code
uvicorn main:app --host localhost --port 8000 --reload
```
Navigate to `http://localhost:8000/docs` to use the interactive Swagger UI.
