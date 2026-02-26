# Vital Monitoring and ML Anomaly Detection (Work in Progress)

This project is a Python-based prototype for real-time vital sign monitoring and future machine learning–driven anomaly detection.

The current version simulates biometric data and delivers it through both a console interface and a lightweight web dashboard. The system is being structured to support future integration of real sensor data and time-series analysis models.

No real patient data is used.

---

## Project Goal

The long-term objective is to build a modular pipeline capable of:

- Streaming biometric signals in real time
- Establishing physiological baselines
- Detecting abnormal patterns using statistical and machine learning methods
- Supporting edge-device deployment (e.g., Raspberry Pi)
- Providing visualization for monitoring and research validation

At this stage, the focus is on architecture, data flow, and extensibility rather than model training.

---

## Current Capabilities

The system currently:

- Simulates vital signs:
  - Heart Rate (HR)
  - Oxygen Saturation (SpO₂)
  - Respiratory Rate (RR)
  - Temperature
- Updates values continuously to mimic live sensor behavior
- Exposes a REST API that streams the latest readings
- Displays a live web dashboard built with Flask
- Provides a console-based monitor for debugging and development
- Maintains modular separation between data generation, processing, and presentation

This establishes the foundation needed for future anomaly detection work.

---

## Project Structure

```
pi5_Files/
│
├── app.py                # Flask server and live update loop
├── base.py               # Console monitoring interface
│
├── hr.py                 # Heart rate simulation logic
├── ox.py                 # Oxygen simulation logic
├── respRate.py           # Respiratory rate simulation logic
├── temp.py               # Temperature simulation logic
│
├── templates/
│   └── index.html        # Web dashboard layout
│
├── static/
│   ├── app.js            # Frontend polling and UI updates
│   └── style.css         # Dashboard styling
│
└── .venv/                # Local virtual environment
```

Additional scripts in the repository represent earlier experiments and hardware abstractions and may be refactored or removed as the architecture stabilizes.

---

## How to Run

### 1. Create a Virtual Environment

From the project root:

```
python -m venv .venv
```

### 2. Activate the Environment (Windows)

```
.\.venv\Scripts\activate
```

### 3. Install Dependencies

```
python -m pip install --upgrade pip
pip install flask
```

### 4. Start the Web Dashboard

```
python app.py
```

Open a browser and navigate to:

```
http://127.0.0.1:5000
```

### 5. (Optional) Run the Console Monitor

```
python base.py
```

The console version is primarily used for validating data flow during development.

---

## Development Focus

The active development priorities are:

- Preparing a clean time-series pipeline suitable for ML ingestion
- Ensuring modular sensor abstraction for real hardware integration
- Designing data structures compatible with anomaly detection models
- Avoiding UI-heavy complexity in favor of analyzable data flow

---

## Planned Machine Learning Work

Future stages will introduce:

- Sliding-window feature extraction
- Baseline modeling per vital stream
- Statistical anomaly detection
- Sequence modeling for physiological drift detection
- Evaluation using anonymized or synthetic datasets

The system is being structured so models can be introduced without rewriting the data pipeline.

---

## Data Policy

This project currently uses simulated data only.

Future datasets will be:
- Anonymized
- Non-identifiable
- Used strictly for research and modeling purposes

---

## Intended Applications

This architecture is being designed as a foundation for:

- Edge-based health monitoring systems
- Continuous biometric analysis platforms
- Research prototypes for physiological anomaly detection
- Machine learning pipelines operating on streaming medical signals

---

## Status

| Component | Status |
|----------|--------|
Simulation Engine | Implemented |
Flask Dashboard | Implemented |
Data Streaming API | Implemented |
Sensor Integration | Planned |
ML Pipeline | In Design |
Anomaly Detection Models | Not Yet Implemented |

---

This repository represents an early-stage research and engineering prototype rather than a finished product. The emphasis is on building a reliable pipeline that can support meaningful anomaly detection experimentation in later phases.