#!/bin/bash

echo "Starting Chaos Test"

echo "Stopping node3..."
docker stop node3

sleep 10

echo "Restarting node3..."
docker start node3

sleep 5

echo "Stopping node5..."
docker stop node5

sleep 10

echo "Restarting node5..."
docker start node5

echo "Chaos Test Completed"