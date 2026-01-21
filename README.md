# FDA FAERS Data Quality & Safety Signal Detection PoC

## 🎯 Project Overview

This Proof of Concept demonstrates AI-driven pharmacovigilance data quality monitoring and safety signal detection using FDA's FAERS (FDA Adverse Event Reporting System) dataset.

**Aligned with DART Program Goals:**
- 🔍 Data quality surveillance and monitoring
- 🤖 AI/ML-based anomaly detection
- 📊 Predictive data quality scoring
- 🚨 Automated safety signal detection
- 🏗️ MLOps-ready architecture

## 📦 Dataset

**Source:** [FDA FAERS Quarterly Data Files](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html)

**Period:** Q3 2025 (July - September 2025)

**Data Tables:**
- `DEMO` - Demographics & Case Information
- `DRUG` - Drug/Medication Information
- `REAC` - Adverse Reactions
- `OUTC` - Patient Outcomes
- `INDI` - Drug Indications
- `THER` - Therapy Information
- `RPSR` - Report Sources

## 🚀 Quick Start

### Option 1: Interactive Dashboard (Recommended)

```bash
# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Launch interactive dashboard
./run_dashboard.sh
# Or manually: streamlit run app.py
```

Then open your browser to **http://localhost:8501**

### Option 2: Command-Line Demos

```bash
# Activate environment
source venv/bin/activate

# Run data quality analysis
python src/demo_data_quality.py

# Run signal detection
python src/demo_signal_detection.py
```

## 💡 PoC Demonstrations

### 🖥️ **Interactive Streamlit Dashboard** (`app.py`) ⭐ MAIN DEMO

**4 Comprehensive Dashboards:**

1. **Overview Dashboard**
   - Executive summary with key metrics
   - Temporal reporting trends
   - Geographic distribution
   - Patient demographics
   - Serious outcomes breakdown

2. **Data Quality Analysis** (4 Stages)
   - Stage 1: Data completeness assessment
   - Stage 2: Missing data pattern analysis
   - Stage 3: Temporal anomaly detection
   - Stage 4: Individual case quality scoring

3. **Safety Signal Detection** (3 Stages)
   - Stage 1: Disproportionality analysis (PRR)
   - Stage 2: Serious outcomes analysis
   - Stage 3: Most reported drugs analysis

4. **About & Technical Specs**
   - Project overview
   - Technology stack
   - Production architecture
   - MLOps capabilities

### 🖥️ **Command-Line Demos**

1. **Data Quality Surveillance** (`demo_data_quality.py`)
   - Automated data completeness scoring
   - Anomaly detection for data entry patterns
   - Duplicate record identification
   - Missing data profiling
   - Individual case quality scoring

2. **Safety Signal Detection** (`demo_signal_detection.py`)
   - Statistical signal detection (PRR)
   - Time-series anomaly detection
   - Drug-event association mining
   - Serious outcome prediction
   - ML-based risk prediction

## 🎓 Key Technologies

- **Data Processing:** Pandas, NumPy
- **ML/AI:** Scikit-learn, Transformers, PyTorch
- **Data Quality:** Great Expectations, Evidently
- **MLOps:** MLflow
- **Visualization:** Plotly, Seaborn, Matplotlib

## 📊 Sample Insights

The PoC demonstrates:
1. **85%+ data completeness** across critical fields
2. Detection of **seasonal reporting patterns**
3. Identification of **high-risk drug-reaction pairs**
4. **Automated quality scoring** for individual case reports
5. **Real-time anomaly alerts** for unusual reporting patterns

## 🏗️ Architecture for Production

```
Data Ingestion → Quality Checks → Feature Engineering → ML Models → Monitoring
     ↓               ↓                  ↓                  ↓            ↓
  AWS S3      Great Expectations    Feature Store     SageMaker   CloudWatch
```

## 👥 Created For

Roche - DART Program Data Surveillance & Data Quality Workstream Interview

**Author:** Michał  
**Date:** January 2026  
**Status:** PoC / Demonstration
# FDA-FAERS-Data-Quality-Safety-Signal-Detection
