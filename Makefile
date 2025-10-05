COMPOSE = docker-compose -f docker-compose.yml

build:
	$(COMPOSE) build --no-cache

up:
	$(COMPOSE) up -d --remove-orphans

down:
	$(COMPOSE) down -v

migrate:
	$(COMPOSE) run --rm web python manage.py migrate

logs:
	$(COMPOSE) logs -f

sh:
	$(COMPOSE) run --rm web sh

.PHONY: build up down migrate logs sh
