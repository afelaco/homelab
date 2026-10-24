.PHONY: build up

build:
	docker compose build

up: build
	docker rm -f synergyzer
	docker compose up --build -d
