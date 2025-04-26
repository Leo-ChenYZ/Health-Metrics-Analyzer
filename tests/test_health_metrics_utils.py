"""Tests for SQLite-based health_metrics_utils."""

import os
import sqlite3
from uuid import uuid4

from health_metrics_utils import HealthMetricsDatabase


def test_bmi_and_category() -> None:
    """Test bmi() and bmi_category() functions."""
    test_db = f"test_health_{uuid4()}.db"

    if os.path.exists(test_db):
        os.remove(test_db)

    db = HealthMetricsDatabase(test_db)
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    test_cases = [
        ("2001", 170, 65),  # Normal weight
        ("2002", 160, 45),  # Underweight
        ("2003", 165, 75),  # Overweight
        ("2004", 155, 90),  # Obesity
    ]

    for patient_id, height, weight in test_cases:
        cursor.execute(
            """
            INSERT INTO metrics (
                patient_id, height_cm, weight_kg, waist_cm, 
                systolic_bp, diastolic_bp
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (patient_id, height, weight, 0, 0, 0),
        )

    conn.commit()
    conn.close()

    expected = {
        "2001": "Normal weight",
        "2002": "Underweight",
        "2003": "Overweight",
        "2004": "Obesity",
    }

    for patient_id, expected_category in expected.items():
        metric = db.get_metric(patient_id)
        assert metric is not None
        assert metric.bmi_category() == expected_category

    if os.path.exists(test_db):
        os.remove(test_db)


def test_blood_pressure_category() -> None:
    """Test blood_pressure_category() function."""
    test_db = f"test_health_{uuid4()}.db"

    if os.path.exists(test_db):
        os.remove(test_db)

    db = HealthMetricsDatabase(test_db)
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    test_cases = [
        ("3001", 0, 0, 0, 118, 76),  # Normal
        ("3002", 0, 0, 0, 125, 75),  # Elevated
        ("3003", 0, 0, 0, 135, 85),  # High BP Stage 1
        ("3004", 0, 0, 0, 145, 95),  # High BP Stage 2
    ]

    for patient_id, _, _, _, sys, dia in test_cases:
        cursor.execute(
            """
            INSERT INTO metrics (
                patient_id, height_cm, weight_kg, waist_cm, 
                systolic_bp, diastolic_bp
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (patient_id, 0, 0, 0, sys, dia),
        )

    conn.commit()
    conn.close()

    expected = {
        "3001": "Normal",
        "3002": "Elevated",
        "3003": "High Blood Pressure Stage 1",
        "3004": "High Blood Pressure Stage 2",
    }

    for patient_id, expected_category in expected.items():
        metric = db.get_metric(patient_id)
        assert metric is not None
        assert metric.blood_pressure_category() == expected_category

    if os.path.exists(test_db):
        os.remove(test_db)


def test_waist_to_height_ratio_and_category() -> None:
    """Test waist_to_height_ratio() and waist_to_height_category()."""
    test_db = f"test_health_{uuid4()}.db"

    if os.path.exists(test_db):
        os.remove(test_db)

    db = HealthMetricsDatabase(test_db)
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()

    test_cases = [
        ("4001", 170, 75),  # 75/170 = 0.44 → Low Risk
        ("4002", 160, 90),  # 90/160 = 0.56 → High Risk
        ("4003", 180, 100),  # 100/180 = 0.56 → High Risk
    ]

    for patient_id, height, waist in test_cases:
        cursor.execute(
            """
            INSERT INTO metrics (
                patient_id, height_cm, weight_kg, waist_cm, 
                systolic_bp, diastolic_bp
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (patient_id, height, 0, waist, 0, 0),
        )

    conn.commit()
    conn.close()

    expected = {
        "4001": "Low Risk",
        "4002": "High Risk",
        "4003": "High Risk",
    }

    for patient_id, expected_category in expected.items():
        metric = db.get_metric(patient_id)
        assert metric is not None
        assert metric.waist_to_height_category() == expected_category

    if os.path.exists(test_db):
        os.remove(test_db)
