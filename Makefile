COMPOSE = docker-compose -f docker-compose.yml

build:
	$(COMPOSE) build --no-cache

ps:
	$(COMPOSE) ps
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

frontend-logs:
	$(COMPOSE) logs -f frontend

backend-logs:
	$(COMPOSE) logs -f web

dev:
	$(COMPOSE) up web db frontend

stop:
	$(COMPOSE) stop

.PHONY: build up down migrate logs sh frontend-logs backend-logs dev stop
