# Intelligent OCR API

A high-performance FastAPI microservice for handwritten digit recognition using a custom neural network.

## Architecture & Pipeline

* **Request:** Client submits `multipart/form-data` containing an image file to `POST /predict`.
* **In-Memory Byte Extraction:** Raw bytes are decoded directly into an OpenCV numpy array without disk I/O.
* **OpenCV Preprocessing:** Image is converted to grayscale, thresholded (Otsu's binarization), cropped to the character's bounding box, and resized to a strict 20x20 grid.
* **Mathematical ML Inference:** The grid is flattened into a normalized 400-element vector and fed forward through the pre-loaded custom neural network.
* **Response:** API returns a strictly typed JSON payload containing the predicted digit.

## Performance Metrics

* **Training Data:** Model weights (`nn.json`) are trained from scratch on the standard MNIST dataset. Note: `scikit-learn` is used strictly as a utility to fetch the MNIST dataset during the offline training phase (`train.py`).
* **Inference Engine:** 100% custom mathematical implementation utilizing NumPy matrix operations. Zero dependencies on TensorFlow, PyTorch, or Scikit-Learn for runtime inference.
* **Accuracy:** [XX]%

## API Contract

**Endpoint:** `POST /predict`
**Method:** `POST`
**Content-Type:** `multipart/form-data`

### cURL Example

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/handwritten_digit.png"
```

### JSON Response

```json
{
  "prediction": 7,
  "status": "success",
  "type": "test",
  "result": 7
}
```
*(Note: 'type' and 'result' keys are maintained strictly for legacy frontend compatibility)*

## Local Development / Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn opencv-python numpy python-multipart scikit-learn
uvicorn main:app --host localhost --port 8000 --reload
```

## Documentation

Full interactive OpenAPI documentation (Swagger UI) is automatically generated and accessible at `http://localhost:8000/docs` while the server is running locally.
