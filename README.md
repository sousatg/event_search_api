## Installation

### Setup
#### What you'll need
- [Git](https://git-scm.com/)
- [Python 3.10](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker-Compose](https://docs.docker.com/compose/)
- make ([Windows - CMD](http://gnuwin32.sourceforge.net/packages/make.htm), MacOS - brew, Ubuntu/WSL - apt)

#### Clone the Repository
```
git@github.com:FeverCodeChallenge/GilSousa.git
```

#### Change directories into the main project folder
```
cd GilSousa
```

#### Create a Virtualenv and install dependencies

```
python3 -m venv env
source /env/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.text
```

#### Start the project
1. Start Postgres and RabbitMQ using `docker-compose up -d`
2. Make sure the images are running with `docker ps`
3. Start the API server with `make server`
4. Start the cron job by going to `src` foler and executing `celery -A worker beat -l INFO`
5. Start the task runner by going to `src` foler and executing `celery -A worker worker -l INFO`

### Useful commands
- `make tests` - will run all tests

## Architecture

## Component Diagram

![Component Diagram](/docs/component_diagram.png)
