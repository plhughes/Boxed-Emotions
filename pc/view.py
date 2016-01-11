import numpy as np
import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])

while(cap.isOpened()):
	try:
		ret, frame = cap.read()
		
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	except:
		break

print "End"
cap.release()
cv2.destroyAllWindows()