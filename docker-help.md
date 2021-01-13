# remove all images
`docker rmi (docker images -a --format '{{.ID}}')`

# List images
`docker images -a`

# Build image
`docker build -t <name> .` with a docker file
