#!/bin/bash
cp response.csv response2.csv
# Find the line number of "Question,Answer"
line_num=$(grep -n "Question,Answer" response.csv | head -n 1 | cut -d ":" -f 1)

# Remove all lines before "Question,Answer"
sed -i "1,$((line_num-1))d" response.csv
if [ $? -ne 0 ]
then
    echo "Error: sed command failed to remove lines before 'Question,Answer'" >&2
    exit 1
fi

# Remove all lines that are exactly "Question,Answer"
sed -i "/^Question,Answer$/d" response.csv
if [ $? -ne 0 ]
then
    echo "Error: sed command failed to remove lines that are exactly 'Question,Answer'" >&2
    exit 2
fi

# Delete last two characters of last line
sed -i '$ s/..$//' response.csv
if [ $? -ne 0 ]
then
    echo "Error: sed command failed to delete last two characters of last line" >&2
    exit 3
fi

exit 0
