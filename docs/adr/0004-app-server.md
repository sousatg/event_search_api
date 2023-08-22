# App Server

In the context of the Search API, I decided to use Uvicorn agains Gunicorn to achieve a better performance, scalability and resource consuption given that the traffic of our API is 100% non blocking I/O.

## Considered Options

### Gunicorn
Bad, only supports WSGI

### Uvicorn
Good, Supports the ASGI protocol
Good, Allow to use coroutines with Flask 
Good, Handle high nember of concurrent connections and perform non-blocking I/O operations
Bad, Low capabilities as a workers manager

## Links
[Flask: Using async and await](https://flask.palletsprojects.com/en/2.3.x/async-await/)