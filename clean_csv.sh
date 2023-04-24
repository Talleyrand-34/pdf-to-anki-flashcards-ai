#!/bin/bash

for file in ./out_csv/*.csv; do
    pwd
    ls "$file"
    cat "$file"
    # Find the line number of "Question,Answer"
    line_num=$(grep -n "Question|Answer" "$file" | head -n 1 | cut -d ":" -f 1)
    echo "line_num = $line_num"

    if [ -z "$line_num" ]; then
        echo "Error: 'Question,Answer' not found in file $file" >&2
        continue
    fi

    # Remove all lines before "Question,Answer"
    sed -i "1,$((line_num-1))d" "$file"
    if [ $? -ne 0 ]; then
        echo "Error: sed command failed to remove lines before 'Question,Answer' in file $file" >&2
    fi

    # Remove all lines that are exactly "Question,Answer"
    sed -i "/^Question,Answer$/d" "$file"
    if [ $? -ne 0 ]; then
        echo "Error: sed command failed to remove lines that are exactly 'Question,Answer' in file $file" >&2
    fi

    # Delete last two characters of last line
    sed -i '$s/..$//' "$file"
    if [ $? -ne 0 ]; then
        echo "Error: sed command failed to delete last two characters of last line in file $file" >&2
    fi
done

exit 0

