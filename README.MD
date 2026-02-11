# Vital Monitoring & Anomaly Detection (WIP)

A modular Python-based vital monitoring system designed to simulate real-time biometric data streams and prepare for future machine learning–based anomaly detection.

> Current version uses simulated (fake) data only.  
> Real-world anonymized data integration and ML components are in progress.

---

## Overview

This project serves as an architectural prototype for a real-time vital monitoring platform.  

The current system:
- Simulates heart rate and sensor data
- Processes data through a modular pipeline
- Displays live console updates using ANSI color codes
- Separates core logic, state management, and UI layers

The long-term goal is to integrate anonymized real-world data and apply machine learning models for anomaly detection.

---

## Project Structure

- core/ System orchestration
- data/ Simulated data generation
- processing/ Data processing pipeline
- sensors/ Sensor abstraction layer (fake sensors for now)
- state/ Application state management
- tests/ Unit and functional tests
- ui/ Console-based output
- utils/ Shared utilities


### Entry Points

- `main.py` – Primary application runner  
- `heartRateLive.py` – Simulated live heart rate stream  
- `HRwire.py` – Hardware abstraction prototype  
- `config.py` – Configuration settings  

---

## Current Status

| Component | Status |
|-----------|--------|
| Modular Architecture | Complete |
| Simulated Data Pipeline | Complete |
| Console UI Output | Complete |
| Real Sensor Integration | Planned |
| Machine Learning Module | Work in Progress |

---

## Machine Learning (Planned)

The ML section will include:

- Time-series feature extraction
- Baseline modeling
- Statistical anomaly detection
- Future supervised models

This will allow the system to move from simulated monitoring to predictive analysis.

---

## Data Plan

Future versions will integrate:
- Anonymized biometric datasets
- Ethical and privacy-conscious data handling
- Secure processing workflows

No real personal health data is currently used.

---

## Tech Stack

- Python
- Modular architecture design
- Console-based UI rendering
- Planned: scikit-learn / PyTorch

---

## Development Notes (To Self)

- Refactor repeated logic across modules  
- Improve separation between processing and UI layers  
- Remove unused experimental scripts  
- Standardize naming conventions  
- Add docstrings and inline documentation  
- Improve configuration structure  
- Replace print-based alerts with structured logging  

---

## Purpose

This project is intended as a foundation for:

- Remote patient monitoring systems
- Edge-device biometric processing
- Healthcare anomaly detection research
- ML-based health monitoring pipelines



