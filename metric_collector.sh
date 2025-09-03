#!/bin/bash

set -e

disk_usage=$(df -k / | awk 'NR==2 {print $3}')
memory_usage=$(free -k | awk 'NR==2 {print $3}')

echo "disk=$disk_usage"
echo "memory=$memory_usage"