#!/bin/bash
export DATABASE_URL="postgresql://postgres:password123@localhost:5432/final"
export EXCITED="true"

echo $DATABASE_URL
echo $EXCITED
echo "setup.sh script executed successfully!"