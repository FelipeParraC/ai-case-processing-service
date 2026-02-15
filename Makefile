setup:
	cp -n .env.example .env || true
	cp -n .env.docker.example .env.docker || true

run:
	docker compose up --build

stop:
	docker compose down

reset:
	docker compose down -v
	docker compose up --build
