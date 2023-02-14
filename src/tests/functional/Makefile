down:
	docker-compose -f docker-compose.tests.yml down -v

up:
	docker-compose -f docker-compose.tests.yml up -dV --build

ps:
	docker-compose -f docker-compose.tests.yml ps

restart: down up

# test:
# 	@restart tests && docker-compose logs -f tests
