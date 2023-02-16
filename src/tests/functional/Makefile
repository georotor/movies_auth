COMPOSE := docker-compose.tests.yml

down:
	docker-compose -f ${COMPOSE} down -v

up:
	docker-compose -f ${COMPOSE} up -dV --build

restart: down up

ps:
	docker-compose -f ${COMPOSE} ps

logs:
	docker-compose -f ${COMPOSE} logs -f ${SVC}

exec:
	docker-compose -f ${COMPOSE} exec ${SVC} sh

test:
	docker-compose -f ${COMPOSE} restart tests && docker-compose -f ${COMPOSE} logs -f tests
