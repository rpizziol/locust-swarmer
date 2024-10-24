#!/bin/bash

# Define an array of user values
user_values=(10 15 20 25 30 35 40)

# Loop through each user value, run the command, and wait for 1 minute after each run
for u in "${user_values[@]}"; do
  python3 run_experiment.py -m HPA -wa 3tier -ht 34.152.30.67 -wl fixed -d 20 -n u${u}-20m -u $u
  echo "Waiting for 1 minute before starting the next experiment..."
  sleep 60  # Wait for 60 seconds (1 minute)
done
