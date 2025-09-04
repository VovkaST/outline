docker build -t outline-app-python-3.10:latest .

docker compose up -d server bot

# Removing all dangling build cache
docker builder prune --force

# Removing all dangling images
docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
