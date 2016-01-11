import numpy as np
import cv2
import pygame
import time


def randomizeMusic():
	fileCat = 'happy'
	#songNumber = random.randint(1,100)
	#categoryNumber = random.randint(1,3)
	songNumber = 1
	categoryNumber = 0
	if categoryNumber==0:
		fileCat = 'happy'
	elif categoryNumber==1:
		fileCat = 'sad'
	elif categoryNumber==2:
		fileCat = 'angry'
	filePath = 'songs\\'+fileCat+'\\song'+str(songNumber)+'.wav'
	print filePath
	return [filePath,categoryNumber]
	

def capVid():
	cap = cv2.VideoCapture(0)

	#Define the codec and create VideoWriter object
	fourcc = cv2.cv.CV_FOURCC(*'IYUV') 
	
	music = False
	musicCount = 0
	record = False
	out = None
	numVid = [0, 0, 0]
	waitTime = 200

	
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
			if numW > 100 and not(music):
				music = True
				[filePath,categoryNumber] = randomizeMusic()
				pygame.mixer.music.load(filePath)
				pygame.mixer.music.play(0)
				print "Staring Music"
			
			#increasing music time
			elif music and musicCount <= waitTime:
				musicCount += 1
			
			#start recording
			elif musicCount > waitTime and not(record):
				record = True
				if categoryNumber==0:
					videoFolder = 'happy'
				elif categoryNumber==1:
					videoFolder = 'sad'
				elif categoryNumber==2:
					videoFolder = 'angry'
				name = 'videos\\' + videoFolder + '\\output' + str(numVid[categoryNumber]) + '.avi'
				out = cv2.VideoWriter(name, fourcc, 20.0, (640,480))
				numVid[categoryNumber] += 1
				print "Start Recording"
			
			#stop recording if the perosn left
			elif record and (numW < 100 or pygame.mixer.music.get_busy() == False):
				record = False
				music = False
				musicCount = 0
				out.release()
				pygame.mixer.music.stop()
				print "Stop Recording"	
				time.sleep(30)
			
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
	capVid()