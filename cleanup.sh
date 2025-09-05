#!/bin/bash

# Remove temporary files
rm -rf /tmp/*
rm -rf /var/tmp/*

# Clear Python cache
find /home/site/wwwroot -type d -name "__pycache__" -exec rm -rf {} +
rm -rf /home/site/wwwroot/*.pyc

# Clear pip cache
rm -rf /root/.cache/pip
rm -rf /home/.local/lib/python*/site-packages

# Clear code profiler
rm -rf /home/site/CodeProfiler

# Clear logs
rm -rf /home/LogFiles/*
rm -rf /home/site/wwwroot/logs/*

# Clear downloaded models
rm -rf /home/site/wwwroot/antenv/lib/python*/site-packages/en_core_web_*

# Clear temp deployment files
rm -rf /home/site/deployments/temp
rm -rf /home/site/repository

# Show disk usage after cleanup
df -h
