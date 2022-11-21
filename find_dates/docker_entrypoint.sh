#!/bin/bash

echo "starting container"

while true; do
  echo "waiting 60 seconds"
  sleep 60
  echo "running scraper"
  python main.py
done