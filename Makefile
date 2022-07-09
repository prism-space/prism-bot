.PHONY: install lint setup

setup:
	./bin/setup

install:
	@echo "==> Installing application dependencies"
	pip install -U --exists-action=s -r requirements.txt

lint:
	flake8
	black --check --fast .

run-web:
	python manage.py runserver 0:9999

run-bot:
	python manage.py run-bot
