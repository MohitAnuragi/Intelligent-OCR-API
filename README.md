# 🧠 Intelligent OCR API System

![OCR System Cover Image](https://socialify.git.ci/MohitAnuragi/Intelligent-OCR-API/image?description=1&font=Inter&language=1&name=1&owner=1&pattern=Circuit%20Board&theme=Dark)

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)](https://docker.com)

Welcome to the **Intelligent OCR API System**. This project is a modern, full-stack Optical Character Recognition (OCR) application that seamlessly bridges complex Machine Learning with a premium User Experience.

Instead of relying on heavy pre-packaged ML frameworks like TensorFlow or PyTorch, this project features a **custom Neural Network written from scratch** alongside a **hardware-accelerated React interface**.

## ✨ Key Features

* **Custom Neural Network:** A multi-layer perceptron (MLP) built from the ground up using core mathematics and NumPy matrix operations.
* **Computer Vision Pipeline:** Real-time image binarization, thresholding, and contour mapping using OpenCV.
* **Premium UX/UI:** A sleek, glassmorphic drag-and-drop interface powered by Framer Motion animations.
* **Asynchronous API:** Highly concurrent RESTful endpoints powered by FastAPI and Uvicorn.
* **Containerized Deployment:** Ready for the cloud with a minimal, optimized Docker footprint.

## 📁 Monorepo Structure

This repository separates concerns into two specialized workspaces:

1. [**`/frontend` - The User Interface**](./frontend/)
   * **Tech Stack:** React, TypeScript, Vite, Tailwind CSS, Framer Motion.
   * **Highlight:** Focuses on micro-interactions, robust state management, and modern aesthetics.
   
2. [**`/code` - The Inference Engine**](./code/)
   * **Tech Stack:** Python, FastAPI, OpenCV, NumPy.
   * **Highlight:** Focuses on mathematical ML implementation, computer vision preprocessing, and strict API contracts.

---

## 🚀 Quick Start Guide

You can run the entire system locally in under 2 minutes.

### 1. Start the Inference API (Terminal 1)
```bash
pip install -r requirements.txt
cd code
uvicorn main:app --host localhost --port 8000 --reload
```
*API will run on `http://localhost:8000` with Swagger docs at `/docs`.*

### 2. Start the Frontend UI (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```
*UI will run on `http://localhost:5173`.*

---

## 🐳 Docker Deployment

The system is fully containerized for easy cloud deployment (Render, AWS, Railway, etc.).

```bash
# Build the production image
docker build -t intelligent-ocr-api .

# Run the container locally (Exposes on port 8000)
docker run -p 8000:7860 intelligent-ocr-api
```
