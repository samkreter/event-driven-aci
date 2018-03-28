brun:
	docker build -t web-server .
	docker run --rm -p 8000:8000  web-server

build: 
	docker build -t web-server .

run:
	docker run --rm -p 8000:8000  web-server

dev:
	docker run -it --rm -p 8000:8000 -v ${PWD}:/app web-server /bin/bash