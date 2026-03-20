# Demo only:
# In real production this would likely be orchestrated by a scheduler
# such as Kubernetes CronJob, Airflow, Dagster, ECS Scheduled Tasks, etc.


#!/usr/bin/env bash
set -euo pipefail

while true; do
  echo "=========================================="
  echo "Pipeline started at $(date '+%Y-%m-%d %H:%M:%S')"
  echo "=========================================="

  make full-run

  echo "=========================================="
  echo "Pipeline finished at $(date '+%Y-%m-%d %H:%M:%S')"
  echo "Sleeping for 1 hour..."
  echo "=========================================="

  sleep 3600
done