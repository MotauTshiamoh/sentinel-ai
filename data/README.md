# Sentinel AI Dataset

## Primary Dataset

Sentinel AI uses the CICIDS2017 cybersecurity dataset for initial intrusion-detection model development.

The dataset contains benign network traffic and multiple simulated attack categories.

## Directory Structure

- `raw/` — Original downloaded dataset files.
- `processed/` — Cleaned and transformed datasets used for model development.

## Git Policy

Raw and processed datasets are excluded from Git because of their size.

The repository contains the code required to reproduce the data-processing pipeline.