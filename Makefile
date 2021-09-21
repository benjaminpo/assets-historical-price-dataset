.PHONY: up
up:
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt

.PHONY: update-dataset
update-dataset:
	python main.py
	git add .
	git commit -m "update datasets"
	git push -f

.PHONY: update
update:
	git add .
	git commit -m "update"
	git push -f
