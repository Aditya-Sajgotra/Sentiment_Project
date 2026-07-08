install:
	pip install -r requirements.txt
lint:
	pylint app/app.py
test:
	python -n pytest tests/test_working.py