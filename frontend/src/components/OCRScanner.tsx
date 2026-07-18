import React, { useState, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { UploadCloud, CheckCircle, AlertCircle, Loader2 } from 'lucide-react';
import axios from 'axios';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

/** Utility for clean tailwind class merging */
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

type ScanState = 'idle' | 'dragging' | 'loading' | 'success' | 'error';

export default function OCRScanner() {
  const [state, setState] = useState<ScanState>('idle');
  const [prediction, setPrediction] = useState<number | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dragCounter = useRef(0);

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (state !== 'loading' && e.dataTransfer.items && e.dataTransfer.items.length > 0) {
      setState('dragging');
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (state !== 'loading') setState('idle');
  };

  const processFile = async (file: File) => {
    if (!file.type.startsWith('image/')) {
      setState('error');
      setErrorMessage('Please upload a valid image file.');
      return;
    }

    // Create a local preview
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
    
    setState('loading');
    setPrediction(null);
    setErrorMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      // Connect to the modernized FastAPI backend
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      // Artificial delay to show off the scanning animation
      setTimeout(() => {
        setPrediction(response.data.prediction);
        setState('success');
      }, 1500);
      
    } catch (err: any) {
      console.error(err);
      setState('error');
      setErrorMessage(err.response?.data?.detail || 'Failed to connect to the OCR server.');
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (state === 'loading') return;
    
    const file = e.dataTransfer.files?.[0];
    if (file) processFile(file);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) processFile(file);
  };

  const resetScanner = () => {
    setState('idle');
    setPrediction(null);
    setPreviewUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  return (
    <div className="w-full max-w-md mx-auto relative group">
      {/* 
        VISUAL DEPTH: Multi-layered background glow that pulses 
        subtly based on the interaction state.
      */}
      <div 
        className={cn(
          "absolute -inset-1 rounded-2xl blur-xl opacity-25 transition-all duration-700",
          state === 'idle' ? "bg-blue-500/30 group-hover:bg-blue-400/50" : "",
          state === 'dragging' ? "bg-indigo-500 opacity-70 scale-105" : "",
          state === 'loading' ? "bg-amber-500/50 animate-pulse" : "",
          state === 'success' ? "bg-emerald-500/60" : "",
          state === 'error' ? "bg-red-500/60" : ""
        )}
      />

      {/* 
        MAIN CONTAINER: Glassmorphism effect with backdrop-blur
        and tactile inner borders.
      */}
      <motion.div
        layout
        className="relative bg-slate-900/80 backdrop-blur-xl border border-white/10 shadow-2xl rounded-2xl overflow-hidden"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 300, damping: 25 }}
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
      >
        {/* INVISIBLE DRAG OVERLAY - PREVENTS CHILD HOVER FLICKER */}
        {state === 'dragging' && (
          <div 
            className="absolute inset-0 z-50 rounded-2xl"
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
          />
        )}

        <div 
          className={cn(
            "p-8 sm:p-12 transition-colors duration-300 flex flex-col items-center justify-center text-center min-h-[320px]",
            state === 'dragging' ? "bg-white/[0.02]" : ""
          )}
        >
          
          <AnimatePresence mode="wait">
            {/* IDLE / DRAGGING STATE */}
            {(state === 'idle' || state === 'dragging') && (
              <motion.div
                key="idle"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ type: "spring" }}
                className="flex flex-col items-center gap-y-6"
              >
                <div 
                  className={cn(
                    "p-4 rounded-full border border-dashed transition-all duration-500",
                    state === 'dragging' 
                      ? "border-indigo-400 bg-indigo-500/20 scale-110" 
                      : "border-slate-500 bg-slate-800/50"
                  )}
                >
                  <UploadCloud className={cn(
                    "w-10 h-10 transition-colors",
                    state === 'dragging' ? "text-indigo-400" : "text-slate-400"
                  )} />
                </div>
                
                <div className="space-y-2">
                  <h3 className="text-xl font-semibold text-slate-100 tracking-tight">
                    Upload Digit Image
                  </h3>
                  <p className="text-sm text-slate-400 leading-relaxed max-w-[240px]">
                    Drag and drop your handwritten digit here, or click to browse.
                  </p>
                </div>

                <button 
                  onClick={() => fileInputRef.current?.click()}
                  className="px-6 py-2.5 bg-white text-slate-900 text-sm font-medium rounded-full shadow-[0_0_15px_rgba(255,255,255,0.1)] hover:shadow-[0_0_20px_rgba(255,255,255,0.3)] hover:scale-105 transition-all active:scale-95"
                >
                  Select Image
                </button>
              </motion.div>
            )}

            {/* LOADING STATE */}
            {state === 'loading' && previewUrl && (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center w-full"
              >
                <div className="relative w-32 h-32 rounded-xl overflow-hidden border border-white/10 shadow-inner bg-black">
                  <img src={previewUrl} alt="Preview" className="w-full h-full object-cover opacity-50 grayscale" />
                  
                  {/* Animated Scanner Line */}
                  <motion.div 
                    className="absolute top-0 left-0 w-full h-1 bg-amber-400 shadow-[0_0_10px_rgba(251,191,36,0.8)]"
                    animate={{ top: ["0%", "100%", "0%"] }}
                    transition={{ duration: 1.5, repeat: Infinity, ease: "linear" }}
                  />
                </div>
                <div className="mt-8 flex items-center gap-x-3 text-amber-400">
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span className="text-sm font-medium tracking-wide animate-pulse">Running CV Pipeline...</span>
                </div>
              </motion.div>
            )}

            {/* SUCCESS STATE */}
            {state === 'success' && (
              <motion.div
                key="success"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0 }}
                transition={{ type: "spring", damping: 15 }}
                className="flex flex-col items-center"
              >
                <div className="w-16 h-16 rounded-full bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center mb-6 text-emerald-400">
                  <CheckCircle className="w-8 h-8" />
                </div>
                
                <h4 className="text-slate-400 text-sm font-medium tracking-widest uppercase mb-2">
                  Prediction Result
                </h4>
                
                <motion.div 
                  initial={{ y: 10, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.2 }}
                  className="text-7xl font-bold text-white tracking-tighter mb-8"
                >
                  {prediction}
                </motion.div>

                <button 
                  onClick={resetScanner}
                  className="text-sm text-slate-400 hover:text-white transition-colors underline decoration-slate-600 underline-offset-4"
                >
                  Scan another image
                </button>
              </motion.div>
            )}

            {/* ERROR STATE */}
            {state === 'error' && (
              <motion.div
                key="error"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center text-center"
              >
                <div className="w-12 h-12 rounded-full bg-red-500/20 text-red-400 flex items-center justify-center mb-4">
                  <AlertCircle className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-semibold text-white mb-2">Scanning Failed</h3>
                <p className="text-sm text-slate-400 max-w-[200px] mb-6">{errorMessage}</p>
                <button 
                  onClick={resetScanner}
                  className="px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white text-sm font-medium rounded-full transition-colors"
                >
                  Try Again
                </button>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </motion.div>

      {/* Hidden file input */}
      <input 
        type="file" 
        ref={fileInputRef} 
        onChange={handleFileSelect} 
        accept="image/*" 
        className="hidden" 
      />
    </div>
  );
}
