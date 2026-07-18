# Use the official Python 3.11 lightweight image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the project files into the container
COPY . .

# Shift the working directory into the 'code' folder so the neural network can find 'nn.json'
WORKDIR /app/code

# Hugging Face Spaces strictly requires web services to run on port 7860
EXPOSE 7860

# Start the FastAPI server on port 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
