#!/bin/bash

# Define the source directories on the VM 
SOURCE_DIR1="/CONTENT/Articles/."
SOURCE_DIR2="/CONTENT/Reports/."
SOURCE_DIR3="/CONTENT/Images/."

#Define the target dirs in containers
TARGET_DIR1="/articles"
TARGET_DIR2="/docs"
TARGET_DIR3="/images"

# Define the Docker container names
CONTAINER1="rt-container"

# Copy files from VM to Docker containers
docker cp $SOURCE_DIR1 $CONTAINER1:$TARGET_DIR1
docker cp $SOURCE_DIR2 $CONTAINER1:$TARGET_DIR2
docker cp $SOURCE_DIR3 $CONTAINER1:$TARGET_DIR3

echo "Files copied successfully."
