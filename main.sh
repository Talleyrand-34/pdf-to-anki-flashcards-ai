#!/bin/bash
#ç
if [ -e "$(dirname "$0")/pdf_files/.gitkeep" ]; then
    rm "$(dirname "$0")/pdf_files/.gitkeep"
    echo "success"
fi

python3 ./pdf-ai-info-processing.py -a
python3 ./anki.py
