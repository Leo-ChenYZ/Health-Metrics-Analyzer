# Health Metrics Analyzer

This repository provides a tool for processing basic health metrics data. It includes functions to parse patient health measurements, calculate Body Mass Index (BMI) and categorize it, determine blood pressure categories, and analyze waist-to-height ratios.

*Group member: Leo*

## For End Users

### Setup/Installation

Clone the repository to your local machine.

### Input File Formats

The tool expects one CSV (Comma-Separated Values) file as input:

**Health Metrics Data**: A table containing patient height, weight, waist circumference, and blood pressure readings.

Example file structure:

| PatientID | Height_cm | Weight_kg | Waist_cm | Systolic_BP | Diastolic_BP |
|-----------|-----------|-----------|----------|-------------|--------------|
| 1001      | 170       | 65        | 75       | 118         | 76           |
| 1002      | 160       | 80        | 90       | 140         | 90           |
| 1003      | 180       | 75        | 85       | 125         | 82           |

### Examples

How to use the provided functions:

1. **Parsing data**:
   ```python
   db = parse_health_data("HealthMetricsTable.csv")
   ```

2. **Calculating BMI and its category**:
   ```python
   metric = db.get_metric("1001")  # 1001 is the patient's id
   metric.bmi()  # e.g., 22.5
   metric.bmi_category()  # e.g., "Normal weight"
   ```

3. **Analyzing blood pressure**:
   ```python
   metric.blood_pressure_category()  # e.g., "Normal"
   ```

4. **Calculating waist-to-height ratio and category**:
   ```python
   metric.waist_to_height_ratio()  # e.g., 0.44
   metric.waist_to_height_category()  # e.g., "Low Risk"
   ```

## For Contributors

### Local Testing Instructions

1. Install `pytest` and other necessary dependencies if not already installed:
   ```bash
   pip install -r requirements-test.txt
   ```

2. Run the tests:
   ```bash
   pytest tests/test_health_metrics_utils.py
   ```

### Contributing

1. Fork the repository and create a new branch for your feature or bugfix.
2. Write tests for your changes in `tests/test_health_metrics_utils.py`.
3. Ensure all tests pass by running `pytest`.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License.
