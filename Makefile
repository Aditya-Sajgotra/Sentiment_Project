install:
	pip install -r requirements.txt
lint:
	pylint app/app.py
test:
	python -m pytest tests/test_working.py