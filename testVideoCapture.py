import numpy as np
import cv2

cap = cv2.VideoCapture(0)

#Define the codec and create VideoWriter object
fourcc = cv2.cv.CV_FOURCC(*'IYUV') 
record = False
out = None
numVid = 0

while(True):
	# Capture frame-by-frame
	ret, frame = cap.read()

	if ret == True:
		#make the picture black and white
		gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		ret, black = cv2.threshold(gray,205,255,cv2.THRESH_BINARY)
		
		
		#num white pic
		numW  = cv2.countNonZero(black)
		
		#start recording
		if numW > 100 and not(record):
			record = True
			name = 'output' + str(numVid) + '.avi'
			out = cv2.VideoWriter(name, fourcc, 20.0, (640,480))
			numVid += 1
			print "Start Recording"
		
		#stop recording
		if numW < 100 and record:
			record = False
			out.release()
			print "Stop Recording"
		
		if record:
			out.write(black)
		
		
		#display the resulting frame
		cv2.imshow('frame',black)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

#release the capture
cap.release()
cv2.destroyAllWindows()