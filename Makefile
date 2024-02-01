.PHONY: restart-docker

restart-docker:
	docker-compose down -v
	docker-compose up --build -d
