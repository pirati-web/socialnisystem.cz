# SocialniSystem.cz

The purpose of this website is to help people in need to find out what social
care benefits are they entitled to.

It is built using Python on top of [Django](https://www.djangoproject.com/)
web framework and [PostgreSQL](https://www.postgresql.org/) database.

## Development

### Local installation

#### Prerequistes

This assumes you have **Python 3 installed**. To run in default
configuration, you also need **PostgreSQL server** up and running on `5432` port. You
also need a database and user ready. Defaults are:

* **Username**: `socialsystem`
* **Database**: `socialsystem`
* **Password**: `socialsystem`

This can be changed by providing the `DATABASE_DSN` environment variable.

#### Installation

1. Clone the repository and cd into it

        git clone git@github.com:pirati-web/socialnisystem.cz.git
        cd socialnisystem.cz

2. Initialize virtual environment and activate it

        make init-env
        source .env/bin/activate

3. Install dependencies

        make install

4. Run the application

        make run

### Local installation using Docker

This app has docker-compose support prepared out-of-the-box. This will also
run PostgreSQL database in case you don't want to install it locally.

    docker-compose up

### Running tests

First, make sure you have test dependencies installed. Run:

    make install-test

From now on, you can run the test suite using:

    make test


## Configuration

All config is made using environment variables.

| Variable name  | Description                                                           | Required                | Default value                              |
|----------------|-----------------------------------------------------------------------|-------------------------|--------------------------------------------|
| `DEBUG`        | Turns on debug mode if equal to '1'. Shall not be used in production. | No                      | None                                       |
| `SECRET_KEY`   | Key used for encryption. Provide a long random string value.          | Yes if `DEBUG` is False | None                                       |
| `DATABASE_DSN` | Database connection string                                            | No                      | `postgresql://localhost:5432/socialsystem` |


## Production deployment

This application is designed to be deployed as Docker container. Therefore,
you can use your preferred orchestration tool like [Kubernetes](https://kubernetes.io/)
or [Docker swarm](https://github.com/docker/swarm).

Or, you can simply launch it using Docker compose for small-scale installations
and/or testing purposes.

Docker images are continuosly pushed to the Docker Hub
[xaralis/socialsystem](https://hub.docker.com/r/xaralis/socialsystem/). App is
exposed via NginX proxy at port `80`.

1. Create your docker-compose.yml file somewhere:

    ```yaml
    version: '3.4'
    services:
        db:
            image: postgres:9.6.10-alpine
            volumes:
                - dbdata:/var/lib/postgresql
            restart: always
            ports:
                - "55432:5432"
            environment:
                POSTGRES_USER: socialsystem
                POSTGRES_PASS: socialsystem
                POSTGRES_DB: socialsystem
        website:
            image: xaralis/socialsystem:latest
            ports:
                - "8000:80"
            restart: always
            environment:
                DEBUG: 1
                DATABASE_DSN: postgresql://socialsystem:socialsystem@db:5432/socialsystem
    volumes:
        dbdata:
    ```

2. Run both the database and the application by a simple `up` command:

        docker-compose up -d

3. Run migrations (in case there are some DB schema changes):

        docker-compose exec --user socialsystem website sh -c "django-admin migrate"

4. Load initial data upon installation:

        docker-compose exec --user socialsystem website sh -c "django-admin loaddata socialsystem/fixtures/initial_data.yml"

*Note*: You can easily update the app by the image tag in the compose file. Make
sure to re-run migrations when updating.

## Running django commands in the container

You can easily run it using `docker exec`. Just make sure you're running it under `socialsystem` user. Otherwise,
things will break.

    docker-compose exec --user socialsystem website django-admin migrate

