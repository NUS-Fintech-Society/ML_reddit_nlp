#!/bin/bash

downloadLinks="./Links"
logFile="./log/$(date +"%FT%T.log")"
mkdir -p "./tmp/compressed"
mkdir -p "./tmp/decompressed"
mkdir -p "./log"
mkdir -p "./data"
while read -r line
do
	echo "------Downloading from $line------" | tee -a "$logFile"
	echo "" >> "$logFile"
	wget "$line" -P "./tmp/compressed" -a "$logFile"
	compressed="$(ls "./tmp/compressed")"
	echo "------Decompressing $compressed------" | tee -a "$logFile"
	echo "" >> "$logFile"
	if [[ $compressed == *.zst ]]; then
		zstd --rm -d "./tmp/compressed/$compressed" --long=31 | tee -a "$logFile"
	elif [[ $compressed == *.bz2 ]]; then
		bzip2 -d "./tmp/compressed/$compressed" -v | tee -a "$logFile"
	elif [[ $compressed == *.xz ]]; then
		xz -d "./tmp/compressed/$compressed" -v | tee -a "$logFile"
	fi
	uncompressed="$(ls "./tmp/compressed")"
	mv "./tmp/compressed/$uncompressed" "./tmp/decompressed"
	echo "------Parsing $uncompressed------" | tee -a "$logFile"
        echo "" >> "$logFile"
	java -jar Reddit_Scraper.jar "$uncompressed"
	rm "./tmp/decompressed/$uncompressed"
done < "$downloadLinks"
echo "------Finished------" | tee -a "$logFile"
rm -r "./tmp"
