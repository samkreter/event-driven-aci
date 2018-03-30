# drm
docker build -t pskreter/high-cpu:latest .

if ($args.Count -gt 0 ){
    docker push pskreter/high-cpu:latest
}
else {
    docker run --rm pskreter/high-cpu:latest
}

