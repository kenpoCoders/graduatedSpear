#!/bin/bash
for filename in *.png; do
 echo "convert ./orig/$filename -resize 30% $filename"
 convert ./orig/$filename -resize 30% $filename
done
