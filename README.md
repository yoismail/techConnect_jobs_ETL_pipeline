````markdown
# TechConnect Jobs ETL Pipeline

A production-style Python ETL pipeline that extracts UK **Data Engineer** job listings from the **DWP Find a Job** platform, stores raw CSV outputs, transforms the dataset into analytics-ready format, and orchestrates the full workflow using modular scripts.

---

## Project Overview

This project demonstrates practical data engineering skills through a real-world web data pipeline.

The workflow:

1. Extracts job listings from the DWP Find a Job website  
2. Saves raw job listing data into CSV files  
3. Cleans and transforms the extracted dataset  
4. Engineers new columns such as city and experience level  
5. Produces a structured output ready for reporting or database loading  

---

## Key Features

- Web scraping using `requests` + `BeautifulSoup`
- Single-page extraction
- Multi-page paginated extraction
- CSV data lake style outputs
- Data transformation with `pandas`
- Column normalization
- Datetime conversion
- Feature engineering
- Reusable colored logging utility
- Pipeline orchestration script
- Wipe/reset utility for reruns

---

# Project Structure

```text
techconnect_jobs/
│
├── data/
│   └── job_listings/
│       ├── job_listings.csv
│       ├── job_listings_all.csv
│       └── job_listings_transformed.csv
│
├── etl/
│   ├── extract.py
│   ├── extract_all.py
│   ├── transform.py
│   ├── logger.py
│   ├── run_all.py
│   └── wipe_all.py
│
├── requirements.txt
└── README.md
````

---

# ETL Pipeline Breakdown

---

## 1. Extract Single Page

### File:

```python
etl/extract.py
```

Extracts job listings from the first results page.

### Output:

```text
data/job_listings/job_listings.csv
```

### Fields Captured:

* Title
* Link
* Date Posted
* Company
* Location
* Salary

---

## 2. Extract All Pages

### File:

```python
etl/extract_all.py
```

Loops through multiple search result pages and extracts all available listings.

### Output:

```text
data/job_listings/job_listings_all.csv
```

### Notes:

* Uses pagination logic
* Logs number of jobs found per page
* Handles missing salary/location/company values

---

## 3. Transform Data

### File:

```python
etl/transform.py
```

Loads extracted CSV data and applies transformations.

### Transformations Performed:

### Column Standardization

```text
Title → title
Date Posted → date_posted
```

### Datetime Conversion

```python
date_posted → datetime
```

### City Extraction

Example:

```text
London, Greater London → London
```

### Experience Level Classification

Based on job title keywords:

| Keyword    | Output      |
| ---------- | ----------- |
| Senior     | Senior      |
| Junior     | Junior      |
| Lead       | Lead        |
| Principal  | Principal   |
| Manager    | Manager     |
| Head       | Head        |
| None Found | Entry-Level |

### Final Output:

```text
data/job_listings/job_listings_transformed.csv
```

---

## 4. Logging Utility

### File:

```python
etl/logger.py
```

Reusable logging module with:

* Colored terminal output
* Section dividers
* Runtime tracking decorator

Example:

```text
🔷 Extracting Job Listings
⏱️ Step completed in 2.31s
```

---

## 5. Wipe Utility

### File:

```python
etl/wipe_all.py
```

Deletes generated data folders/files for clean reruns.

### Usage:

```bash
python -m etl.wipe_all all
```

Modes:

```text
transformed
all listings
all
```

---

## 6. Full Pipeline Runner

### File:

```python
etl/run_all.py
```

Runs the full ETL flow automatically:

```text
wipe → extract → extract_all → transform
```

### Run:

```bash
python -m etl.run_all
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yoismail/techConnect_jobs_ETL_pipeline.git
cd techconnect_jobs
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

### Activate (Windows)

```bash
.\venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

```text
requests
bs4
pandas
```

---

# How To Run

## Single Page Extraction

```bash
python -m etl.extract
```

---

## Multi Page Extraction

```bash
python -m etl.extract_all
```

---

## Transform Dataset

```bash
python -m etl.transform
```

---

## Full Pipeline

```bash
python -m etl.run_all
```

---

## Wipe Outputs

```bash
python -m etl.wipe_all all
```

---

# Output Files

| File                         | Purpose                      |
| ---------------------------- | ---------------------------- |
| job_listings.csv             | First page raw extract       |
| job_listings_all.csv         | All pages raw extract        |
| job_listings_transformed.csv | Clean analytics-ready output |

---

# Technical Skills Demonstrated

* Python scripting
* ETL pipeline architecture
* Web scraping
* Data cleaning
* Feature engineering
* File system automation
* Logging & monitoring
* Workflow orchestration
* Reproducible pipelines
* Analytics-ready dataset creation

---

# Future Improvements

* PostgreSQL database loading
* Airflow scheduling
* Salary min/max numeric parsing
* Remote / Hybrid classification
* Duplicate detection
* Unit testing
* Dockerization
* Cloud deployment (AWS)

---

# Author

**Yomi Ismail**
Data Engineer | Python | SQL | ETL | PostgreSQL | Analytics Engineering

---

```
```
