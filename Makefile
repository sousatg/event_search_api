run:
	docker-compose up

migrate:
	cd src; flask --app api.main:app db upgrade

server:
	uvicorn src.api.main:asgi_app --reload

tests:
	python -m unittest discover src

format:
	python -m black . 
