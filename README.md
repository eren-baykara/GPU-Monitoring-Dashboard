# 📊 Local GPU Monitoring Dashboard

A lightweight, real-time dashboard to monitor GPU resources (Memory, Temperature, Usage) on local Deep Learning workstations. 

Built with **Streamlit**, designed to run silently in the background using Windows automation scripts.

## 🚀 Key Features
* **Real-Time Visualization:** Tracks GPU Memory usage, Fan speed, and Temperature instantly.
* **Process Monitoring:** Shows which processes (PID) are consuming the GPU memory.
* **Background Service:** Includes `.bat` and `.vbs` scripts to run the dashboard as a hidden background service on Windows startup.
* **Alert System:** Visual indicators for high temperature or memory bottlenecks.

## 🛠️ Technology Stack
* **Python 3.x**
* **Streamlit:** For the interactive web interface.
* **GPUtil / NVIDIA-SMI:** To fetch hardware metrics.
* **Windows Scripting (Batch/VBS):** For task automation and silent execution.
