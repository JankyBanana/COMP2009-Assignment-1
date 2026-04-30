#!/usr/bin/env bash
# Using 'time ./pso_avg.sh' will return running time as:
# real - Actual start-finish time
# user - CPU user-space time
# sys  - CPU kernel-space time

> pso_log.txt  # To clear contents of file before writing
iteration=0
while [[ iteration -lt $1 ]]; do #comparison less-than/equal = lt/le
  iteration=$((iteration + 1))
  echo -ne "Current iteration: $((iteration))\r"
  python3 particle_swarm.py >> pso_log.txt
done

sum=0
for inter in $(awk -F " " '{print $12}' "pso_log.txt"); do
  sum=$((sum + inter))
done

echo -ne "\nPSO takes" $((sum / iteration)) "iterations on average\n"
