# 🌍 Air Quality Dashboard

A premium, modern, and fluid air quality monitoring dashboard that provides real-time insights into environmental conditions. Features a sleek "Modern Fluid" aesthetic with automatic theme switching and detailed pollutant analytics.

![Modern Dashboard](https://img.shields.io/badge/UI-Modern%20Fluid-indigo)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![JS](https://img.shields.io/badge/Frontend-Vanilla%20JS-F7DF1E)

## ✨ Features

- **Real-time Monitoring**: Fetches live data using the OpenWeatherMap API.
- **US EPA Standards**: Calculates accurate AQI values (0-500) based on PM2.5 concentrations.
- **Adaptive UI**: Automatically switches between **Dark** and **Light** modes based on system preferences.
- **Fluid Animations**: Staggered entrance animations for a premium user experience.
- **Health Guidance**: Provides tailored health recommendations based on current air quality.
- **Pollutant Analytics**: Interactive charts showing concentrations of PM2.5, PM10, and CO.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **OpenWeatherMap API Key**: Get yours at [OpenWeatherMap](https://openweathermap.org/api).

### 🛠️ Backend Setup

1. **Navigate to the backend directory**:
   ```powershell
   cd backend
   ```

2. **Install dependencies**:
   ```powershell
   pip install fastapi uvicorn requests python-dotenv
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the `backend/` folder and add your API key:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

4. **Start the Server**:
   ```powershell
   uvicorn main:app --reload
   ```
   The backend will be running at `http://127.0.0.1:8000`.

---

### 💻 Frontend Setup

1. **Navigate to the frontend directory**:
   ```powershell
   cd frontend
   ```

2. **Start the Development Server**:
   You can use any local server. The easiest way is using Python:
   ```powershell
   py -m http.server 5500
   ```
   *(Note: Use `py` or `python` depending on your system's configuration.)*

3. **Open in Browser**:
   Visit `http://localhost:5500` to see the dashboard in action!

---

## 📂 Project Structure

```text
AQI/
├── backend/
│   ├── main.py              # FastAPI application & endpoints
│   ├── services/
│   │   └── air_quality.py   # Business logic & AQI calculations
│   └── .env                 # API Keys (gitignored)
├── frontend/
│   ├── index.html           # Main UI structure
│   ├── style.css            # Modern Fluid design system
│   └── script.js            # Interactivity & animations
└── README.md                # Project documentation
```

## 🛠️ Built With

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/)
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism), Vanilla JavaScript, [Chart.js](https://www.chartjs.org/)
- **Data Source**: [OpenWeatherMap Air Pollution API](https://openweathermap.org/api/air-pollution)

---

Developed with ❤️ for a standout portfolio experience.
