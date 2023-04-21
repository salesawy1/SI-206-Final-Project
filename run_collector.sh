#!/bin/bash

count=$1

for i in $(seq 1 $count); do
  echo "Running collector.py iteration $i"
  python3 collector.py
  echo "Iteration $i completed"
done