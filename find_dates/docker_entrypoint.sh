#!/bin/bash

echo "starting container"
sleep 30

while true; do
  echo "running loop"
  python main.py
  sleep 60
done