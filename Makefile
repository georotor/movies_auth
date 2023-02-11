dev_up:
	docker-compose -f docker-compose.dev.yml up -dV

dev_down:
	docker-compose -f docker-compose.dev.yml down -v

dev_restart: dev_down dev_up
