#!/bin/bash
filename="current_tag.txt"
echo $filename
echo "read"
#!/usr/bin/bas
while read -r line; do
    name="$line"
    echo "Name read from file - $name"
done < "$filename"
echo $name
