from api.create_app import create_app
from asgiref.wsgi import WsgiToAsgi
from config.api_config import ApiConfig


app = create_app(ApiConfig())
asgi_app = WsgiToAsgi(app)
