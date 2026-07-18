#  Frontend User Interface

[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?logo=typescript&logoColor=white)](https://typescriptlang.org)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?logo=vite&logoColor=white)](https://vitejs.dev)
[![Framer Motion](https://img.shields.io/badge/Framer_Motion-11.0-0055FF?logo=framer&logoColor=white)](https://www.framer.com/motion/)

This directory contains the user-facing application for the Intelligent OCR System. It is designed to provide a seamless, premium, and highly interactive experience for users submitting images for prediction.

##  Design Philosophy

A backend is only as good as the interface that exposes it. This frontend was engineered with **extreme attention to detail**:

1. **State-Driven UX:** The application fluidly transitions through 5 distinct UI states (`idle`, `dragging`, `loading`, `success`, `error`) ensuring the user is always informed of the system's status.
2. **Micro-Interactions:** Using `framer-motion`, every user action triggers a physical response—from the bouncy drag-and-drop scale effect to the simulated "laser scanning" line during network requests.
3. **Modern Aesthetics:** Utilizes Tailwind CSS for complex glassmorphism (backdrop blurs, translucent borders) and dynamic background glow effects that react to application state.
4. **Type Safety:** 100% written in strict TypeScript to prevent runtime errors and ensure a robust contract with the FastAPI backend.

## Architecture & Tools

* **Vite:** Chosen over Create React App (CRA) for lightning-fast Hot Module Replacement (HMR) and optimized build times.
* **Axios:** For structured, interceptor-ready HTTP requests handling `multipart/form-data` flawlessly.
* **Tailwind Merge (`twMerge` / `clsx`):** Implemented utility functions to safely merge conditional Tailwind classes without specificity conflicts.

## Running Locally

Ensure you have Node.js installed, then run:

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:5173`. Make sure the Python backend is running simultaneously on `http://localhost:8000` so predictions can be processed!
