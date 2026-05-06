#!/bin/bash

echo "Starting deployment..."

# Build the base vulnerable_web image
echo "Building vulnerable_web image..."
cd vulnerable_web
docker build -t vulnerable_web .
cd ..

# Create the external network if it doesn't already exist
echo "Setting up global_macvlan_net..."
docker network inspect global_macvlan_net >/dev/null 2>&1 || \
    docker network create -d macvlan --subnet=192.168.100.0/24 --gateway=192.168.100.254 -o parent=eth0 global_macvlan_net

# Start the user app
echo "Starting user application..."
cd user_docker
docker-compose -f user-docker-compose.yml up -d
cd ..

# Start the bot app
# Default to 5 bots if not specified as argument
BOT_COUNT=${1:-5}
echo "Starting $BOT_COUNT bot applications..."
cd bot_docker
# stop any existing orphans if the old service was running
docker-compose -f bot1-docker-compose.yml down --remove-orphans >/dev/null 2>&1 || true
docker-compose -f bot1-docker-compose.yml up -d --scale bot=$BOT_COUNT --remove-orphans
cd ..

# Start the AI Agent (if configured)
echo "Starting AI Agent Template..."
cd agent_template
# Uncomment the line below to automatically boot the AI agent if your API keys are set!
# docker-compose up -d --build
cd ..

echo "Deployment complete! Use 'docker ps' to see running containers."
