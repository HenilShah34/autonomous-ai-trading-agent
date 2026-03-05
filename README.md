# Autonomous AI Trading Agent

An autonomous AI-powered trading intelligence system that collects live market data, calculates technical indicators, and visualizes insights in real time.

---

## Features

- Real-time market monitoring for:
  - Gold
  - Silver
  - Crude Oil
  - S&P 500

- Automated market data collection using **Playwright**
- Backend API built with **FastAPI**
- High-frequency time-series data stored in **PostgreSQL (TimescaleDB)**
- Parallel browser automation using **multiprocessing**
- Technical indicators:
  - MA20
  - MA50
  - MA100
  - MA200
- Interactive live dashboard built with **React**

---

## Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- TimescaleDB
- Playwright
- Multiprocessing

### Frontend
- React
- TailwindCSS
- Vite

---

## System Architecture


Playwright Scrapers
│
▼
Market Data Collection
│
▼
PostgreSQL (TimescaleDB)
│
▼
FastAPI Backend API
│
▼
React Dashboard


---

## Installation

### 1. Clone the Repository


git clone https://github.com/HenilShah34/autonomous-ai-trading-agent.git

cd autonomous-ai-trading-agent


---

### 2. Backend Setup


cd backend

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt


Run the market scrapers:


python run_all_markets.py


Start the backend API:


uvicorn api:app --reload


---

### 3. Frontend Setup


cd frontend

npm install
npm run dev


The dashboard will run at:


http://localhost:5173


---

## Dashboard

The dashboard displays:

- Live market prices
- Moving averages
- Technical indicators
- Market trend visualization

*(You can add a screenshot here later)*

---

## Author

**Henil Shah**

GitHub  
https://github.com/HenilShah34
