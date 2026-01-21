#!/bin/bash

echo "🏥 Starting FDA FAERS Data Quality & Safety Dashboard..."
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo "Launching Streamlit dashboard..."
echo ""
echo "Dashboard will open in your browser at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run app.py
