project=whosinfirst
envfile=config/local/${project}env
RAW_DATA=data/sample/music_data_combined.csv
CONFIG=config/config.py
FEATURES=test/model/test/example-features.csv
TMO=models/example-model.pkl

.PHONY: test app venv clean clean-pyc clean-env clean-tests features trained-models


${project}-env/bin/activate: requirements.txt
	test -d ${project}-env || virtualenv ${project}-env
	pip install -r requirements.txt
	touch ${project}-env/bin/activate

venv: ${project}-env/bin/activate

${FEATURES}: ${RAW_DATA} src/generate_features.py
	python run.py generate_features --config=${CONFIG} --input=${RAW_DATA} --output=${FEATURES}

features: ${FEATURES}

${TMO}: ${FEATURES} src/train_model.py
	python run.py train_model --config=${CONFIG} --input=${FEATURES} --output=${TMO}

trained-model: ${TMO}

app
	python run.py app

swagger: app/app.py app/models.py
	python run.py swagger

test:
	pytest

clean-tests:
	rm -rf .pytest_cache

clean-env:
	rm -r ${project}-env

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf .pytest_cache

clean: clean-tests clean-env clean-pyc