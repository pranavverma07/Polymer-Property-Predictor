# 🧪 Polymer Property Prediction

A machine learning web application that predicts essential polymer properties using SMILES (Simplified Molecular Input Line Entry System) strings. The app provides both numerical predictions and descriptive summaries, helping users assess polymer suitability for scientific or industrial applications.

---

## 🚀 Features

- 🧬 **Input SMILES** and predict:
  - Density
  - Refractive Index
  - Dielectric Constant (DC)
  - Thermal Conductivity
- 🧠 Powered by LightGBM and RDKit
- 🌐 React frontend with Flask backend
- 💬 AI-generated descriptions of polymer properties
- 💾 Caching using MongoDB to avoid repeated generation
- 🔗 REST API interface for easy integration

---

## 🖼️ Demo
![image](https://github.com/user-attachments/assets/d6ba6146-761f-46a3-bdb2-64710d8d3f12)
![image](https://github.com/user-attachments/assets/840f752a-a462-4ebc-83e9-a5c9c554f448)


---

## 🧰 Tech Stack

### 🧠 Machine Learning & Chemistry
- `RDKit`: Molecular descriptor extraction
- `LightGBM`: Regression model for property prediction
- `Pandas`, `NumPy`: Data manipulation

### 🧪 Backend
- `Flask`: API server
- `MongoDB`: Caching previously generated outputs
- `Python`: Core backend logic

### 💻 Frontend
- `React.js`: Interactive UI
- `Axios`: API requests to Flask backend

---

## 📦 Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js & npm
- MongoDB running locally or remotely

---

### 🔧 Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
