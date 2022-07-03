.PHONY: install lint setup

setup:
	./bin/setup

install:
	@echo "==> Installing application dependencies"
	pip install -U --exists-action=s -r requirements.txt

lint:
	flake8
	black --check --fast .

run:
	python manage.py runserver 0.0.0.0:9999
