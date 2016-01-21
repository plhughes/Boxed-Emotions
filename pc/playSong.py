#Boxed Emotion

import pygame
import wave

'''A function to check if s is a float'''
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

'''Main program'''
def main():
	
	pygame.init()
	pygame.mixer.init()
	s = pygame.mixer.Sound('bgSong.wav')
	ch = s.play()

	channels = 1
	swidth = 2
	
	threshold = 80.0
	color = 125.0
	
	#wait a while before reading he file
	readWait = 100
	
	#count of waiting to read the file
	readCount = 0
	
	change_rate = 1
	max_change_rate = 5000
	
	playSong = True
	while (True):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					playSong = False
		
		if playSong:
			if(readCount>=readWait):
			
				#read in the avg rgb color from speed.txt
				f = open("/Volumes/Courses/CS267/BoxedEmotion/speed.txt","r")
				string_number = f.read()
				#print "string_number", string_number
				if(is_number(string_number)==False):
					continue
				new_color = float(string_number)
				#print "change_rate", change_rate
				
				#if the new color is different from the old one
				#change the change_rate according to the threshold
				if(new_color!=color):
					s.stop()
					color = new_color
					if(color<=threshold):
						change_rate = -max_change_rate
						
					else:
						change_rate = max_change_rate
					#read the current framerate of the song
					spf = wave.open('bgSong.wav', 'rb')
					rate=spf.getframerate()
					signal = spf.readframes(-1)
				
					#change the framerate of the song
					wf = wave.open('bgSong.wav', 'wb')
					wf.setnchannels(channels)
					wf.setsampwidth(swidth)
					new_rate = rate+change_rate
					if new_rate<20000:
						new_rate = 20000
					elif new_rate > 500000:
						new_rate = 500000
						
					wf.setframerate(new_rate)
					print "color", color
					print "change_rate", change_rate
					print "old_rate", rate
					print "new_rate", new_rate
				
					#write the new wave file
					wf.writeframes(signal)
					wf.close()
					s = pygame.mixer.Sound('bgSong.wav')
				
					#play it again
					ch = s.play(-1)
				readCount = 0	
	
			readCount+=1
		
		else:
			return
		
		
if __name__ == "__main__":
	main()

	