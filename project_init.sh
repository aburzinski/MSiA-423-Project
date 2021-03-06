#!/bin/bash

# Pull raw data
python src/read_historical_files_from_S3.py
python src/pull_daily_data.py

# Create model artifacts
python models/cy_young_model/create_features.py historical
python models/cy_young_model/create_features.py projected
python models/cy_young_model/create_model.py
python models/cy_young_model/predict_daily_rankings.py

python models/mvp_model/create_features.py historical
python models/mvp_model/create_features.py projected
python models/mvp_model/create_model.py
python models/mvp_model/predict_daily_rankings.py

# Format data
python src/combine_stats_files.py current
python src/combine_stats_files.py projected

# Write files to s3
python src/write_to_cloud.py historical
python src/write_to_cloud.py features
python src/write_to_cloud.py projected

# Create and populate database
python models/mlb_database/create_database.py
python src/ingest_data.py