import requests

url = "http://localhost:8000/predict"
# Pointing to the image file in the parent directory
with open('../ocr-images/ann.png', 'rb') as img:
    response = requests.post(url, files={'file': img})
    
print("Server Response:", response.json())
