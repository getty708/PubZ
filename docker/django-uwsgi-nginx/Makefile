PUBZ_VERSION := 0.5.0


help:
	@echo If you cannot build image with docker-compose, build container by `make build.`

build:
	cp ../../pyproject.toml .
	cp ../../poetry.lock .
	cp -r ../../src .
	docker build -t pubz:web-prd-v${PUBZ_VERSION} .
