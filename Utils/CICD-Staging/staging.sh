#!/bin/bash

# Define the source directories on the VM 
SOURCE_DIR1="/STAGING/Articles"
SOURCE_DIR2="/STAGING/Reports"
SOURCE_DIR3="/STAGING/Images"

#Define the target dirs
TARGET_DIR1="/CONTENT/Articles"
TARGET_DIR2="/CONTENT/Reports"
TARGET_DIR3="/CONTENT/Images"



# Copy all markdown files in all of the subdirectories of SOURCE_DIR1 to TARGET_DIR1
find $SOURCE_DIR1 -name "*.md" -exec cp {} $TARGET_DIR1 \;

rsync -a $SOURCE_DIR2/ $TARGET_DIR2/
rsync -a $SOURCE_DIR3/ $TARGET_DIR3/



echo "Files copied successfully."
