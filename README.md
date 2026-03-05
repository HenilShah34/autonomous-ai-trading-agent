# Autonomous AI Trading Agent

An autonomous AI-powered trading intelligence system that collects live market data, calculates technical indicators, and visualizes insights in real time.

## Features

- Real-time market monitoring for:
  - Gold
  - Silver
  - Crude Oil
  - S&P 500

- Automated data collection using **Playwright**
- Backend API built with **FastAPI**
- Market data stored in **PostgreSQL (TimescaleDB)**
- Parallel browser automation
- Technical indicators:
  - MA20
  - MA50
  - MA100
  - MA200

- Live dashboard built with **React**

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
PostgreSQL Database
│
▼
FastAPI Backend
│
▼
React Dashboard

---

## Installation

### 1 Clone Repository
git clone https://github.com/YOUR_USERNAME/autonomous-ai-trading-agent.git


---

### 2 Backend Setup


cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


Run scrapers


python run_all_markets.py


Start API


uvicorn api:app --reload


---

### 3 Frontend Setup


cd frontend
npm install
npm run dev


---

## Dashboard

The dashboard displays:

- Live market price
- Moving averages
- Technical indicators
- Market trends

---

## Author

Henil Shah

GitHub  
https://github.com/HenilShah34
