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
git@github.com:sousatg/event_search_api.git
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
5. Start the cron job `celery -A worker beat -l INFO`
6. Start the task runner `src` foler and executing `celery -A worker worker -l INFO`
7. Start the API server by running `uvicorn api.main:asgi_app --host 0.0.0.0`

### Useful commands
- `make tests` - will run all tests
- `make format` - format the code according to PEP8
- `make migrate` - run migrations
- `make server` - start the uvicorn locally
- `make run` - run docker-compose with all images

## Architecture

![Component Diagram](/docs/diagrams/component_diagram.png)

### ADR (Architectural Decision Records)
- [Data Persistency](/docs/adr/0001-data-persistency.md)
- [Fetch Events From Provider](/docs/adr/0002-fetch-events-from-provider.md)
- [Tasks Queue](/docs/adr/0003-task-queue.md)
- [App Server](/docs/adr/0004-app-server.md)

## The extra mile
Facing the need to scale the application with a focus on performance, I decided to break the functionality of extracting events from the provider and saving them in a database in separate service using task queue to achieve to achieve a high performance of the API.

In the context receiving between 5k/10k request per second on our endpoint the Search API and the Database can be scaled with replication. For the Search API we can have has many replicas as needed since the API is stateless, regarding the Database we would have a primary node responsible for writes and share the binlog with the other replicas.

To optimize the read performance we can also add a application cache-aside strategy and after some monitoring of the user data access patterns select a proper cache eviction policy but until then a least recently used should be alright.

In the context of that the files we get from the provider contains
thousands of events with hundreds of zones each our task queue can scale the ammount of workers as needed. The extraction of events is done in a multithreaded to ensure the optimal use of CPU and Memory in this process. The extraction of events and their processing could have been done in diference tasks and in batches of diferent workers.

Saving the extracted events in the database is already a separated task running async.
