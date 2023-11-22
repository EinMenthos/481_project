#!/bin/bash

# Specify the number of times to run the command
num_runs=1000

# Loop to run the command
for ((i = 1; i <= num_runs; i++)); do
  python3 game3.py
done