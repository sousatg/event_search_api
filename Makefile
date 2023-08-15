run:
	uvicorn src.api.main:asgi_app

tests:
	python -m unittest discover src
