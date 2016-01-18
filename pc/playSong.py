
import pygame
import wave

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def main():
	
	pygame.init()
	pygame.mixer.init()
	s = pygame.mixer.Sound('bgSong.wav')
	ch = s.play()

	channels = 1
	swidth = 2

	#wait a while before reading he file
	readWait = 100
	
	#count of waiting to read the file
	readCount = 0
	
	change_rate = 1
	
	playSong = True
	while (True):
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					playSong = False
		
		if playSong:
			if(readCount>=readWait):
				f = open("speed.txt","r")
				string_number = f.read()
				print "string_number", string_number
				if(is_number(string_number)==False):
					continue
				new_rate = float(string_number)
				print "change_rate", change_rate

				if(new_rate!=change_rate):
					s.stop()
					change_rate = int(new_rate)
					#read the current framerate of the song
					spf = wave.open('bgSong.wav', 'rb')
					rate=spf.getframerate()
					signal = spf.readframes(-1)
				
					#change the framerate of the song
					wf = wave.open('bgSong.wav', 'wb')
					wf.setnchannels(channels)
					wf.setsampwidth(swidth)
					wf.setframerate(rate+change_rate)
				
					#write the new wave file
					wf.writeframes(signal)
					wf.close()
					s = pygame.mixer.Sound('bgSong.wav')
				
					#play it again
					ch = s.play()
				readCount = 0	
	
			readCount+=1
		
		else:
			return
		
		
if __name__ == "__main__":
	main()

	