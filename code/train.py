import numpy as np
import cv2
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
import time
import os

# Import the legacy OCR neural network
from ocr import OCRNeuralNetwork

def preprocess_mnist_images(images):
    """
    PREPROCESSING MATCH:
    Resizes 28x28 MNIST images to the 20x20 dimensions expected by the legacy Neural Network.
    Binarizes the pixel values to strictly 0 and 1.
    Returns a list of 400-element 1D vectors.
    """
    processed = []
    # Ensure images are in a numpy array of shape (N, 784)
    images = np.array(images)
    
    for img in images:
        # 1. Reshape the 1D MNIST array back to a 28x28 2D image
        img_2d = img.reshape(28, 28).astype(np.uint8)
        
        # 2. Resize to 20x20 using INTER_AREA for optimal downsampling
        resized = cv2.resize(img_2d, (20, 20), interpolation=cv2.INTER_AREA)
        
        # 3. Binarize: MNIST uses 0-255 scale where digits are bright.
        # We apply thresholding to push pixels > 127 to exactly 1, and background to 0.
        _, binary = cv2.threshold(resized, 127, 1, cv2.THRESH_BINARY)
        
        # 4. Flatten the 2D image into a 1D vector of length 400
        processed.append(binary.flatten().tolist())
        
    return processed

def calculate_loss(nn, sample_data):
    """
    Computes Mean Squared Error (MSE) loss using the legacy network's forward pass.
    """
    loss = 0.0
    for data in sample_data:
        # Forward pass reproducing ocr.py math logic
        y1 = np.dot(np.asmatrix(nn.theta1), np.asmatrix(data['y0']).T)
        sum1 = y1 + np.asmatrix(nn.input_layer_bias)
        y1 = nn.sigmoid(sum1)
        
        y2 = np.dot(np.array(nn.theta2), y1)
        y2 = np.add(y2, nn.hidden_layer_bias)
        y2 = nn.sigmoid(y2)
        
        actual_vals = [0] * 10
        actual_vals[data['label']] = 1
        output_errors = np.asmatrix(actual_vals).T - np.asmatrix(y2)
        
        loss += np.sum(np.square(output_errors))
    
    return loss / len(sample_data)

def main():
    print("Fetching MNIST dataset from OpenML (this may take a minute)...")
    # DATASET LOADING: Fetch the dataset without TensorFlow/PyTorch
    mnist = fetch_openml('mnist_784', version=1, as_frame=False, parser='auto')
    X = mnist.data
    y = mnist.target.astype(int)
    
    print(f"Successfully downloaded {len(X)} samples.")
    print("Preprocessing images (resizing to 20x20 and binarizing)...")
    
    # Process images to match legacy formats
    X_processed = preprocess_mnist_images(X)
    
    # Split into training (60,000) and testing (10,000) sets
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=10000, random_state=42)
    
    # Format data for the legacy train function: array of dicts {'y0': vector, 'label': int}
    train_data = [{'y0': x, 'label': l} for x, l in zip(X_train, y_train)]
    test_data = [{'y0': x, 'label': l} for x, l in zip(X_test, y_test)]
    
    print("Initializing Legacy Neural Network from scratch...")
    HIDDEN_NODE_COUNT = 15
    
    # Initialize without relying on the old data.csv
    # use_file=False prevents loading pre-existing weights and forces random initialization.
    # We pass empty training_indices to bypass the legacy internal __init__ training step.
    nn = OCRNeuralNetwork(num_hidden_nodes=HIDDEN_NODE_COUNT, 
                          data_matrix=[], 
                          data_labels=[], 
                          training_indices=[], 
                          use_file=False)
                          
    EPOCHS = 5
    print(f"Starting CUSTOM TRAINING LOOP for {EPOCHS} epochs over {len(train_data)} samples...")
    
    # We take a small subset for calculating loss quickly so we don't delay printing
    validation_subset = test_data[:500]
    
    for epoch in range(1, EPOCHS + 1):
        start_time = time.time()
        
        # Feed the MNIST training split directly into the custom legacy training loop
        nn.train(train_data)
        
        # Calculate loss on validation subset for visual tracing
        current_loss = calculate_loss(nn, validation_subset)
        
        elapsed = time.time() - start_time
        print(f"Epoch {epoch}/{EPOCHS} | Validation Loss (MSE): {current_loss:.4f} | Time: {elapsed:.2f}s")
        
    print("\nTraining complete! Serializing weights...")
    # MODEL SERIALIZATION: Export the trained weights to the legacy structured JSON format
    nn._use_file = True  # Re-enable file usage so save() executes
    nn.save()            # Writes to 'nn.json' by default
    print(f"Weights successfully saved to nn.json")
    
    print("\nEvaluating model against 10,000 test samples...")
    correct_predictions = 0
    total_samples = len(test_data)
    
    for data in test_data:
        # EVALUATION METRIC: Validate using the exact same predict structure
        prediction = nn.predict(data['y0'])
        if prediction == data['label']:
            correct_predictions += 1
            
    accuracy = (correct_predictions / total_samples) * 100
    
    print(f"==================================================")
    print(f"FINAL EVALUATION METRICS:")
    print(f"Total Test Samples: {total_samples}")
    print(f"Correct Predictions: {correct_predictions}")
    print(f"Accuracy Percentage: {accuracy:.2f}%")
    print(f"==================================================")

if __name__ == "__main__":
    main()
