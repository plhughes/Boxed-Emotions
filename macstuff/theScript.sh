#!/bin/bash 
COUNTER=1
python testVideoCapture.py
for category in happy angry sad
do
	while true; do
		OUTPUT="videos/"
		OUTPUT+=$category
		OUTPUT+="/out"
		OUTPUT+=$COUNTER
		OUTPUT+=".avi"
		
		FILENAME="images/"
		FILENAME+=$category
		FILENAME+="/output"
		
		FILE="images/"
		FILE+=$category
		FILE+="/output"
		LASTPART="_numpic_%4d.png"
		LASTPART2="_numpic_0000.png"
		FILENAME+=$COUNTER
		FILENAME+=$LASTPART
		FILE+=$COUNTER
		FILE+=$LASTPART2  
		echo $FILE
		if [ -f $FILE ]
		then
			ffmpeg -framerate 15 -i $FILENAME -c:v libx264 -r 30 -pix_fmt yuv420p $OUTPUT
			((COUNTER+=1))
		else
			break
		fi
	done
	rm images/$category/output*.png
done