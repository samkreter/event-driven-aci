# drm
docker build -t pskreter/web-server:latest .

if ($args.Count -gt 0 ){
    docker run -it --rm -p 8000:8000 -v ${PWD}:/app pskreter/web-server:latest /bin/bash
}
else {
    docker run --rm -p 8000:8000  web-server
}

