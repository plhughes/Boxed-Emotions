import numpy as np
import sys
import cv2
import pygame
import random


def randomizeMusic():
	fileCat = 'happy'
	songNumber = random.randint(1,100)
	categoryNumber = random.randint(1,3)
	if categoryNumber==2:
		fileCat = 'sad'
	elif categoryNumber==3:
		fileCat = 'angry'
	fileCat = 'happy'
	categoryNumber = 1
	filePath = 'songs/'+fileCat+'/song'+str(categoryNumber)+'.wav'
	return [filePath,categoryNumber]
	

def main():
	cap = cv2.VideoCapture(0)

	if not cap.isOpened():
		print("can't open the camera")

	#Define the codec and create VideoWriter object
	fourcc = cv2.cv.CV_FOURCC(*'SVQ3') 
	record = False
	play = False
	waitRecord = 0
	waitTime = 50
	numVid = 0
	numPics = 0
	[filePath,categoryNumber] = randomizeMusic()
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load(filePath)
	videoFolder = '';
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
			if numW > 100 and not(play):
				pygame.mixer.music.play(0)
				play = True
		
			if play:
				waitRecord+=1
			
			if play and waitRecord>=waitTime and not(record):
				record = True
				numVid += 1
				print "Start Recording"
	
			#stop recording
			if numW < 100 and record:
				record = False
				play = False
				waitRecord = 0
				print "Stop Recording"
				numPics = 0
				pygame.mixer.music.stop()
				[filePath,categoryNumber] = randomizeMusic()
				pygame.mixer.music.load(filePath)
	
			if record:
				index = str(numPics)
				while(len(index) != 4):
					index = '0' + index
				if categoryNumber==1:
					videoFolder = 'happy'
				elif categoryNumber==2:
					videoFoder = 'sad'
				elif categoryNumber==3:
					videoFolder = 'angry'
				name = 'images/'+videoFolder+'/output' + str(numVid) +'_numpic_'+index+'.png'
				print name
				#name = 'output' + str(numVid) +'_numpic_'+index+'.png'
				cv2.imwrite(name,black)
				numPics+=1
	
	
			#display the resulting frame
			cv2.imshow('frame',black)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	#release the capture
	cap.release()
	cv2.destroyAllWindows()
	
if __name__ == "__main__":
	main()
