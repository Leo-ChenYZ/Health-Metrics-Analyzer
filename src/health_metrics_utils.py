"""This module provides utility functions for basic health metrics analysis."""

import sqlite3
from pathlib import Path
from typing import Optional


class HealthMetric:
    """Class representing a patient's health metrics."""

    def __init__(self, patient_id: str, db_path: str = "health_metrics.db"):
        """Initialize a HealthMetric instance."""
        self.patient_id = patient_id
        self._db_path = db_path

    @property
    def height_cm(self) -> Optional[float]:
        """Get the patient's height in centimeters."""
        return self._fetch_metric("height_cm")

    @property
    def weight_kg(self) -> Optional[float]:
        """Get the patient's weight in kilograms."""
        return self._fetch_metric("weight_kg")

    @property
    def waist_cm(self) -> Optional[float]:
        """Get the patient's waist circumference in centimeters."""
        return self._fetch_metric("waist_cm")

    @property
    def systolic_bp(self) -> Optional[float]:
        """Get the patient's systolic blood pressure."""
        return self._fetch_metric("systolic_bp")

    @property
    def diastolic_bp(self) -> Optional[float]:
        """Get the patient's diastolic blood pressure."""
        return self._fetch_metric("diastolic_bp")

    def _fetch_metric(self, column: str) -> Optional[float]:
        """Fetch a specific metric value for the patient from the database."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT {column} FROM metrics WHERE patient_id = ?",
            (self.patient_id,),
        )
        result = cursor.fetchone()
        conn.close()
        return float(result[0]) if result and result[0] is not None else None

    @classmethod
    def from_dict(
        cls, metric_data: dict[str, str], db_path: str = "health_metrics.db"
    ) -> "HealthMetric":
        """Create a HealthMetric instance from a dictionary of data."""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        patient_id = metric_data.get("PatientID", "")
        height_cm = float(metric_data.get("Height_cm") or 0.0)
        weight_kg = float(metric_data.get("Weight_kg") or 0.0)
        waist_cm = float(metric_data.get("Waist_cm") or 0.0)
        systolic_bp = float(metric_data.get("Systolic_BP") or 0.0)
        diastolic_bp = float(metric_data.get("Diastolic_BP") or 0.0)

        cursor.execute(
            """
            INSERT INTO metrics (
                patient_id, height_cm, weight_kg, waist_cm, 
                systolic_bp, diastolic_bp
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                patient_id,
                height_cm,
                weight_kg,
                waist_cm,
                systolic_bp,
                diastolic_bp,
            ),
        )
        conn.commit()
        conn.close()

        return cls(patient_id=patient_id, db_path=db_path)

    def bmi(self) -> Optional[float]:
        """Calculate the patient's Body Mass Index (BMI)."""
        if self.height_cm is None or self.weight_kg is None:
            return None
        height_m = self.height_cm / 100
        return self.weight_kg / (height_m**2)

    def bmi_category(self) -> Optional[str]:
        """Categorize the patient's BMI into standard categories."""
        bmi_value = self.bmi()
        if bmi_value is None:
            return None
        if bmi_value < 18.5:
            return "Underweight"
        elif bmi_value < 25:
            return "Normal weight"
        elif bmi_value < 30:
            return "Overweight"
        else:
            return "Obesity"

    def blood_pressure_category(self) -> Optional[str]:
        """Categorize the patient's blood pressure."""
        if self.systolic_bp is None or self.diastolic_bp is None:
            return None
        if self.systolic_bp < 120 and self.diastolic_bp < 80:
            return "Normal"
        elif 120 <= self.systolic_bp < 130 and self.diastolic_bp < 80:
            return "Elevated"
        elif (130 <= self.systolic_bp < 140) or (80 <= self.diastolic_bp < 90):
            return "High Blood Pressure Stage 1"
        elif (self.systolic_bp >= 140) or (self.diastolic_bp >= 90):
            return "High Blood Pressure Stage 2"
        else:
            return "Hypertensive Crisis"

    def waist_to_height_ratio(self) -> Optional[float]:
        """Calculate the patient's Waist-to-Height Ratio."""
        if self.height_cm is None or self.waist_cm is None:
            return None
        return self.waist_cm / self.height_cm

    def waist_to_height_category(self) -> Optional[str]:
        """Categorize the patient's Waist-to-Height Ratio."""
        ratio = self.waist_to_height_ratio()
        if ratio is None:
            return None
        if ratio <= 0.5:
            return "Low Risk"
        else:
            return "High Risk"


class HealthMetricsDatabase:
    """Class representing a database of patient health metrics."""

    def __init__(self, db_path: str = "health_metrics.db"):
        """Initialize a HealthMetricsDatabase instance."""
        self._db_path = db_path
        self._initialize_db()

    def get_metric(self, patient_id: str) -> Optional[HealthMetric]:
        """Retrieve a HealthMetric for a given patient ID."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT patient_id FROM metrics WHERE patient_id = ?",
            (patient_id,),
        )
        result = cursor.fetchone()
        conn.close()
        if result:
            return HealthMetric(patient_id=result[0], db_path=self._db_path)
        return None

    def get_all_metrics(self) -> dict[str, HealthMetric]:
        """Retrieve all HealthMetric entries in the database."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT patient_id FROM metrics")
        metrics = {
            row[0]: HealthMetric(patient_id=row[0], db_path=self._db_path)
            for row in cursor.fetchall()
        }
        conn.close()
        return metrics

    def _initialize_db(self) -> None:
        """Initialize the database schema."""
        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                patient_id TEXT,
                height_cm REAL,
                weight_kg REAL,
                waist_cm REAL,
                systolic_bp REAL,
                diastolic_bp REAL
            )
            """
        )
        conn.commit()
        conn.close()


def parse_health_data(
    metric_filename: str, db_path: str = "health_metrics.db"
) -> HealthMetricsDatabase:
    """Parse a CSV file into a HealthMetricsDatabase."""
    db_file = Path(db_path)
    if db_file.exists():
        db_file.unlink()

    db = HealthMetricsDatabase(db_path)

    with open(metric_filename) as file:
        headers = file.readline().strip().split(",")
        for line in file:
            values = line.strip().split(",")
            metric_data = dict(zip(headers, values))
            HealthMetric.from_dict(metric_data, db_path)

    return db
