## Installation
### What you'll need
- [Git](https://git-scm.com/)
- [Python 3.10](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker-Compose](https://docs.docker.com/compose/)
- make ([Windows - CMD](http://gnuwin32.sourceforge.net/packages/make.htm), MacOS - brew, Ubuntu/WSL - apt)

### Initial Steps
#### Clone the Repository
```
git@github.com:FeverCodeChallenge/GilSousa.git
```

#### Change directories into the main project folder
```
cd GilSousa
```

### Run with docker compose
```
make run
```

And the application will be runnig at http://localhost:8000

### Run Locally
#### Create a Virtualenv and install dependencies

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

#### Create a .env file
```
cp .dis.env .env
```

Note: Update the necessary values

#### Load the environment variables
```
source .env
```

#### Start the project
1. Start Postgres and RabbitMQ using `docker-compose up -d`
2. Make sure the images are running with `docker ps`
3. CD into the `src` folder
4. Run the migrations with `flask --app api.main:app db upgrade`
5. Start the API server by running `uvicorn api.main:asgi_app --host 0.0.0.0`
6. Start the cron job `celery -A worker beat -l INFO`
7. Start the task runner `src` foler and executing `celery -A worker worker -l INFO`

### Useful commands
- `make tests` - will run all tests

## Architecture

### Component Diagram

![Component Diagram](/docs/component_diagram.png)
