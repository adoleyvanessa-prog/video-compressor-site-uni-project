# Sustainable Video Compression Web App  
*A final-year BSc Digital Media Computing dissertation project by Vanessa Addo*

This repository contains the artefact from my final-year dissertation on **developing sustainable video compression techniques** to help reduce the carbon footprint of digital media. The project investigates how different **codecs (H.264/H.265)**, **CRF values**, and **encoding presets** affect:

- File size  
- Compression speed  
- Estimated CPU energy usage  
- Overall sustainability of video processing

The prototype includes:

1. A **Python/FFmpeg command-line tool**  
2. A **Flask web application** that allows users to upload, compress, and download videos using sustainable compression settings.

---

## Why This Project Was Created

Video streaming contributes massively to global internet traffic and digital energy consumption. However, most compression tools focus only on **speed** or **quality**, not on **energy efficiency** or **environmental impact**.

This project was designed to:

- Investigate how compression settings influence energy use  
- Build a working prototype demonstrating **energy-aware video compression**  
- Make sustainability a key part of video encoding decisions  
- Provide an approachable way for users to experiment with greener compression choices  

This aligns with academic themes in my dissertation, including:  
- Green computing  
- Sustainable algorithms  
- Energy consumption in digital media  
- Compression optimisation techniques  

---

## Features

- **Video upload (up to ~3 minutes)**  
  Supports `.mp4`, `.mkv`, `.avi`, `.mov`
- **Codec selection:**  
  - H.264 (libx264)  
  - H.265 (libx265)
- **Adjustable settings:**  
  - **CRF value** (quality vs compression strength)  
  - **Preset** (speed vs efficiency)
- **FFmpeg-based compression**
- **Estimated energy usage calculation**  
  Based on:  
  `Energy (J) = Time (s) × 15 W`  
  (15W = CPU TDP of the Intel i5-10210U)
- **Results page displays:**  
  - Original size  
  - Compressed size  
  - Time taken  
  - Estimated energy (joules)

## 1st Place Poster Design for Technical Clarity and Innovation
![Poster Preview](static/poster_converted.png)



