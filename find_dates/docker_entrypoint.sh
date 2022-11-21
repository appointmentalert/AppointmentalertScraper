#!/bin/bash

echo "starting container"
sleep 40

while true; do
  echo "running loop"
  python main.py
  sleep 60
done