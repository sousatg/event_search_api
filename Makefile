server:
	uvicorn src.api.main:asgi_app --reload

tests:
	python -m unittest discover src
