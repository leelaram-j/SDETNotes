#!/bin/bash
cd /Users/lee/Documents/SDET_Master/Docker
docker-compose -f docker-compose.yaml up --scale chrome=5 >>output.txt