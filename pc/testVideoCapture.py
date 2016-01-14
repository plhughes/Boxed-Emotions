import numpy as np
import cv2
import pygame
import random
import sys
import os


def randomizeMusic():
	fileCat = 'happy'
	songNumber = random.randint(0,8)
	categoryNumber = random.randint(0,2)
	#songNumber = 1
	#categoryNumber = 0
	if categoryNumber==0:
		fileCat = 'happy'
	elif categoryNumber==1:
		fileCat = 'angry'
	elif categoryNumber==2:
		fileCat = 'sad'
	filePath = 'songs\\'+fileCat+'\\song'+str(songNumber)+'.wav'
	print filePath
	return [filePath,categoryNumber]
	

def capVid(argv):
	cap = cv2.VideoCapture(1)

	#Define the codec and create VideoWriter object 
	fourcc = cv2.cv.CV_FOURCC(*'MSVC')
	out = None
	numVid = [0, 0, 0]
	record = False
	music = False
	musicCount = 0
	waitTime = 200
	
	#allows time between when music stop and person leaves
	waitPersonLeave = 500
	if len(argv) > 1:
		waitPersonLeave = int(argv[1])
	personWaitCount = waitPersonLeave
	print "Will wait ", waitPersonLeave
	
	#music
	pygame.init()
	pygame.mixer.init()
	
	
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()

		if ret == True:
			#make the picture black and white
			gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
			ret, black = cv2.threshold(gray,205,255,cv2.THRESH_BINARY)
			
			#num white pic
			numW  = cv2.countNonZero(black)
			
			#start music
			if numW > 100 and not(music) and personWaitCount > waitPersonLeave:
				music = True
				[filePath,categoryNumber] = randomizeMusic()
				pygame.mixer.music.load(filePath)
				pygame.mixer.music.play(0)
				print "Staring Music"
			
			#increasing music time
			elif music and musicCount <= waitTime:
				musicCount += 1
			
			#create new video
			elif musicCount > waitTime and not(record):
				record = True
				if categoryNumber==0:
					videoFolder = 'happy'
				elif categoryNumber==1:
					videoFolder = 'angry'
				elif categoryNumber==2:
					videoFolder = 'sad'
				num = numVid[categoryNumber]
				name = 'videos\\' + videoFolder + '\\output' + str(num) + '.avi'
				out = cv2.VideoWriter(name, fourcc, 8.0, (640,480))
				numVid[categoryNumber] += 1
				print "Start Recording"
				
				#delete older videos
				if num > 9:
					deleteName = 'videos\\' + videoFolder + '\\output' + str(num-10) + '.avi'
					print "Deleting ", deleteName
					os.remove(deleteName)
			
			#stop recording if the person left
			elif record and (numW < 100 or pygame.mixer.music.get_busy() == False):
				record = False
				music = False
				musicCount = 0
				personWaitCount = 0
				out.release()
				pygame.mixer.music.stop()
				print "Stop Recording"
			
			#waiting a few seconds
			#allows time for user to leave
			elif not(record) and not(music):
				personWaitCount += 1
				
			#record
			elif record:
				out.write(black)
			
			
			#display the resulting frame
			cv2.imshow('frame',black)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	#release the capture
	cap.release()
	cv2.destroyAllWindows()
	
if __name__ == "__main__":
	capVid(sys.argv)