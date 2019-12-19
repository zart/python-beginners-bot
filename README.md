This is helper bot for https://t.me/ru_python_beginners administrators.

Not intended for any public use.
# How to run
```cp .docker-compose-example.env .docker-compose.env```

Set parameters in `.docker-compose.env`

# Run
 `docker-compose up -d`
# Stop
`docker-compose down`
# Build and publish image
```
docker build -t docker.pkg.github.com/vlade11115/python-beginners-garbotdge/garbotdge:{version_id} .
docker push docker.pkg.github.com/vlade11115/python-beginners-garbotdge/garbotdge

```
