I'm missing a proper development setup on my personal computer currently since I just rebuilt, so this is definitely missing some stuff, sorry!

You should be able to run this by just building and running the docker image
`docker build -t api .`
`docker run -p 8080:8080 api`

and then you can send requests to `localhost:8080`

Currently missing:
- requirements (need a pipenv to freeze)
- unit tests (would usually use this for dev, but no setup)
- docker verification (been a while and would need to confirm everything works)