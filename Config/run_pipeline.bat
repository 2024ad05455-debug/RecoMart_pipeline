@echo off
REM =========================================
REM RecoMart End-to-End Automated Pipeline
REM Tasks: 2 → 3 → 6 → 7 → 8
REM =========================================

cd /d E:\BITS\DM4ML\RecoMart_pipeline

echo.
echo ==============================
echo RecoMart Pipeline Started
echo ==============================
echo.

REM ---------- TASK 2: DATA INGESTION ----------
echo [TASK 2] Ingesting user events (CSV)...
python ingestion\ingest_events.py

echo [TASK 2] Ingesting product data (API)...
python ingestion\ingest_products_api.py

REM ---------- TASK 3: RAW STORAGE + DB LOAD ----------
echo [TASK 3] Loading user events into PostgreSQL...
python ingestion\load_events_to_postgres.py

echo [TASK 3] Loading product data into PostgreSQL...
python ingestion\load_products_to_postgres.py

REM ---------- TASK 6: FEATURE ENGINEERING ----------
echo [TASK 6] Running feature engineering...
python features\feature_engineering.py

REM ---------- TASK 7: FEATURE STORE / REGISTRY ----------
echo [TASK 7] Registering features into feature store...
python registry\register_features.py

REM ---------- TASK 7: FEATURE STORE / REGISTRY ----------
echo [TASK 7] Registering features into feature store...
python registry\register_features.py

REM ---------- TASK 8: DATA VERSIONING & LINEAGE ----------
echo [TASK 8] Versioning datasets and tracking lineage...

dvc add data/raw
dvc add data/processed
git add .
git commit -m "Auto dataset version update"

echo [TASK 8] Data versioning completed

echo.
echo ==============================
echo RecoMart Pipeline Completed
echo ==============================
echo.


