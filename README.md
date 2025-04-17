# Health Metrics Analyzer

A Python library for analyzing basic health measurements and providing insights about a person's health status based on standard medical guidelines.

Group member: Leo

## Overview

The Health Metrics Analyzer is a command-line tool that processes CSV files containing health metrics data and generates reports on key health indicators. The library focuses on three core health domains:

1. Body Mass Index (BMI) calculation and categorization
2. Blood pressure analysis and categorization
3. Vital signs assessment (heart rate, respiratory rate, temperature)

## Features

- Calculate and interpret BMI values based on height and weight
- Analyze systolic and diastolic blood pressure readings
- Evaluate vital signs against standard healthy ranges
- Process individual or batch health data from CSV files
- Generate simple summary reports for individuals
- Command-line interface for easy interaction

## Architecture

The project follows a modular design with the following components:

```
health_metrics_analyzer/
├── __init__.py
├── cli.py                  # Command-line interface
├── analyzer/
│   ├── __init__.py
│   ├── bmi_analyzer.py     # BMI calculation and classification
│   ├── bp_analyzer.py      # Blood pressure analysis
│   └── vitals_analyzer.py  # Vital signs assessment
├── data/
│   ├── __init__.py
│   └── data_loader.py      # CSV data loading and preprocessing
├── reporting/
│   ├── __init__.py
│   └── report_generator.py # Health summary report generation
└── utils/
    ├── __init__.py
    └── constants.py        # Medical reference values and thresholds
```
