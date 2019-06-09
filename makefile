project=whosinfirst
historical=data/historical
projected=data/projected
features=data/features
models=data/model_files
database=data/mlb_database

.PHONY: test app venv clean clean-pyc clean-env clean-tests historical-data daily-data features models predictions statistics aws-s3 database

# Virtual Environment
${project}-env/bin/activate: requirements.txt
	test -d ${project}-env || virtualenv ${project}-env
	pip install -r requirements.txt
	touch ${project}-env/bin/activate

venv: ${project}-env/bin/activate

# Historical Raw Data
${historical}/hittingHistorical.csv ${historical}/pitchingHistorical.csv ${historical}/players.csv ${historical}/teams.csv:
	# The following command pulls already created training data
	python src/read_historical_files_from_S3.py
	# Use the follwing instead to recreate the training data
	# python src/pull_historical_data/py


historical-data: ${historical}/hittingHistorical.csv ${historical}/pitchingHistorical.csv ${historical}/players.csv ${historical}/teams.csv

# Daily Raw Data
${projected}/hittingCurrent.csv ${projected}/hittingProjected.csv ${projected}/pitchingCurrent.csv ${projected}/pitchingProjected.csv:
	python src/pull_daily_data.py

daily-data: ${projected}/hittingCurrent.csv ${projected}/hittingProjected.csv ${projected}/pitchingCurrent.csv ${projected}/pitchingProjected.csv

# Features
${features}/cyYoungFeatureshistorical.csv: ${historical}/pitchingHistorical.csv ${historical}/players.csv ${historical}/teams.csv
	python models/cy_young_model/create_features historical

${features}/cyYoungFeaturesprojected.csv: ${projected}/pitchingProjected.csv ${historical}/players.csv ${historical}/teams.csv
	python models/cy_young_model/create_features projected

${features}/mvpFeatureshistorical.csv: ${historical}/hittingHistorical.csv ${historical}/pitchingHistorical.csv ${historical}/players.csv ${historical}/teams.csv
	python models/mvp_model/create_features historical

${features}/mvpFeaturesprojected.csv: ${projected}/hittingProjected.csv ${projected}/pitchingProjected.csv ${historical}/players.csv ${historical}/teams.csv
	python models/mvp_model/create_features projected

features: ${features}/cyYoungFeatureshistorical.csv ${features}/cyYoungFeaturesprojected.csv ${features}/mvpFeatureshistorical.csv ${features}/mvpFeaturesprojected.csv

# Create Models
${models}/cyYoung.model: ${features}/cyYoungFeatureshistorical.csv
	python models/cy_young_model/create_model.py

${models}/mvp_lr.model ${models}/mvp_rf.model: ${features}/mvpFeatureshistorical.csv
	python models/mvp_model/create_model.py

models: ${models}/cyYoung.model ${models}/mvp_lr.model ${models}/mvp_rf.model

# Create Predictions
${projected}/cyYoungPredictions.csv: ${features}/cyYoungFeaturesprojected.csv ${models}/cyYoung.model
	python models/cy_young_model/predict_daily_rankings.py

${projected}/mvpPredictions.csv: ${features}/mvpFeaturesprojected.csv ${models}/mvp_lr.model ${models}/mvp_rf.model
	python models/mvp_model/predict_daily_rankings.py

predictions: ${projected}/cyYoungPredictions.csv ${projected}/mvpPredictions.csv

# Create statistics files
${projected}/currentStats.csv: ${projected}/hittingCurrent.csv ${projected}/pitchingCurrent.csv
	python src/combine_stats_files.py current

${projected}/projectedStats.csv: ${projected}/cyYoungPredictions.csv ${projected}/mvpPredictions.csv
	python src/combine_stats_files.py projected

statistics: ${projected}/currentStats.csv ${projected}/projectedStats.csv

# Write files to S3

aws-s3:
	python src/write_to_cloud.py historical
	python src/write_to_cloud.py features
	python src/write_to_cloud.py projected



# Create and Populate database
${database}/mlb.db:
	python models/mlb_database/create_database.py
	python src/ingest_data.py

database: ${database}/mlb.db

# Run app
app:
	python app/app.py

# Run test scripts
test:
	pytest

# Clean test folder
clean-tests:
	rm -rf .pytest_cache

# Remove environment
clean-env:
	rm -r ${project}-env

# Remove python cache files
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf .pytest_cache

# Run All Clean Scripts
clean: clean-tests clean-env clean-pyc