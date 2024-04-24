#!/bin/bash

images_directory="images"
text_directory="text"

mkdir -p "$text_directory"

for image_file in "$images_directory"/*.png; do
    filename=$(basename "$image_file" .png)
    output_base="$text_directory/$filename"
    output_text_file="${output_base}.txt"
    if [ ! -f "$output_text_file" ]; then
        echo "Processing: $filename"
        tesseract "$image_file" "$output_base"
    else
        echo "Already processed: $filename, skipping."
    fi
done


