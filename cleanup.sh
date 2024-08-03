#!/bin/bash

# Remove anything between square brackets in MP3 filenames
for file in *.mp3; do
    new_name=$(echo "$file" | sed 's/\[.*\]//')
    mv "$file" "$new_name"
done