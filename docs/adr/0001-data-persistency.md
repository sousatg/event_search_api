# Data Persistency

Facing the need to keep event data from providers available, I devided to use a relational database (Postgres) and against using a non relational database (Elasticsearch) to achieve the data persistency.

## Considered Options

### Postgres
Good, supported by SQLAlchemy
Good, SQLAlchemy support for async database opreations
Good, easly adaptable for future use cases
Good, easy to improve data availability and accessibility by replication
Bad, harder to handle write operaiton scaling

### ElasticSearch
Good, extensive set of search functionalities
Bad, overkill for the current use case (YAGNI)
Bad, hard to manage and mantain

## Links
[Postgres Replication](https://www.postgresql.org/docs/current/runtime-config-replication.html)
[Connect to PostgreSQL with SQLAlchemy and asyncio](https://makimo.com/blog/connect-to-postgresql-with-sqlalchemy-and-asyncio/)
[Yagni Martin Fowler](https://martinfowler.com/bliki/Yagni.html)
