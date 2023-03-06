.DEFAULT_GOAL := help
help:       ## show this help.
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

COMPOSE := docker-compose.dev.yml

down:       ## docker-compose down -v
	docker-compose -f ${COMPOSE} down -v

up:         ## docker-compose up -dV --build
	docker-compose -f ${COMPOSE} up -dV --build

restart: down up    ## restart with "down" and "up" commands

ps:         ## docker-compose ps
	docker-compose -f ${COMPOSE} ps

logs:       ## docker-compose logs -f ${SVC}
	docker-compose -f ${COMPOSE} logs -f ${SVC}

exec:       ## docker-compose exec ${SVC} sh
	docker-compose -f ${COMPOSE} exec ${SVC} sh
