<h1 align="center">🤖 Autonomous AI Trading Agent</h1>

<p align="center">
  <b>An autonomous, real-time market intelligence system that eliminates manual monitoring —</b><br/>
  collecting live multi-asset market data, computing technical indicators, and visualizing insights the moment they happen.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/TimescaleDB-FDB515?style=for-the-badge&logo=timescale&logoColor=black"/>
  <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white"/>
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black"/>
  <img src="https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white"/>
  <img src="https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white"/>
</p>

---

## 🎯 Overview

Manually tracking multiple markets — checking prices, recalculating moving averages, watching for trend shifts — doesn't scale, and it's easy to miss a signal the moment it matters. This system removes that bottleneck entirely.

It runs **parallel browser-automation pipelines** that continuously pull live data across four asset classes, feeds it into a **high-frequency time-series database**, and serves it through a **FastAPI backend** to a **live-updating React dashboard** — so market state, moving averages, and trend signals are always current, with zero manual checking required.

Built for resilience, not just demonstration: the scraping layer auto-restarts on crashes, and the multiprocessing architecture is designed to run unattended for extended periods.

---

## ✨ Features

- **Real-time monitoring across 4 asset classes** — Gold, Silver, Crude Oil, and S&P 500 — tracked simultaneously, not sequentially
- **Zero-touch data collection** via Playwright-driven browser automation, replacing what would otherwise be manual price-checking
- **High-frequency time-series storage** in PostgreSQL with TimescaleDB hypertables, built to handle continuous market data ingestion without degrading query performance
- **Parallel, fault-tolerant architecture** — multiprocessing with auto-restart crash handling, so the system keeps running unattended
- **Automated technical indicators** calculated continuously: MA20, MA50, MA100, MA200
- **Live interactive dashboard** built with React — no manual refresh needed to see current market state

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Data Collection** | Playwright, Multiprocessing |
| **Backend / API** | Python, FastAPI |
| **Database** | PostgreSQL, TimescaleDB |
| **Frontend** | React, TailwindCSS, Vite |

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    A[Playwright Scrapers] -->|Parallel multiprocessing| B[Market Data Collection]
    B --> C[(PostgreSQL / TimescaleDB)]
    C --> D[FastAPI Backend API]
    D --> E[React Dashboard]

    subgraph Assets Tracked
        F[Gold] --> A
        G[Silver] --> A
        H[Crude Oil] --> A
        I[S&P 500] --> A
    end

    D -->|Computes| J[Technical Indicators<br/>MA20 · MA50 · MA100 · MA200]
    J --> E
```

---

## 📸 Dashboard Preview

The dashboard displays:
- Live market prices across all 4 tracked assets
- Real-time moving averages (MA20/50/100/200)
- Technical indicator overlays
- Market trend visualization

### Static Previews
<p align="center">
  <img src="assets/terminal_screenshot.jpeg" alt="Terminal Output" width="450"/>
  &nbsp;&nbsp;
  <img src="assets/dashboard_screenshot.jpeg" alt="Dashboard" width="450"/>
</p>

<p align="center">
  <i>
    Left: Real-time terminal output showing live market data collection and processing.<br/>
    Right: Interactive AI Autonomous Trading Agent dashboard displaying market insights and analytics.
  </i>
</p>

### Live Operations

**Dashboard in Action**
<p align="center">
  <img src="assets/dashboard_output.gif" alt="Dashboard Live Action" width="800"/>
</p>

**Automated Browser Scraping**
<p align="center">
  <img src="assets/browser_output.gif" alt="Browser Automation" width="800"/>
</p>

**Real-Time Terminal Processing**
<p align="center">
  <img src="assets/terminal_output.gif" alt="Terminal Processing" width="800"/>
</p>

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/HenilShah34/autonomous-ai-trading-agent.git
cd autonomous-ai-trading-agent
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run the market scrapers:

```bash
python run_all_markets.py
```

Start the backend API:

```bash
uvicorn api:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The dashboard will run at:

```
http://localhost:5173
```

---

## 📊 Results / Impact

> *Add concrete numbers here once you have them — this section is what turns the project from "a cool build" into proof of engineering impact. Ideas to fill in:*
- Number of data points ingested per day/hour
- Uptime achieved during unattended operation (e.g., "ran continuously for X days without manual intervention")
- Query performance on the TimescaleDB layer (e.g., average query latency on X million rows)
- Reduction in manual monitoring effort compared to checking prices manually

---

## 🔮 Future Improvements

- [ ] Add authentication and multi-user support to the dashboard
- [ ] Expand asset coverage beyond the current 4 markets
- [ ] Add configurable alerting (email/webhook) on indicator threshold crossings
- [ ] Containerize the full stack with Docker Compose for one-command setup
- [ ] Add automated tests for the scraping and indicator-calculation layers

---

## 👤 Author

**Henil Shah**
Software Developer | Backend & Automation Specialist

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/HenilShah34)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/henil-shah-5958b327a)
[![Upwork](https://img.shields.io/badge/Upwork-6FDA44?style=for-the-badge&logo=upwork&logoColor=white)](https://www.upwork.com/freelancers/~01c3c0b0cda5f0df04)
