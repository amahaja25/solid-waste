#!/bin/bash

pdf_directory="pdfs"
image_directory="images"

mkdir -p "$image_directory"

for pdf_file in "$pdf_directory"/*.pdf; do
    filename=$(basename "$pdf_file" .pdf)
    
    if [ ! -f "$image_directory/${filename}_0.png" ]; then
        pdf2image --output "$image_directory" --image_type png "$pdf_file"
    fi
done