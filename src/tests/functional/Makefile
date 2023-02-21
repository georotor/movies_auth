COMPOSE := docker-compose.tests.yml
TEST_FILE := .

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

test_docker:
	docker-compose -f ${COMPOSE} restart tests && docker-compose -f ${COMPOSE} logs -f tests

test_local:
	cd ../.. && python -m pytest tests/functional/src/${TEST_FILE}

restore_dump:
	cat dump.sql | docker exec -i db_test psql -U app -d auth_database_tests
