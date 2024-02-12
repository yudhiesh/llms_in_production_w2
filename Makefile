.PHONY: restart start stop

restart:
	$(MAKE) stop
	$(MAKE) start

start:
	docker compose up --build -d

stop:
	docker compose down -v
