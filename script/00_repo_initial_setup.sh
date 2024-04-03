#!/bin/bash
# Purpose: Setup the project for the first time
# Run this in the repo root directory

mkdir data
echo "Created 'data' directory"

echo "Environment variables:"
cp env.sample .env
echo "Copied env.sample to .env, please update the values inside"
