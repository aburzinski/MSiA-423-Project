#!/bin/bash

# Pull raw data
python src/pull_daily_data.py

# Update predictions
python models/cy_young_model/create_features.py projected
python models/cy_young_model/predict_daily_rankings.py

python models/mvp_model/create_features.py projected
python models/mvp_model/predict_daily_rankings.py

# Format data
python src/combine_stats_files.py current
python src/combine_stats_files.py projected

# Write updated files to s3
python src/write_to_cloud.py features
python src/write_to_cloud.py projected

# Update database
python src/ingest_data.py