#!/bin/bash

python3 /data/echorf.py
mkdir /data/Informes

for dirname in /data/*/; do
	rf=$(find "$dirname" -type f -name "*.tex")
	pdflatex --output-directory=/data/Informes "$rf"
	sleep 5
	pdflatex --output-directory=/data/Informes "$rf"
done

rm /data/Informes/*.log
rm /data/Informes/*.aux
