import cv2
import numpy as np
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List

# Import the exact legacy neural network from the original implementation
from ocr import OCRNeuralNetwork

# Legacy variables matching the original mathematical implementation
HOST_NAME = 'localhost'
PORT_NUMBER = 8000
HIDDEN_NODE_COUNT = 15

# Global instance for the neural network
nn = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    INFRASTRUCTURE EFFICIENCY: 
    Lifespan context manager ensures neural network weights and training samples 
    are loaded ONCE into memory during FastAPI server startup, completely eliminating
    the overhead of reloading for every API call.
    """
    global nn
    
    # MODEL SERIALIZATION LOADING:
    # Initialize the neural network purely from serialized file ('nn.json').
    # We pass empty data arrays since we are skipping the legacy from-scratch training step,
    # ensuring the model is instantly ready for client inference requests on boot.
    nn = OCRNeuralNetwork(HIDDEN_NODE_COUNT, [], [], [], use_file=True)
    
    yield  # Server accepts incoming requests while yielding
    
    # Graceful shutdown cleanup
    nn = None


# INFRASTRUCTURE: Kill BaseHTTPRequestHandler; Initialize FastAPI
app = FastAPI(title="Modernized OCR Neural Network API", lifespan=lifespan)

# Add CORS middleware so the frontend can communicate seamlessly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DATA VALIDATION: Pydantic models for strict data structure contracts
class PredictResponse(BaseModel):
    prediction: int = Field(..., description="The predicted digit (0-9)")
    status: str = Field(..., description="Status of the request execution")
    # Included for legacy frontend compatibility (ocr.js expects these keys)
    type: str = "test"
    result: int

def preprocess_image(image_bytes: bytes) -> List[int]:
    """
    COMPUTER VISION PIPELINE:
    Preprocesses the raw uploaded image into the exact 1D mathematical vector 
    (400 elements of 1s and 0s) expected by the legacy Neural Network.
    """
    # 1. BYTE EXTRACTION: Decode the bytes directly into an OpenCV numpy array in memory
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Invalid image file format")
    
    # 2. GRAYSCALE CONVERSION: Drop color channels, simplifying the matrix to 2D (intensity only)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 3. BINARIZATION & INVERSION (Thresholding):
    # Apply Otsu's thresholding to automatically find the optimal threshold value.
    # We use cv2.THRESH_BINARY_INV so the background becomes 0 (black) and the character becomes 255 (white).
    # This aligns with the Neural Network's expectation where 1 is the stroke and 0 is the background.
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 4. BOUNDING BOX (Cropping):
    # Find contours (outlines of the character) to crop out excess whitespace
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No character found in the image")
    
    # Find the largest contour assuming it's the digit we want to predict
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding rectangle coordinates and crop the binary image tightly around the digit
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_digit = thresh[y:y+h, x:x+w]
    
    # 5. RESIZING:
    # Resize the cropped digit strictly to a 20x20 grid to match the 400-element input length requirement.
    # cv2.INTER_AREA is often the best interpolation method for shrinking images.
    resized_digit = cv2.resize(cropped_digit, (20, 20), interpolation=cv2.INTER_AREA)
    
    # 6. FLATTENING & NORMALIZATION:
    # We binarize again briefly just in case interpolation added grey pixels (values between 0 and 255)
    _, final_binary = cv2.threshold(resized_digit, 127, 255, cv2.THRESH_BINARY)
    
    # Flatten the 20x20 matrix into a 1D array of 400 elements
    flattened = final_binary.flatten()
    
    # Normalize: Convert 255 (white pixel) to 1, and 0 (black pixel) remains 0
    # This perfectly matches the legacy format (array of 1s and 0s)
    normalized_vector = (flattened / 255.0).astype(int).tolist()
    
    return normalized_vector

# CLEAN APIS: Expose a clean, single asynchronous POST endpoint
@app.get("/")
async def root():
    return {"message": "OCR API is running. Use /predict to submit images."}

@app.post("/predict", response_model=PredictResponse)
async def predict_digit(file: UploadFile = File(...)):
    """
    ASYNC ARCHITECTURE: Handles digit predictions asynchronously.
    Receives an image file upload, executes the Computer Vision preprocessing pipeline,
    hooks into the legacy mathematical prediction logic, and returns a strictly validated JSON payload.
    """
    if nn is None:
        raise HTTPException(status_code=503, detail="Neural network is not initialized")
    
    try:
        # Read the raw bytes into memory (avoids saving to disk)
        image_bytes = await file.read()
        
        # Preprocess the image into the normalized vector
        try:
            image_vector = preprocess_image(image_bytes)
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        
        # ======================================================================
        # HOOKING INTO ORIGINAL MATH IMPLEMENTATION:
        # The legacy server passed `str(payload['image'])` to the predict method.
        # We cast the processed List back to a string representation to guarantee 
        # the original internal numpy matrix transformation in `ocr.py` executes identically.
        # ======================================================================
        prediction_result = nn.predict(str(image_vector))
        
        return PredictResponse(
            prediction=prediction_result,
            status="success",
            type="test",
            result=prediction_result
        )
    except HTTPException:
        # Re-raise already formatted HTTPExceptions
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Powered strictly by Uvicorn, replacing the legacy socket looping execution
    uvicorn.run(app, host=HOST_NAME, port=PORT_NUMBER)
